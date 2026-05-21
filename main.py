#!/usr/bin/env python3
import sys
import io
import os
import argparse
from dotenv import load_dotenv
from orchestrator.workflow import WorkflowOrchestrator
from rich.console import Console
from rich.panel import Panel

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Workflow Orchestrator")
    parser.add_argument("--task", "-t", default="开发一个电商网站", help="任务描述")
    parser.add_argument("--model", "-m", default="gpt-4", help="使用的模型")
    
    args = parser.parse_args()
    
    console.print(Panel.fit(
        f"[bold cyan]多Agent工作流编排系统[/bold cyan]\n"
        f"任务: {args.task}",
        border_style="cyan"
    ))
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold yellow]Warning: 未设置 API_KEY，使用模拟模式[/bold yellow]")
    
    orchestrator = WorkflowOrchestrator(model=args.model)
    result = orchestrator.run_workflow(args.task)
    
    console.print("\n" + "="*50)
    orchestrator.print_summary(result)


if __name__ == "__main__":
    main()