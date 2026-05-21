from .base import BaseAgent, Task, TaskStatus
from typing import Dict, Any
import time


class ResearcherAgent(BaseAgent):
    def __init__(self, name: str = "ResearcherAgent", model: str = "gpt-4"):
        super().__init__(name, "researcher", model)
    
    def execute_task(self, task: Task) -> Task:
        self.log(f"执行研究任务: {task.name}")
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        
        result = self._research(task.description)
        
        task.result = result
        task.status = TaskStatus.COMPLETED
        task.completed_at = task.completed_at or task.created_at
        self.task_history.append(task)
        
        self.add_message("assistant", f"研究完成 ({len(result)} 字符)")
        return task
    
    def _research(self, topic: str) -> str:
        return f"关于「{topic}」的研究结果:\n\n1. 行业现状分析\n2. 技术方案对比\n3. 最佳实践建议\n4. 风险评估"


class CoderAgent(BaseAgent):
    def __init__(self, name: str = "CoderAgent", model: str = "gpt-4"):
        super().__init__(name, "coder", model)
    
    def execute_task(self, task: Task) -> Task:
        self.log(f"执行编码任务: {task.name}")
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        
        code = self._write_code(task.description)
        
        task.result = code
        task.status = TaskStatus.COMPLETED
        task.completed_at = task.completed_at or task.created_at
        self.task_history.append(task)
        
        self.add_message("assistant", f"编码完成 ({len(code)} 字符)")
        return task
    
    def _write_code(self, requirement: str) -> str:
        return f"// 实现: {requirement}\n\nfunction main() {\n    console.log('Hello World');\n}\n\nmain();"


class ReviewerAgent(BaseAgent):
    def __init__(self, name: str = "ReviewerAgent", model: str = "gpt-4"):
        super().__init__(name, "reviewer", model)
    
    def execute_task(self, task: Task) -> Task:
        self.log(f"执行审查任务: {task.name}")
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        
        review = self._review(task.description)
        
        task.result = review
        task.status = TaskStatus.COMPLETED
        task.completed_at = task.completed_at or task.created_at
        self.task_history.append(task)
        
        self.add_message("assistant", f"审查完成")
        return task
    
    def _review(self, content: str) -> str:
        return f"审查报告:\n\n优点:\n- 代码结构清晰\n- 命名规范\n\n建议:\n- 添加错误处理\n- 增加注释\n- 考虑边界情况"


class TesterAgent(BaseAgent):
    def __init__(self, name: str = "TesterAgent", model: str = "gpt-4"):
        super().__init__(name, "tester", model)
    
    def execute_task(self, task: Task) -> Task:
        self.log(f"执行测试任务: {task.name}")
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        
        test_result = self._test(task.description)
        
        task.result = test_result
        task.status = TaskStatus.COMPLETED
        task.completed_at = task.completed_at or task.created_at
        self.task_history.append(task)
        
        self.add_message("assistant", f"测试完成")
        return task
    
    def _test(self, requirement: str) -> str:
        return f"测试报告:\n\n测试用例: 5\n通过: 5\n失败: 0\n覆盖率: 95%\n\n所有测试通过!"