#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import glob


def short(text: str, n: int = 80) -> str:
	text = (text or "").replace("\n", " ").strip()
	return text if len(text) <= n else text[: n - 1] + "…"


def read_summary(summary_path: str):
	if not os.path.exists(summary_path):
		raise FileNotFoundError(summary_path)
	with open(summary_path, "r", encoding="utf-8") as f:
		return json.load(f)


from typing import Optional


def iter_examples(run_dir: str, limit: Optional[int] = None):
	path = os.path.join(run_dir, "trajectories.jsonl")
	if not os.path.exists(path):
		return []
	rows = []
	with open(path, "r", encoding="utf-8") as f:
		for i, line in enumerate(f):
			obj = json.loads(line)
			traj = obj.get("trajectory", [])
			tools = [e.get("name") for e in traj if e.get("role") == "tool"]
			tools_seq = []
			for t in tools:
				if t and (not tools_seq or tools_seq[-1] != t):
					tools_seq.append(t)
			rows.append({
				"id": obj.get("id"),
				"question": short(obj.get("question", ""), 100),
				"gold": short(obj.get("gold", ""), 60),
				"pred": short(obj.get("pred", ""), 60),
				"ok": obj.get("ok"),
				"judged_ok": obj.get("judged_ok"),
				"tool_calls": len(tools),
				"tools_seq": ", ".join(tools_seq) if tools_seq else "-",
				"steps": len(traj),
			})
			if limit and len(rows) >= limit:
				break
	return rows


def make_md(summary_path: str, out_md: str, examples_per_run: int = 5):
	summary = read_summary(summary_path)
	lines = []
	lines.append("运行汇总与工具调用细节（自动生成）\n")
	lines.append("\n总体汇总\n--------\n")
	lines.append("| run | mode | total | EM acc | judged acc | tool_calls | steps |")
	lines.append("|---|---|---:|---:|---:|---|---:|")
	for r in summary:
		tool_calls = r.get("tool_calls", {})
		tool_str = ", ".join(f"{k}={v}" for k, v in tool_calls.items()) or "-"
		lines.append(
			f"| {r['run']} | {r.get('mode') or '-'} | {r.get('total')} | {r.get('accuracy')} | {r.get('judged_accuracy') or '-'} | {tool_str} | {r.get('total_steps')} |"
		)

	for r in summary:
		run_dir = os.path.join(os.path.dirname(summary_path), r["run"]) if os.path.basename(summary_path) == "summary.json" else os.path.join("runs", r["run"]) 
		lines.append("\n" + r["run"] + "\n" + "-" * len(r["run"]) + "\n")
		lines.append("| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |")
		lines.append("|---|---|---|---|:--:|:--:|---:|---|---:|")
		for ex in iter_examples(run_dir, examples_per_run):
			lines.append(
				f"| {ex['id']} | {ex['question']} | {ex['gold']} | {ex['pred']} | {ex['ok']} | {ex.get('judged_ok')} | {ex['tool_calls']} | {ex['tools_seq']} | {ex['steps']} |"
			)

	os.makedirs(os.path.dirname(out_md), exist_ok=True)
	with open(out_md, "w", encoding="utf-8") as f:
		f.write("\n".join(lines))
	print(f"Wrote {out_md}")


if __name__ == "__main__":
	make_md("runs/summary.json", "docs/run_details_zh.md", examples_per_run=5)


