#!/usr/bin/env python3
"""
CrewAI 并行执行演示

核心思路：
1. 调研任务先执行（串行）
2. 三个平台任务并行执行（asyncio.gather）
3. 汇总任务最后执行（依赖并行任务的结果）
"""

import os
import sys
import asyncio
from typing import List, Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

# 修复 sqlite3 问题
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
    sys.modules['sqlite3.dbapi2'] = pysqlite3.dbapi2
except ImportError:
    pass


@CrewBase
class ParallelDemo:
    """并行执行演示 - 多平台内容创作"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @property
    def llm_config(self):
        """返回 LLM 配置"""
        api_key = os.getenv("LLM_API_KEY")
        api_base = os.getenv("LLM_API_BASE")
        model = os.getenv("LLM_MODEL", "openai/qwen3.5-plus")
        
        if api_key and api_base:
            from crewai import LLM
            return LLM(
                model=model,
                api_key=api_key,
                base_url=api_base
            )
        return model

    # ============== Agents ==============

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=self.llm_config if isinstance(self.llm_config, str) else self.llm_config,
            verbose=True
        )

    @agent
    def wechat_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['wechat_specialist'],
            llm=self.llm_config if isinstance(self.llm_config, str) else self.llm_config,
            verbose=True
        )

    @agent
    def xiaohongshu_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['xiaohongshu_specialist'],
            llm=self.llm_config if isinstance(self.llm_config, str) else self.llm_config,
            verbose=True
        )

    @agent
    def douyin_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['douyin_specialist'],
            llm=self.llm_config if isinstance(self.llm_config, str) else self.llm_config,
            verbose=True
        )

    @agent
    def coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['coordinator'],
            llm=self.llm_config if isinstance(self.llm_config, str) else self.llm_config,
            verbose=True
        )

    # ============== Tasks ==============

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def wechat_task(self) -> Task:
        return Task(
            config=self.tasks_config['wechat_task'],
        )

    @task
    def xiaohongshu_task(self) -> Task:
        return Task(
            config=self.tasks_config['xiaohongshu_task'],
        )

    @task
    def douyin_task(self) -> Task:
        return Task(
            config=self.tasks_config['douyin_task'],
        )

    @task
    def coordinate_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordinate_task'],
            output_file='parallel_execution_report.md'
        )

    # ============== Crew ==============

    @crew
    def crew(self) -> Crew:
        """创建 Crew - 使用 sequential 流程"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
        )


# ============== 并行执行核心逻辑 ==============

async def execute_parallel_tasks(
    crew: Crew,
    research_result: Any,
    inputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    并行执行三个平台任务
    
    Args:
        crew: Crew 实例
        research_result: 调研任务的结果
        inputs: 输入参数
    
    Returns:
        三个任务的执行结果
    """
    
    # 获取三个平台任务
    wechat_task = next(t for t in crew.tasks if t.name == 'wechat_task')
    xiaohongshu_task = next(t for t in crew.tasks if t.name == 'xiaohongshu_task')
    douyin_task = next(t for t in crew.tasks if t.name == 'douyin_task')
    
    # 为每个任务设置上下文（调研结果）- context 需要是字符串
    for task in [wechat_task, xiaohongshu_task, douyin_task]:
        if research_result:
            # TaskStartedEvent 的 context 字段期望字符串类型
            task.context = str(research_result) if not isinstance(research_result, str) else research_result
        else:
            task.context = ""
    
    print("\n" + "="*60)
    print("🚀 开始并行执行三个平台任务...")
    print("="*60)
    
    # 创建并发执行函数
    async def run_task(task: Task) -> Any:
        """异步执行单个任务"""
        print(f"\n📝 开始执行：{task.name}")
        # 注意：CrewAI 的 task.execute 是同步的，需要用 run_in_executor
        # 使用默认参数捕获当前的 task 值，避免 lambda 闭包陷阱
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda t=task: t.execute_sync(context=t.context)
        )
        print(f"✅ 完成：{task.name}")
        return result
    
    # 并行执行三个任务
    results = await asyncio.gather(
        run_task(wechat_task),
        run_task(xiaohongshu_task),
        run_task(douyin_task),
        return_exceptions=True  # 捕获异常而不是抛出
    )
    
    return {
        'wechat': results[0],
        'xiaohongshu': results[1],
        'douyin': results[2]
    }


def run_parallel_demo(topic: str = "人工智能技术") -> Any:
    """
    运行并行执行演示
    
    执行流程：
    1. 调研任务（串行）
    2. 三个平台任务（并行）
    3. 汇总任务（串行）
    """
    
    print("\n" + "="*60)
    print("🎯 CrewAI 并行执行演示")
    print(f"📋 主题：{topic}")
    print("="*60)
    
    # 创建 Crew
    demo = ParallelDemo()
    crew = demo.crew()
    
    inputs = {'topic': topic}
    
    # ========== 阶段 1: 调研任务（串行）==========
    print("\n📚 阶段 1: 执行调研任务...")
    research_task = next(t for t in crew.tasks if t.name == 'research_task')
    research_result = research_task.execute_sync()
    print("✅ 调研完成")
    
    # ========== 阶段 2: 平台任务（并行）==========
    print("\n⚡ 阶段 2: 并行执行平台任务...")
    parallel_results = asyncio.run(
        execute_parallel_tasks(crew, research_result, inputs)
    )
    
    # 检查是否有异常
    for platform, result in parallel_results.items():
        if isinstance(result, Exception):
            print(f"⚠️  {platform} 任务执行失败：{result}")
        else:
            print(f"✅ {platform} 任务完成")
    
    # ========== 阶段 3: 汇总任务（串行）==========
    print("\n📊 阶段 3: 执行汇总任务...")
    coordinate_task = next(t for t in crew.tasks if t.name == 'coordinate_task')
    
    # 设置汇总任务的上下文（所有平台结果）- context 需要是字符串
    context_list = [v for v in parallel_results.values() if not isinstance(v, Exception)]
    if context_list:
        # 将所有结果合并为一个字符串作为上下文
        coordinate_task.context = "\n\n".join(str(r) if not isinstance(r, str) else r for r in context_list)
    else:
        coordinate_task.context = ""

    final_result = coordinate_task.execute_sync(context=coordinate_task.context)
    print("✅ 汇总完成")
    
    print("\n" + "="*60)
    print("🎉 并行执行演示完成！")
    print("="*60)
    print(f"📄 报告已保存：parallel_execution_report.md")
    
    return final_result


# ============== 入口 ==============

def run():
    """标准入口函数"""
    return run_parallel_demo("人工智能技术")


if __name__ == "__main__":
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else "人工智能技术"
    result = run_parallel_demo(topic)
    print(f"\n最终结果:\n{result}")
