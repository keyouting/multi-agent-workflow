from .base import BaseAgent, Task, TaskStatus
from typing import Dict, Any, List
import uuid


class PlannerAgent(BaseAgent):
    def __init__(self, name: str = "PlannerAgent", model: str = "gpt-4"):
        super().__init__(name, "planner", model)
    
    def execute_task(self, task: Task) -> Task:
        self.log(f"规划任务: {task.name}")
        
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        
        subtasks = self._decompose_task(task)
        
        task.result = f"任务已分解为 {len(subtasks)} 个子任务"
        task.status = TaskStatus.COMPLETED
        task.completed_at = task.completed_at or task.created_at
        
        self.task_history.append(task)
        self.add_message("assistant", f"任务分解完成: {len(subtasks)} 个子任务")
        
        return task, subtasks
    
    def _decompose_task(self, task: Task) -> List[Task]:
        description = task.description
        
        if "网站" in description or "web" in description.lower():
            subtasks = [
                Task(id=str(uuid.uuid4())[:8], name="需求分析", description="分析网站需求和功能规格", status=TaskStatus.PENDING),
                Task(id=str(uuid.uuid4())[:8], name="UI设计", description="设计网站页面布局和交互", status=TaskStatus.PENDING, dependencies=["需求分析"]),
                Task(id=str(uuid.uuid4())[:8], name="前端开发", description="实现网站前端页面", status=TaskStatus.PENDING, dependencies=["UI设计"]),
                Task(id=str(uuid.uuid4())[:8], name="后端开发", description="实现网站后端API和数据库", status=TaskStatus.PENDING, dependencies=["需求分析"]),
                Task(id=str(uuid.uuid4())[:8], name="测试部署", description="测试网站功能并部署上线", status=TaskStatus.PENDING, dependencies=["前端开发", "后端开发"])
            ]
        elif "数据分析" in description or "data" in description.lower():
            subtasks = [
                Task(id=str(uuid.uuid4())[:8], name="数据收集", description="收集并整理原始数据", status=TaskStatus.PENDING),
                Task(id=str(uuid.uuid4())[:8], name="数据清洗", description="清洗和处理缺失值、异常值", status=TaskStatus.PENDING, dependencies=["数据收集"]),
                Task(id=str(uuid.uuid4())[:8], name="数据分析", description="进行统计分析和建模", status=TaskStatus.PENDING, dependencies=["数据清洗"]),
                Task(id=str(uuid.uuid4())[:8], name="可视化", description="生成图表和可视化报告", status=TaskStatus.PENDING, dependencies=["数据分析"]),
                Task(id=str(uuid.uuid4())[:8], name="报告撰写", description="撰写数据分析报告", status=TaskStatus.PENDING, dependencies=["可视化"])
            ]
        else:
            subtasks = [
                Task(id=str(uuid.uuid4())[:8], name="需求分析", description="分析任务需求和目标", status=TaskStatus.PENDING),
                Task(id=str(uuid.uuid4())[:8], name="方案设计", description="设计实现方案", status=TaskStatus.PENDING, dependencies=["需求分析"]),
                Task(id=str(uuid.uuid4())[:8], name="任务执行", description="执行具体任务", status=TaskStatus.PENDING, dependencies=["方案设计"]),
                Task(id=str(uuid.uuid4())[:8], name="结果验证", description="验证任务结果", status=TaskStatus.PENDING, dependencies=["任务执行"])
            ]
        
        return subtasks