# 修复 sqlite3 版本问题
import pysqlite3 as sqlite3
import sys
sys.modules['sqlite3'] = sqlite3

from dotenv import load_dotenv
import os

# 从 .env 文件加载环境变量
load_dotenv()

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

# ==================== 配置 LLM ====================
llm = LLM(
    model=os.getenv("LLM_MODEL", "openai/qwen3.5-plus"),
    api_key=os.getenv("LLM_API_KEY"),
    api_base=os.getenv("LLM_API_BASE"),
    temperature=0.7,
)

# ==================== 1. 定义 Agent ====================

# 研究员 Agent
researcher = Agent(
    role="技术研究员",
    goal="深入调研{topic}领域，找出关键信息和技术要点",
    backstory=(
        "你是一位经验丰富的技术研究员，拥有 10 年技术调研经验。"
        "你擅长从海量信息中筛选出最关键的内容，并用清晰的结构呈现。"
        "你特别关注技术的实用性、性能特点和适用场景。"
    ),
    llm=llm,  # 显式传递 LLM 配置
    verbose=True,
    allow_delegation=False
)

# ==================== 2. 定义 Task ====================
# 调研任务
research_task = Task(
    description=(
        "对{topic}进行彻底调研，重点关注：\n"
        "1. 核心概念和原理\n"
        "2. 主要特点和优势\n"
        "3. 典型使用场景\n"
        "4. 与其他技术的对比\n"
        "5. 学习资源和最佳实践\n\n"
        "确保信息准确、结构清晰，适合有 C++/Go 背景的开发者阅读。"
    ),
    expected_output=(
        "一份包含以下内容的调研报告：\n"
        "- 核心概念（5-7 个要点）\n"
        "- 技术特点（3-5 个要点）\n"
        "- 使用场景（3-5 个场景）\n"
        "- 对比分析（与 1-2 个类似技术对比）\n"
        "- 学习建议（3-5 条建议）"
    ),
    agent=researcher,
    output_file="output/research_report.md"  # 输出到文件
)

# ==================== 3. 创建 Crew ====================
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True,
    memory=False  # 禁用记忆功能（需要额外的 embedder 配置）
)

# ==================== 4. 执行 ====================
if __name__ == "__main__":
    print("🚀 启动 CrewAI 基础 Demo - 技术调研团队")
    print("=" * 50)

    # 传入主题参数
    inputs = {
        "topic": "Claude Code使用技巧"  # 可以改成任何你想调研的主题
    }

    print(f"📋 调研主题：{inputs['topic']}")
    print("=" * 50)
    print()

    # 启动执行
    result = crew.kickoff(inputs=inputs)
    print()
    print("=" * 50)
    print("✅ 任务完成！")
    print(f"\n📄 调研报告：output/research_report.md")
