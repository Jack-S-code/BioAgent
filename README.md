BioAgent Evaluation Framework
=============================

Purpose: A pluggable, reproducible ReAct-style evaluation framework for biomedical agent models. It can run any OpenAI-compatible API model or a local model, operate tools (web search, page crawl), and evaluate accuracy on datasets like `futurehouse/hle-gold-bio-chem` and `futurehouse/lab-bench` while saving full trajectories (Q ⇒ A with tool calls).

Quick Start
-----------

1) Install dependencies:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Set environment variables (use your own keys):

```bash
export OPENAI_API_KEY=sk-xxx
# optional if using custom endpoint
# export OPENAI_BASE_URL=https://api.openai.com/v1

# Tools
export SERPER_API_KEY=serper_dev_key
export JINA_API_KEY=jina_xxx
```

3) Run an evaluation (example):

```bash
python scripts/evaluate.py \
  --dataset hf \
  --hf-path futurehouse/hle-gold-bio-chem \
  --split test \
  --question-field question --answer-field answer \
  --limit 20 \
  --model openai --model-name gpt-4o-mini \
  --out-dir runs/demo
```

Artifacts
---------
- Trajectories: JSONL with per-sample ReAct steps and tool interactions
- Metrics: JSON and CSV summary (accuracy, steps, latency)

Design
------
- Pluggable datasets via adapters (`bioagent/datasets`)
- Pluggable models via a simple chat interface (`bioagent/models`)
- Tools are plain Python callables returning JSON, registered by name (`bioagent/tools`)
- ReAct loop enforces a schema:
  - The model may emit tool calls inside `<tool_call>{...}</tool_call>` tags
  - Tool results are fed back using `<tool_response>{...}</tool_response>`
  - Final answer must be emitted inside `<final_answer>...</final_answer>`

Notes
-----
- This repo prioritizes a clean scaffold for evaluation. You can swap models, datasets, and tools without touching the core loop.

Custom OpenAI-compatible API
----------------------------
If you have a self-hosted OpenAI-compatible endpoint, pass base URL and API key without setting env vars:

```bash
python scripts/evaluate.py \
  --dataset hf \
  --hf-path futurehouse/hle-gold-bio-chem \
  --split test \
  --question-field question --answer-field answer \
  --limit 5 \
  --model openai --model-name qwen2.5 \
  --openai-base-url http://35.220.164.252:3888/v1 \
  --openai-api-key demo-key \
  --out-dir runs/api-demo
```


