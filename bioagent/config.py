import os
import re
import time
import json
import string
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RunConfig:
	model: str = "openai"
	model_name: str = "gpt-4o-mini"
	temperature: float = 0.0
	max_steps: int = 8
	step_timeout: int = 120
	answer_timeout: int = 300


def now_ms() -> int:
	return int(time.time() * 1000)


def normalize_text(text: str) -> str:
	if text is None:
		return ""
	text = text.strip().lower()
	text = re.sub(r"\s+", " ", text)
	text = text.translate(str.maketrans("", "", string.punctuation))
	return text


def exact_match(pred: Any, gold: Any) -> bool:
	pred_s = normalize_text(str(pred))
	if isinstance(gold, list):
		return any(pred_s == normalize_text(str(g)) for g in gold)
	return pred_s == normalize_text(str(gold))


def dump_json(path: str, data: Dict[str, Any]):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


