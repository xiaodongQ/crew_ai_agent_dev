from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
import os

# 设置DashScope API环境变量
os.environ['OPENAI_API_KEY'] = os.environ.get('LLM_API_KEY', '')
os.environ['OPENAI_BASE_URL'] = os.environ.get('LLM_API_BASE', 'https://coding.dashscope.aliyuncs.com/v1')

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TestCreateProject():
    """Technical Social Media Expert crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @property
    def llm_config(self):
        """Return LLM configuration from environment"""
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

    @agent
    def wechat_specialist(self) -> Agent:
        llm = self.llm_config if isinstance(self.llm_config, str) else self.llm_config
        return Agent(
            config=self.agents_config['wechat_specialist'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    @agent
    def xiaohongshu_specialist(self) -> Agent:
        llm = self.llm_config if isinstance(self.llm_config, str) else self.llm_config
        return Agent(
            config=self.agents_config['xiaohongshu_specialist'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    @agent
    def douyin_specialist(self) -> Agent:
        llm = self.llm_config if isinstance(self.llm_config, str) else self.llm_config
        return Agent(
            config=self.agents_config['douyin_specialist'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        llm = self.llm_config if isinstance(self.llm_config, str) else self.llm_config
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            llm=llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def wechat_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['wechat_strategy_task'], # type: ignore[index]
        )

    @task
    def xiaohongshu_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['xiaohongshu_strategy_task'], # type: ignore[index]
        )

    @task
    def douyin_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['douyin_strategy_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='social_media_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Technical Social Media Expert crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,  # 串行
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

