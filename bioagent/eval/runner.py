import os
import json
import asyncio
from typing import Dict, Any, Optional
from dataclasses import asdict
from tqdm import tqdm
import pandas as pd

from ..config import exact_match, dump_json
from .judge import LLMJudge


class EvalRunner:
	def __init__(self, agent, dataset, out_dir: str, judge: Optional[LLMJudge] = None, forced_choice: bool = False):
		self.agent = agent
		self.dataset = dataset
		self.out_dir = out_dir
		self.judge = judge
		self.forced_choice = forced_choice
		os.makedirs(self.out_dir, exist_ok=True)
		self.traj_path = os.path.join(self.out_dir, "trajectories.jsonl")
		self.metrics_path = os.path.join(self.out_dir, "metrics.json")
		self.csv_path = os.path.join(self.out_dir, "metrics.csv")

	async def arun(self, limit: Optional[int] = None) -> Dict[str, Any]:
		total = 0
		right = 0
		rows = []
		with open(self.traj_path, "w", encoding="utf-8") as ftraj:
			for ex in tqdm(self.dataset.iter(limit=limit), total=(limit or len(self.dataset))):
				total += 1
				qid = ex["id"]
				question = ex["question"]
				# If multiple-choice options are available and forced-choice is enabled, append them to the question
				if self.forced_choice and "options" in ex and isinstance(ex["options"], list) and ex["options"]:
					opts = "\n".join(f"- {o}" for o in ex["options"])
					question = f"{question}\n\nYou must answer by selecting exactly one of the following options and output only the option text.\nOptions:\n{opts}"
				gold = ex["answer"]
				res = await self.agent.arun(question)
				pred = res.get("final_answer", "")
				ok = exact_match(pred, gold)
				judged_ok = None
				judge_raw = None
				if self.judge is not None and not ok:
					try:
						jr = await self.judge.ajudge(question, gold, pred, res["trajectory"])
						judged_ok = bool(jr.get("ok"))
						judge_raw = jr.get("raw")
					except Exception:
						judged_ok = None
				if ok:
					right += 1
					
				record = {
					"id": qid,
					"question": question,
					"gold": gold,
					"pred": pred,
					"ok": bool(ok),
					"judged_ok": judged_ok,
					"judge_raw": judge_raw,
					"trajectory": res["trajectory"],
				}
				ftraj.write(json.dumps(record, ensure_ascii=False) + "\n")
				rows.append(record)

		acc = right / max(total, 1)
		# judged metrics if present
		judged_total = 0
		judged_correct = 0
		for row in rows:
			if row.get("judged_ok") is not None:
				judged_total += 1
				if row.get("judged_ok"):
					judged_correct += 1
		judged_acc = (judged_correct / judged_total) if judged_total else None

		metrics = {
			"total": total,
			"correct": right,
			"accuracy": acc,
			"judged_total": judged_total,
			"judged_correct": judged_correct,
			"judged_accuracy": judged_acc,
			"mode": "forced_choice" if self.forced_choice else "free_form",
		}
		dump_json(self.metrics_path, metrics)
		pd.DataFrame(rows).to_csv(self.csv_path, index=False)
		return metrics


