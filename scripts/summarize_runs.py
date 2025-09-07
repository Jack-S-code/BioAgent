#!/usr/bin/env python
import os
import json
import glob
from collections import Counter


def load_metrics(run_dir: str):
	path = os.path.join(run_dir, "metrics.json")
	if os.path.exists(path):
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	return None


def tool_stats(run_dir: str):
	traj = os.path.join(run_dir, "trajectories.jsonl")
	ctr = Counter()
	steps = 0
	if os.path.exists(traj):
		with open(traj, "r", encoding="utf-8") as f:
			for line in f:
				try:
					obj = json.loads(line)
					for ev in obj.get("trajectory", []):
						if ev.get("role") == "tool":
							ctr[ev.get("name", "")] += 1
						steps += 1
				except Exception:
					continue
	return {"tool_calls": dict(ctr), "total_steps": steps}


def main():
	runs = sorted(glob.glob("runs/*"))
	rows = []
	for rd in runs:
		m = load_metrics(rd)
		if not m:
			continue
		stats = tool_stats(rd)
		rows.append({
			"run": os.path.basename(rd),
			"mode": m.get("mode"),
			"total": m.get("total"),
			"accuracy": m.get("accuracy"),
			"judged_accuracy": m.get("judged_accuracy"),
			"tool_calls": stats.get("tool_calls"),
			"total_steps": stats.get("total_steps"),
		})
	print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
	main()


