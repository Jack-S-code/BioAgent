from typing import Dict, Any, Optional
from openai import AsyncOpenAI


JUDGE_PROMPT = """
You are an impartial scientific evaluator. Determine if the model's answer correctly answers the question.

Return strictly one JSON object with fields:
{"ok": true|false, "reason": "short explanation"}

Criteria:
- Focus on factual correctness against the gold/reference answer. Allow synonyms, formatting and unit variants if equivalent.
- If the gold is a list of acceptable answers, any match is acceptable.
- Ignore extra commentary as long as the key answer is present and correct.
"""


class LLMJudge:
	def __init__(self, base_url: Optional[str], api_key: Optional[str], model: str, temperature: float = 0.0):
		self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
		self.model = model
		self.temperature = temperature

	async def ajudge(self, question: str, gold: Any, pred: str, trajectory: Any) -> Dict[str, Any]:
		user = f"Question: {question}\nGold/reference: {gold}\nModel answer: {pred}\n"
		resp = await self.client.chat.completions.create(
			model=self.model,
			messages=[{"role": "system", "content": JUDGE_PROMPT}, {"role": "user", "content": user}],
			temperature=self.temperature,
		)
		text = resp.choices[0].message.content or ""
		# very relaxed JSON parse: look for ok and reason
		ok = "true" in text.lower()
		return {"ok": ok, "raw": text}


