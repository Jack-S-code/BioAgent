#!/usr/bin/env python
import asyncio
import os
import sys
import typing
import typer

# Ensure project root is on sys.path when running from scripts/
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from bioagent.models import OpenAIChatModel
from bioagent.agent.react import ReActAgent
from bioagent.tools import SerperSearch, JinaCrawl
from bioagent.datasets import HFDataset
from bioagent.eval.runner import EvalRunner
from bioagent.eval.judge import LLMJudge


app = typer.Typer()


@app.command()
def main(
	dataset: str = typer.Option("hf", help="Dataset type"),
	hf_path: str = typer.Option(..., help="HF dataset path"),
	split: str = typer.Option("test", help="HF split"),
	question_field: str = typer.Option("question", help="Question field name"),
	answer_field: str = typer.Option("answer", help="Answer field name"),
	subset: typing.Optional[str] = typer.Option(None, help="HF subset/config name"),
	limit: typing.Optional[int] = typer.Option(10, help="Max samples (None for all)"),
	model: str = typer.Option("openai"),
	model_name: str = typer.Option("gpt-4o-mini"),
	temperature: float = typer.Option(0.0),
	max_steps: int = typer.Option(6),
	out_dir: str = typer.Option("runs/demo"),
	openai_base_url: typing.Optional[str] = typer.Option(None, help="Override OpenAI-compatible base URL, e.g. http://host:port/v1"),
	openai_api_key: typing.Optional[str] = typer.Option(None, help="API key for OpenAI-compatible server"),
	judge: bool = typer.Option(False, help="Enable LLM-as-a-Judge scoring when exact match fails"),
	judge_model: str = typer.Option("kimi-k2-turbo-preview", help="Judge model name on the same API"),
	forced_choice: bool = typer.Option(False, help="If options exist, force model to choose one option"),
):
	if dataset != "hf":
		raise typer.BadParameter("Only 'hf' dataset type is supported in this scaffold")
	data = HFDataset(hf_path, split=split, question_field=question_field, answer_field=answer_field, subset=subset)

	if model != "openai":
		raise typer.BadParameter("Only 'openai' model is scaffolded")
	mdl = OpenAIChatModel(model=model_name, temperature=temperature, base_url=openai_base_url, api_key=openai_api_key)

	search = SerperSearch()
	crawl = JinaCrawl()

	async def tool_serper_search(q: str, num: int = 10):
		return await search.asearch(q=q, num=num)

	async def tool_crawl_page_summary(urls: list[str], web_search_query: str = "", think_content: str = ""):
		return await crawl.acrawl(urls=urls)

	agent = ReActAgent(
		model=mdl,
		tools={
			"serper-search": tool_serper_search,
			"crawl-page-summary": tool_crawl_page_summary,
		},
		max_steps=max_steps,
	)

	judge_client = LLMJudge(openai_base_url, openai_api_key, judge_model) if judge else None
	runner = EvalRunner(agent=agent, dataset=data, out_dir=out_dir, judge=judge_client, forced_choice=forced_choice)
	metrics = asyncio.run(runner.arun(limit=limit))
	print(metrics)


if __name__ == "__main__":
	app()


