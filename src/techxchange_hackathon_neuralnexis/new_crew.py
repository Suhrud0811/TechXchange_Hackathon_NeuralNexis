from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class PlanningCrew:
    """A crew designed to break down a goal into a scheduled and monitored plan."""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    watson_llm = LLM(
        model="watsonx/meta-llama/llama-3-2-1b-instruct",
        api_key=os.getenv("WATSONX_API_KEY"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        api_base=os.getenv("WATSONX_URL")
    )

    # --- Agent Definitions ---
    @agent
    def goal_planner_agent(self) -> Agent:
        return Agent(config=self.agents_config['GoalPlannerAgent'], verbose=True, llm=self.watson_llm)

    @agent
    def time_analyzer_agent(self) -> Agent:
        return Agent(config=self.agents_config['TimeAnalyzerAgent'], verbose=True, llm=self.watson_llm)

    @agent
    def impact_agent(self) -> Agent:
        return Agent(config=self.agents_config['ImpactAgent'], verbose=True, llm=self.watson_llm)

    @agent
    def prioritizer_agent(self) -> Agent:
        return Agent(config=self.agents_config['PrioritizerAgent'], verbose=True, llm=self.watson_llm)

    @agent
    def scheduler_agent(self) -> Agent:
        return Agent(config=self.agents_config['SchedulerAgent'], verbose=True, llm=self.watson_llm)

    @agent
    def monitor_agent(self) -> Agent:
        return Agent(config=self.agents_config['MonitorAgent'], verbose=True, llm=self.watson_llm)

    # --- Task Definitions ---
    @task
    def plan_goal_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_goal_task'],
            agent=self.goal_planner_agent()
        )

    @task
    def estimate_time_task(self) -> Task:
        return Task(
            config=self.tasks_config['estimate_time_task'],
            agent=self.time_analyzer_agent(),
            context=[self.plan_goal_task()]
        )

    @task
    def assign_impact_task(self) -> Task:
        return Task(
            config=self.tasks_config['assign_impact_task'],
            agent=self.impact_agent(),
            context=[self.estimate_time_task()]
        )

    @task
    def prioritize_task(self) -> Task:
        return Task(
            config=self.tasks_config['prioritize_task'],
            agent=self.prioritizer_agent(),
            context=[self.assign_impact_task()]
        )

    @task
    def schedule_task(self) -> Task:
        return Task(
            config=self.tasks_config['schedule_task'],
            agent=self.scheduler_agent(),
            context=[self.prioritize_task()]
        )

    @task
    def monitor_task(self) -> Task:
        return Task(
            config=self.tasks_config['monitor_task'],
            agent=self.monitor_agent(),
            context=[self.schedule_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates and configures the planning crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )