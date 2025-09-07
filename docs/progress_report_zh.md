BioAgent 评测框架工作进度汇报（阶段版）
====================================

一、目标与范围
--------------
- 目标：搭建可替换模型/数据/工具的通用 ReAct 评测框架，产出完整交互轨迹与自动化指标（Exact Match + LLM 判分）。
- 评测数据：HLE 生物子集（gated，split=train）、Lab Bench（含 8 子集，本阶段在 CloningScenarios 上验证）。
- 模型：优先使用 OpenAI 兼容 API（本阶段用 Kimi），后续可切换本地小模型。

二、当前框架与实现
------------------
1) 目录与核心组件
- `bioagent/agent/react.py`：ReAct 主循环
  - 严格标签协议：`<tool_call> {json} </tool_call>`、`<tool_response> {json} </tool_response>`、`<final_answer>...</final_answer>`
  - 限步控制、轨迹记录
- `bioagent/tools/`：工具封装
  - `SerperSearch`：serper.dev 搜索
  - `JinaCrawl`：Jina Reader 抓取
- `bioagent/models/openai_compat.py`：OpenAI 兼容聊天接口（可指定 base_url+api_key）
- `bioagent/datasets/hf.py`：HF 数据集适配
  - 自动识别字段（question / answer / ideal 等）
  - 若有 `distractors`，可输出 `options` 用于“强制选项”模式
- `bioagent/eval/runner.py`：评测执行器
  - 保存轨迹 `trajectories.jsonl`，输出 `metrics.json|csv`
  - 指标：EM（归一化大小写/标点）、LLM 判分（judged_accuracy）
- `bioagent/eval/judge.py`：LLM-as-a-Judge（OpenAI 兼容）
  - 返回 `{ok, reason}`；框架记录 `judged_ok` 与 `judge_raw`
- `scripts/evaluate.py`：CLI 入口
  - 关键参数：`--openai-base-url`、`--openai-api-key`、`--judge`、`--judge-model`、`--forced_choice`
- `scripts/inspect_dataset.py`：查看子集列名与样例
- `scripts/summarize_runs.py`：聚合 runs 下历史评测结果与工具调用统计

2) ReAct 提示词优化
- 加入少量示例，强调只用标签输出、最终答案应“短、唯一、无解释”。
- 在“强制选项”时，将选项拼接到问题末尾并硬约束“仅输出选项文本”。

三、环境与运行方式（可复现）
--------------------------
1) 安装
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) 凭据
```bash
# Kimi（OpenAI 兼容）
export OPENAI_BASE_URL=https://api.moonshot.cn/v1
export OPENAI_API_KEY=你的_kimi_key

# 可选：工具
export SERPER_API_KEY=<serper_key>
export JINA_API_KEY=<jina_key>

# HuggingFace（HLE 为 gated）
export HUGGINGFACEHUB_API_TOKEN=<hf_token>
```

3) 示例命令
```bash
# 自由作答 + LLM 判分
python scripts/evaluate.py \
  --dataset hf --hf-path futurehouse/lab-bench --subset CloningScenarios --split train \
  --limit 15 --model openai --model-name kimi-k2-turbo-preview \
  --openai-base-url $OPENAI_BASE_URL --openai-api-key $OPENAI_API_KEY \
  --judge --judge-model kimi-k2-turbo-preview \
  --out-dir runs/labbench-cloning-kimi-free15

# 强制选项（附加指标）
python scripts/evaluate.py \
  --dataset hf --hf-path futurehouse/lab-bench --subset CloningScenarios --split train \
  --limit 15 --model openai --model-name kimi-k2-turbo-preview \
  --openai-base-url $OPENAI_BASE_URL --openai-api-key $OPENAI_API_KEY \
  --judge --forced_choice \
  --out-dir runs/labbench-cloning-kimi-free-fc15
```

四、阶段性结果与统计（CloningScenarios）
--------------------------------------
- 所有运行的聚合见 `runs/summary.json`（由 `scripts/summarize_runs.py` 生成）。

汇总（节选）：

| run | mode | total | EM acc | judged acc | tool_calls | steps |
|---|---|---:|---:|---:|---|---:|
| labbench-cloning-kimi-free15 | free_form | 15 | 0.00 | 0.20 | serper=30, crawl=3 | 77 |
| labbench-cloning-kimi-free-fc15 | forced_choice | 15 | 0.20 | 0.50 | serper=32, crawl=4 | 82 |
| labbench-cloning-kimi-v5 | – | 3 | 0.67 | – | serper=5, crawl=1 | 14 |
| labbench-cloning-kimi | – | 3 | 0.00 | – | serper=7, crawl=1 | 19 |
| labbench-cloning-kimi-judge | – | 3 | 0.67 | – | serper=6 | 14 |

要点解读：
- 强制选项 > 自由作答：EM 0.20 vs 0.00、Judge 0.50 vs 0.20。约束输出格式可明显降低“跑题/冗长解释导致的 EM 失败”。
- Judge>EM 的差距提示：自由作答存在“语义接近但格式不一致”的情况（单位、标点、附带说明等）。
- 工具使用：每 15 条样本约 30+ 次搜索、3–4 次网页抓取；抓取更集中在需要证据汇总的题目。

五、问题与改进方向
------------------
1) 自由作答命中率偏低的主要原因
- 最终答案含解释/同义变形，与金标的短答案不一致；
- 从检索结果到“短答案”的抽取/压缩不充分；
- 个别工具响应与题目实体对齐不足（比如未定位到题目特定构件）。

2) 立即可行的优化
- 提示层：
  - 在最终回答前，加入“只输出短答案（或从选项中原样输出）”的强约束；
  - 加少量域内 few-shot（题干→短答案）范例；
- 规约层：
  - 对数字/序列类答案做轻量正则归一化（空格/逗号/大小写）；
  - 自由作答保留 EM 与 judged 两套指标，主报告以“自由作答+LLM 判分”为主；
- 策略层：
  - 当检索结果充足时，自动进入“候选抽取→答案压缩”的子流程；
  - 对包含 `distractors` 的题，默认并行产出 forced-choice 附加指标用于稳定对比。

六、已完成里程碑（按时间序）
--------------------------
1) 框架搭建：包结构、依赖、README、CLI 初版
2) 工具封装：Serper、Jina（含缓存/日志）
3) 模型接口：OpenAI 兼容客户端；支持自定义 base_url 与 key（已接入 Kimi）
4) 数据集：HF 适配、字段自动识别、`inspect_dataset.py`
5) ReAct：标签协议与轨迹记录；步数/超时
6) 评测与指标：EM + 轨迹；CSV/JSON 汇总
7) 强制选项：自动拼接 `options`，提升 EM 稳定性
8) LLM 判分：`--judge` 与 `--judge-model`，输出 `judged_accuracy`
9) 运行汇总：`scripts/summarize_runs.py` 统计所有 run 的指标与工具调用

七、下一步计划（建议）
--------------------
- A. 提示与规约：
  - 强化“答案压缩”模板；为数值/单位/序列设计归一化；
- B. 数据与任务扩展：
  - Lab Bench 其余 7 子集各取 10–20 条；HLE 生物子集 train 取 20 条；
- C. 工具与证据链：
  - 新增生物数据库（如 UniProt/GeneCards）适配器（离线/在线均可）；
- D. 成本与并发：
  - 控制 limit，复用缓存，保留失败重试（已在 Jina 内建）；
- E. 报告化：
  - 统一输出实验卡片（模型/数据/时间/成本/指标），便于项目周报归档。

八、附：关键产物路径
--------------------
- 轨迹：`runs/<name>/trajectories.jsonl`
- 指标：`runs/<name>/metrics.json|csv`
- 聚合：`runs/summary.json`
- 评测脚本：`scripts/evaluate.py`
- 汇总脚本：`scripts/summarize_runs.py`


