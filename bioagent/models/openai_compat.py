import os
from typing import List, Dict, Any
from openai import AsyncOpenAI
from typing import Optional


class OpenAIChatModel:
	"""OpenAI-compatible chat client with simple call() method.

	Expect the agent prompt to follow the tool-calling protocol described by the user.
	"""

	def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0, base_url: Optional[str] = None, api_key: Optional[str] = None):
		self.model = model
		self.temperature = temperature
		self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
		self.api_key = api_key or os.getenv("OPENAI_API_KEY")
		if not self.api_key:
			raise ValueError("OPENAI_API_KEY not set")
		self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

	async def chat(self, messages: List[Dict[str, str]], max_tokens: Optional[int] = None) -> str:
		resp = await self.client.chat.completions.create(
			model=self.model,
			messages=messages,
			temperature=self.temperature,
			max_tokens=max_tokens,
		)
		return resp.choices[0].message.content or ""


