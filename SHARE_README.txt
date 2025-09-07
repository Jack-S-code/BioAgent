Quick Start
===========

1) python -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) export OPENAI_BASE_URL=... && export OPENAI_API_KEY=...
4) python scripts/evaluate.py --dataset hf --hf-path futurehouse/lab-bench --subset CloningScenarios --split train --limit 5 --model openai --model-name kimi-k2-turbo-preview --openai-base-url  --openai-api-key  --judge --out-dir runs/demo
5) python scripts/summarize_runs.py && python scripts/make_markdown_report.py

Docs:
- docs/progress_report_zh.md
- docs/run_details_zh.md
