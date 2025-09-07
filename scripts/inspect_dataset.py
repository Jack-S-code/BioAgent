#!/usr/bin/env python
from typing import Optional
import typer
from datasets import load_dataset


app = typer.Typer()


@app.command()
def main(
	path: str = typer.Argument(...),
	subset: Optional[str] = typer.Option(None, help="HF subset/config name, e.g., CloningScenarios"),
	split: str = typer.Option("test"),
	rows: int = typer.Option(3, help="Show up to N example rows"),
):
	ds = load_dataset(path, subset, split=split)
	print("Columns:", ds.column_names)
	print("Total rows:", len(ds))
	print("\nExamples:")
	for i, ex in enumerate(ds):
		if i >= rows:
			break
		print({k: ex[k] for k in ds.column_names})


if __name__ == "__main__":
	app()


