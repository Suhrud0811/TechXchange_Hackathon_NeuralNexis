from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from techxchange_hackathon_neuralnexis.tools.custom_tool import SerpAPISearchTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class TechxchangeHackathonNeuralnexis():
    """TechxchangeHackathonNeuralnexis crew"""

    agents = List[BaseAgent]
    tasks = List[Task]

    def _get_watson_llm(self) -> LLM:
        """Configure and return IBM Watson LLM"""
        api_key = os.getenv("WATSONX_APIKEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        model = os.getenv("MODEL", "watsonx/meta-llama/llama-3-2-1b-instruct")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not api_key or not project_id:
            raise ValueError("WATSONX_APIKEY and WATSONX_PROJECT_ID are required")
        
        # Configure Watson LLM
        watson_llm = LLM(
            model=model,
            config={
                "api_key": api_key,
                "project_id": project_id,
                "url": url,
                "temperature": 0.7,
                "max_tokens": 512,
                "top_p": 0.9,
                "top_k": 50,
                "repetition_penalty": 1.1
            }
        )
        
        return watson_llm

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def goal_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['GoalPlannerAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            tools=[SerpAPISearchTool()],
            verbose=True
        )

    @agent
    def time_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['TimeAnalyzerAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            verbose=True
        )

    @agent
    def impact_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ImpactAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            verbose=True
        )

    @agent
    def prioritizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['PrioritizerAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            verbose=True
        )

    @agent
    def scheduler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['SchedulerAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            verbose=True
        )

    @agent
    def monitor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['MonitorAgent'], # type: ignore[index]
            llm=self._get_watson_llm(),
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def plan_goal_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_goal'], # type: ignore[index]
        )

    @task
    def estimate_time_task(self) -> Task:
        return Task(
            config=self.tasks_config['estimate_time'], # type: ignore[index]
        )

    @task
    def assign_impact_task(self) -> Task:
        return Task(
            config=self.tasks_config['assign_impact'], # type: ignore[index]
        )

    @task
    def prioritize_task(self) -> Task:
        return Task(
            config=self.tasks_config['prioritize'], # type: ignore[index]
        )

    @task
    def schedule_task(self) -> Task:
        return Task(
            config=self.tasks_config['schedule'], # type: ignore[index]
        )

    @task
    def monitor_task(self) -> Task:
        return Task(
            config=self.tasks_config['monitor'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TechxchangeHackathonNeuralnexis crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
