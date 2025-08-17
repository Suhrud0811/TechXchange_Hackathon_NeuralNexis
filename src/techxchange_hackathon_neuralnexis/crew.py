# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""

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

    def create_agents(self, topic: str):
        """Create agents with the given topic"""
        researcher = Agent(
            role=f"{topic} Senior Data Researcher",
            goal=f"Uncover cutting-edge developments in {topic}",
            backstory=f"You're a seasoned researcher with a knack for uncovering the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[SerperDevTool()]
        )
        
        reporting_analyst = Agent(
            role=f"{topic} Reporting Analyst",
            goal=f"Create detailed reports based on {topic} data analysis and research findings",
            backstory=f"You're a meticulous analyst with a keen eye for detail. You're known for your ability to turn complex data into clear and concise reports, making it easy for others to understand and act on the information you provide.",
            llm=self._get_watson_llm(),
            verbose=True
        )
        
        return researcher, reporting_analyst

    def create_tasks(self, researcher: Agent, reporting_analyst: Agent, topic: str, current_year: str):
        """Create tasks with the given agents and parameters"""
        research_task = Task(
            description=f"Conduct a thorough research about {topic}. Make sure you find any interesting and relevant information given the current year is {current_year}.",
            expected_output=f"A list with 10 bullet points of the most relevant information about {topic}",
            agent=researcher
        )
        
        reporting_task = Task(
            description="Review the context you got and expand each topic into a full section for a report. Make sure the report is detailed and contains any and all relevant information.",
            expected_output="A fully fledged report with the main topics, each with a full section of information. Formatted as markdown without '```'",
            agent=reporting_analyst
        )
        
        return research_task, reporting_task

    def crew(self, topic: str, current_year: str) -> Crew:
        """Creates and returns the LatestAiDevelopment crew"""
        researcher, reporting_analyst = self.create_agents(topic)
        research_task, reporting_task = self.create_tasks(researcher, reporting_analyst, topic, current_year)
        
        return Crew(
            agents=[researcher, reporting_analyst],
            tasks=[research_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )