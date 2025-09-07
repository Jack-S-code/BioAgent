import os
import json
import httpx
from typing import Dict, Any, List, Optional


class SerperSearch:
	"""Lightweight wrapper for google.serper.dev.

	Usage contract for the ReAct loop:
	- Input: {"q": str, "num": int}
	- Output: {"organic_results": [{"title": str, "snippet": str, "link": str}]}
	"""

	def __init__(self, api_key: Optional[str] = None, timeout: int = 60):
		self.api_key = api_key or os.getenv("SERPER_API_KEY")
		if not self.api_key:
			raise ValueError("SERPER_API_KEY not set")
		self.timeout = timeout

	async def asearch(self, q: str, num: int = 10) -> Dict[str, Any]:
		headers = {
			"Content-Type": "application/json",
			"X-API-KEY": self.api_key,
		}
		payload = {"q": q, "num": num, "autocorrect": False}
		async with httpx.AsyncClient() as client:
			resp = await client.post(
				"https://google.serper.dev/search",
				json=payload,
				headers=headers,
				timeout=self.timeout,
			)
			resp.raise_for_status()
			data = resp.json()
			organic = data.get("organic") or data.get("organic_results") or []
			results: List[Dict[str, Any]] = []
			for item in organic[:num]:
				results.append(
					{
						"title": item.get("title"),
						"snippet": item.get("snippet") or item.get("description"),
						"link": item.get("link") or item.get("url"),
					}
				)
			return {"organic_results": results}


