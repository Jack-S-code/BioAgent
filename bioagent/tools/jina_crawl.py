import os
import re
import aiohttp
from typing import Dict, Any, List, Optional


class JinaCrawl:
	"""Wrapper for r.jina.ai reader with simple text return.

	Input: {"urls": [str], "web_search_query": str, "think_content": str}
	Output: {"summaries": [ {"url": str, "content": str} ]}
	"""

	def __init__(self, api_key: Optional[str] = None, timeout: int = 30, token_budget: int = 80000):
		self.api_key = api_key or os.getenv("JINA_API_KEY")
		if not self.api_key:
			raise ValueError("JINA_API_KEY not set")
		self.timeout = timeout
		self.token_budget = token_budget

	def _extract_url(self, s: str) -> Optional[str]:
		m = re.search(r"\((https?://[^\s)]+)\)", s)
		if m:
			return m.group(1)
		if s.startswith("http://") or s.startswith("https://"):
			return s
		m = re.search(r"(https?://[^\s]+)", s)
		return m.group(1) if m else None

	async def acrawl(self, urls: List[str]) -> Dict[str, Any]:
		processed: List[str] = []
		for u in urls:
			z = self._extract_url(u)
			if z:
				processed.append(z)
		if not processed:
			return {"summaries": []}
		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"X-Engine": "browser",
			"X-Return-Format": "text",
			"X-Token-Budget": str(self.token_budget),
		}
		results: List[Dict[str, str]] = []
		async with aiohttp.ClientSession() as session:
			for url in processed:
				jurl = f"https://r.jina.ai/{url}"
				try:
					async with session.get(jurl, headers=headers, timeout=self.timeout) as resp:
						text = await resp.text()
						results.append({"url": url, "content": text})
				except Exception as e:
					results.append({"url": url, "content": f"[error] {e}"})
		return {"summaries": results}


