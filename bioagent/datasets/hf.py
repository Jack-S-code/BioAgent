from typing import Iterator, Dict, Any, Optional, Tuple
from datasets import load_dataset


class HFDataset:
	"""Thin adapter around HuggingFace datasets.

	Parameters map to fields in the dataset: question and answer.
	"""

	def __init__(self, path: str, split: str = "test", question_field: str = "question", answer_field: str = "answer", subset: Optional[str] = None):
		self.path = path
		self.subset = subset
		self.split = split
		self.qf = question_field
		self.af = answer_field
		self.ds = load_dataset(path, subset, split=split)

		# Auto-detect Q/A fields if provided names are missing
		cols = list(self.ds.column_names)
		if (self.qf not in cols) or (self.af not in cols):
			qf, af = self._auto_detect_fields(cols)
			self.qf = qf or self.qf
			self.af = af or self.af

	def __len__(self) -> int:
		return len(self.ds)

	def iter(self, limit: Optional[int] = None) -> Iterator[Dict[str, Any]]:
		count = 0
		for ex in self.ds:
			item: Dict[str, Any] = {
				"id": ex.get("id") or count,
				"question": ex[self.qf],
				"answer": ex[self.af],
			}
			# Provide multiple-choice options to the agent when available
			if "distractors" in self.ds.column_names:
				try:
					distractors = ex.get("distractors") or []
					if isinstance(distractors, list):
						options = list(distractors) + [ex[self.af]]
						item["options"] = options
				except Exception:
					pass
			yield item
			count += 1
			if limit and count >= limit:
				break

	@staticmethod
	def _auto_detect_fields(cols: list[str]) -> Tuple[Optional[str], Optional[str]]:
		candidates_q = [
			"question", "prompt", "query", "input", "problem", "instruction",
		]
		candidates_a = [
			"answer", "output", "label", "target", "gold", "final_answer", "ideal",
		]
		q = next((c for c in candidates_q if c in cols), None)
		a = next((c for c in candidates_a if c in cols), None)
		return q, a


