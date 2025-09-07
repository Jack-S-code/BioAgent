import asyncio
import json
import re
from typing import Any, Dict, List, Callable


TOOL_CALL_RE = re.compile(r"<tool_call>\s*(\{[\s\S]*?\})\s*</tool_call>")
FINAL_ANSWER_RE = re.compile(r"<final_answer>([\s\S]*?)</final_answer>")


class ReActAgent:
	def __init__(self, model, tools: Dict[str, Callable[..., Any]], max_steps: int = 8):
		self.model = model
		self.tools = tools
		self.max_steps = max_steps

	def _format_messages(self, question: str, scratchpad: str) -> List[Dict[str, str]]:
		prompt = """
You are BioAgent, a strict ReAct agent. Always follow this I/O contract exactly:

Step protocol:
- Think silently and decide whether to use a tool.
- If using a tool, output a single line XML block:
  <tool_call>{"name": <tool-name>, "arguments": <json-args>}</tool_call>
  Wait for <tool_response> before continuing.
- Repeat at most {MAX_STEPS} steps.
- When you have the final answer, output ONLY:
  <final_answer>FINAL STRING ANSWER ONLY</final_answer>

Never output explanations outside these tags. Do not wrap with markdown. Keep the final answer concise.

Available tools:
- serper-search: {"q": string, "num": int}  → returns {"organic_results": [{"title","snippet","link"}]}
- crawl-page-summary: {"urls": [string]}    → returns {"summaries": [{"url","content"}]}

Example (abridged):
User Q: What is the capital of France?
<tool_call>{"name": "serper-search", "arguments": {"q": "capital of France", "num": 3}}</tool_call>
<tool_response>{"organic_results": [{"title": "Paris - Wikipedia", "link": "https://..."}]}</tool_response>
<final_answer>Paris</final_answer>

Your turn.
User Q:
{QUESTION}

Scratchpad:
{SCRATCHPAD}
""".strip().replace("{MAX_STEPS}", str(self.max_steps)).replace("{QUESTION}", question).replace("{SCRATCHPAD}", scratchpad)
		return [{"role": "user", "content": prompt}]

	async def arun(self, question: str) -> Dict[str, Any]:
		scratchpad = ""
		trajectory: List[Dict[str, Any]] = []
		final_answer = None
		for step in range(self.max_steps):
			messages = self._format_messages(question, scratchpad)
			content = await self.model.chat(messages)
			tool_m = TOOL_CALL_RE.search(content or "")
			final_m = FINAL_ANSWER_RE.search(content or "")
			if final_m:
				final_answer = final_m.group(1).strip()
				trajectory.append({"role": "assistant", "content": content})
				break
			if tool_m:
				try:
					call = json.loads(tool_m.group(1))
					name = call["name"]
					args = call.get("arguments", {})
					tool_fn = self.tools.get(name)
					if not tool_fn:
						raise KeyError(f"Unknown tool: {name}")
					result = await tool_fn(**args)
					obs = json.dumps(result, ensure_ascii=False)
					scratchpad += f"\n\n<tool_call>{json.dumps(call)}</tool_call>\n<tool_response>{obs}</tool_response>\n"
					trajectory.append({"role": "assistant", "content": content})
					trajectory.append({"role": "tool", "name": name, "content": obs})
					continue
				except Exception as e:
					scratchpad += f"\n\n<tool_response>{{\"error\": \"{str(e)}\"}}</tool_response>\n"
					trajectory.append({"role": "assistant", "content": content})
					trajectory.append({"role": "tool", "name": "error", "content": str(e)})
					continue
			# No tool and no final answer => stop
			trajectory.append({"role": "assistant", "content": content})
			break
		return {"final_answer": final_answer or "", "trajectory": trajectory}


