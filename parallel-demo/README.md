# Parallel Demo - CrewAI 并行执行演示

一个展示 CrewAI 框架中**并行执行任务**能力的演示项目，模拟多平台内容创作的协同工作流。

## 项目概述

本项目演示如何在 CrewAI 中实现并行任务执行：

1. **调研任务**（串行）- 先执行技术主题调研
2. **平台任务**（并行）- 微信、小红书、抖音三个平台内容同时生成
3. **汇总任务**（串行）- 整合所有平台方案，生成统一执行报告

## 核心特性

- **并行执行** - 使用 `asyncio.gather()` 并发执行多个平台任务
- **多平台适配** - 针对不同平台特性定制内容风格
- **模块化设计** - Agent、Task、Crew 分离，易于扩展
- **环境隔离** - 支持自定义 LLM API 配置

## 技术栈

- Python >= 3.10
- [CrewAI](https://crewai.com) - Agent 编排框架
- asyncio - 异步并发执行

## 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置 LLM API：

```bash
# 阿里云百炼 - 通义千问
LLM_API_KEY=your-api-key-here
LLM_API_BASE=https://coding.dashscope.aliyuncs.com/v1
LLM_MODEL=openai/qwen3.5-plus

# 可选：Serper 搜索 API
# SERPER_API_KEY=your-serper-api-key
```

### 3. 运行演示

```bash
# 默认主题：人工智能技术
python -m parallel_demo.main

# 自定义主题
python -m parallel_demo.main "Python 编程入门"
python -m parallel_demo.main "量子计算基础"
```

## 项目结构

```
parallel-demo/
├── src/parallel_demo/
│   ├── __init__.py
│   ├── main.py              # 主入口，环境变量加载
│   ├── crew.py              # Crew 定义，并行执行核心逻辑
│   └── config/
│       ├── agents.yaml      # 5 个 Agent 角色配置
│       └── tasks.yaml       # 5 个任务配置
├── pyproject.toml           # 项目依赖定义
├── .env.example             # 环境变量模板
└── README.md                # 本文档
```

## Agent 角色

| Agent | 职责 |
|-------|------|
| `researcher` | 技术内容研究员，负责主题调研 |
| `wechat_specialist` | 微信文章创作专家 |
| `xiaohongshu_specialist` | 小红书图文笔记专家 |
| `douyin_specialist` | 抖音短视频脚本专家 |
| `coordinator` | 内容协调分析师，整合各平台策略 |

## 执行流程

```
┌─────────────────┐
│  调研任务        │  ← 串行执行
│  (research)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  并行执行 (asyncio.gather)      │
│  ┌──────────┬──────────┬──────┐ │
│  │ 微信     │ 小红书    │ 抖音  │ │  ← 同时执行
│  │ task     │ task     │ task │ │
│  └──────────┴──────────┴──────┘ │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  汇总任务                        │  ← 串行执行
│  (coordinate)                   │
│  生成统一执行报告                │
└─────────────────────────────────┘
```

## 输出

执行完成后，会生成 `parallel_execution_report.md` 文件，包含：

- 各平台内容策略对比分析
- 可复用核心素材清单
- 跨平台协同运营建议
- 一周发布时间表

## 自定义扩展

### 添加新平台

1. 在 `config/agents.yaml` 中添加新 Agent 配置
2. 在 `config/tasks.yaml` 中添加新任务配置
3. 在 `crew.py` 中添加对应的 `@agent` 和 `@task` 装饰器
4. 在 `execute_parallel_tasks()` 中添加新任务到并行执行列表

### 修改执行策略

修改 `crew.py` 中的 `execute_parallel_tasks()` 函数，调整并发逻辑。

## 注意事项

- 确保已配置有效的 LLM API 密钥
- 并行执行时，各平台任务共享调研结果作为上下文
- 如遇 sqlite3 相关错误，项目会自动使用 `pysqlite3` 替代

## 许可证

MIT License
