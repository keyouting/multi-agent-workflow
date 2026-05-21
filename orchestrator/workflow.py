from agents.base import BaseAgent, Task, TaskStatus
from agents.planner_agent import PlannerAgent
from agents.worker_agents import ResearcherAgent, CoderAgent, ReviewerAgent, TesterAgent
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from rich.console import Console
from rich.table import Table


@dataclass
class WorkflowResult:
    workflow_name: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    duration: float
    task_details: List[Dict[str, Any]]


class WorkflowOrchestrator:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.console = Console()
        
        self.planner = PlannerAgent(model)
        self.researcher = ResearcherAgent(model)
        self.coder = CoderAgent(model)
        self.reviewer = ReviewerAgent(model)
        self.tester = TesterAgent(model)
        
        self.agents = {
            "researcher": self.researcher,
            "coder": self.coder,
            "reviewer": self.reviewer,
            "tester": self.tester
        }
        
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
    
    def run_workflow(self, task_description: str) -> WorkflowResult:
        self.console.print("[bold cyan]=== 开始多Agent工作流编排 ===[/bold cyan]\n")
        
        start_time = datetime.now()
        
        main_task = Task(
            id="main-001",
            name="主任务",
            description=task_description
        )
        
        self.console.print(f"[bold yellow]任务: {task_description}[/bold yellow]\n")
        
        self.console.print("[bold]Step 1: PlannerAgent 任务分解[/bold]")
        result, subtasks = self.planner.execute_task(main_task)
        self.console.print(f"  -> 分解为 {len(subtasks)} 个子任务\n")
        
        self.task_queue = subtasks
        
        self.console.print("[bold]Step 2: 多Agent协作执行[/bold]")
        
        completed = []
        failed = []
        
        while self.task_queue:
            task = self.task_queue.pop(0)
            
            deps_met = all(
                any(c.name == dep for c in completed)
                for dep in task.dependencies
            )
            
            if not deps_met:
                self.task_queue.append(task)
                continue
            
            agent = self._select_agent(task)
            self.console.print(f"  [{agent.role}] 执行: {task.name}")
            
            try:
                result = agent.execute_task(task)
                completed.append(result)
                self.console.print(f"    -> 完成\n")
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = str(e)
                failed.append(task)
                self.console.print(f"    -> 失败: {e}\n")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        
        self.console.print(f"\n[bold green]工作流执行完成! 耗时: {elapsed:.2f}s[/bold green]")
        
        return WorkflowResult(
            workflow_name=task_description,
            total_tasks=len(subtasks),
            completed_tasks=len(completed),
            failed_tasks=len(failed),
            duration=elapsed,
            task_details=[self._task_to_dict(t) for t in completed + failed]
        )
    
    def _select_agent(self, task: Task) -> BaseAgent:
        name = task.name.lower()
        
        if "研究" in name or "分析" in name or "research" in name:
            return self.researcher
        elif "开发" in name or "编码" in name or "code" in name:
            return self.coder
        elif "测试" in name or "test" in name:
            return self.tester
        elif "审查" in name or "review" in name:
            return self.reviewer
        elif "设计" in name or "design" in name:
            return self.researcher
        else:
            return self.researcher
    
    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "agent": task.assigned_agent,
            "result": task.result[:100] if task.result else None
        }
    
    def print_summary(self, result: WorkflowResult):
        table = Table(title="工作流执行报告")
        table.add_column("任务", style="cyan")
        table.add_column("Agent", style="green")
        table.add_column("状态", style="yellow")
        
        for task in result.task_details:
            table.add_row(
                task["name"],
                task["agent"] or "-",
                task["status"]
            )
        
        self.console.print(table)
        self.console.print(f"\n总计: {result.completed_tasks} 完成, {result.failed_tasks} 失败")