# Multi-Agent Workflow Orchestrator

多Agent工作流编排系统 - 任务分解 + 多Agent协作 + 状态管理

## 核心特性

- **智能任务分解**: PlannerAgent自动将复杂任务分解为可执行的子任务
- **多Agent协作**: ResearcherAgent、CoderAgent、ReviewerAgent、TesterAgent协同工作
- **依赖管理**: 自动处理任务依赖关系，确保执行顺序正确
- **状态追踪**: 完整的任务状态管理和执行报告

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行默认任务
python main.py

# 指定任务
python main.py -t "开发一个数据分析平台"
```

## 架构

```
├── agents/              # Agent模块
│   ├── base.py          # 基础Agent类
│   ├── planner_agent.py # 任务规划Agent
│   └── worker_agents.py # 执行Agent集合
├── orchestrator/        # 工作流编排
│   └── workflow.py      # 工作流引擎
└── main.py
```

## 工作流流程

1. **PlannerAgent**: 接收任务 → 智能分解 → 生成子任务列表
2. **依赖检查**: 检查任务依赖关系 → 确定执行顺序
3. **Agent分配**: 根据任务类型自动分配最合适的Agent
4. **并行执行**: 多个Agent协作执行子任务
5. **结果汇总**: 生成完整的工作流执行报告

## 支持的Agent角色

- **PlannerAgent**: 任务规划和分解
- **ResearcherAgent**: 需求分析和方案设计
- **CoderAgent**: 代码编写和实现
- **ReviewerAgent**: 代码审查和质量检查
- **TesterAgent**: 测试验证和报告

## License

MIT