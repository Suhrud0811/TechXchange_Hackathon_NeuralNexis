#!/usr/bin/env python3
"""
Comprehensive example of using various LangChain tools with CrewAI agents
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from langchain.tools import (
    DuckDuckGoSearchRun, 
    WikipediaQueryRun,
    YouTubeSearchTool
)
from langchain_community.utilities import (
    WikipediaAPIWrapper
)

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ComprehensiveLangChainCrew:
    """Crew with comprehensive LangChain tools integration"""

    def _get_bedrock_llm(self) -> LLM:
        """Configure and return AWS Bedrock LLM"""
        model = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        region = os.getenv("AWS_REGION", "us-east-1")
        
        # Configure Bedrock LLM
        bedrock_llm = LLM(
            model=model,
            config={
                "region_name": region,
                "temperature": 0.7,
                "max_tokens": 512,
                "top_p": 0.9,
                "top_k": 50,
                "stop_sequences": []
            }
        )
        
        return bedrock_llm

    def create_reporting_agent(self, topic: str):
        """Create a reporting agent for final synthesis"""
        
        reporter = Agent(
            role=f"{topic} Report Writer",
            goal=f"Create comprehensive reports on {topic}",
            backstory=f"You're a professional report writer specializing in {topic}. You synthesize research findings into clear, actionable reports.",
            llm=self._get_bedrock_llm(),
            verbose=True
        )
        
        return reporter

    def create_requirements_agent(self):
        """Create a requirements agent for final synthesis"""
        
        requirements_agent = Agent(
            role=f"Requirements Agent",
            goal=f"Gather requirements from the user about the goals they want to achieve.",
            backstory=f"You're a professional Therapist/Goal Planner. \
                        You gather requirements from the user about the goals they want to achieve.",
            llm=self._get_bedrock_llm(),
            verbose=True
        )
        
        return requirements_agent

    def create_behaivor_analyzer_agent(self):
        """Create a behavior analyzer agent for final synthesis"""
        
        behavior_analyzer_agent = Agent(
            role=f"Behavior Analyzer Agent",
            goal=f"Analyze the conversation this specific user and gauge if they have any mental health challenges or issues.",
            backstory=f"You're a professional Therapist/Goal Planner. \
                        You analyze the conversation this specific user has had with you \
                        and gauge if they have any mental health challenges or issues.",
            llm=self._get_bedrock_llm(),
            verbose=True        
            )
        
        return behavior_analyzer_agent

    def create_research_agent(self):
        """Create a research agent with multiple search tools"""
        
        # Initialize various LangChain tools
        search_tool = DuckDuckGoSearchRun()
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        youtube_tool = YouTubeSearchTool()
        
        researcher = Agent(
            role=f"Research Specialist",
            goal=f"Conduct comprehensive research on the user's goals and requirements using multiple sources",
            backstory=f"You use multiple research tools to gather comprehensive information from web searches, \
                        Wikipedia, and video content to help the user achieve their goals and requirements with \
                        their mental health challenges or issues.",
            llm=self._get_bedrock_llm(),
            verbose=True,
            tools=[search_tool, wikipedia_tool, youtube_tool, SerperDevTool()]
        )
        
        return researcher

    def create_task_analyzer_agent(self):
        """Create a task analyzer agent for final synthesis"""
        
        task_analyzer_agent = Agent(
            role=f"Task Analyzer Agent",
            goal=f"Analyze the requirements and create a list of tasks that need to be completed to achieve the goals.",
            backstory=f"You're a professional Therapist/Goal Planner. \
                        You analyze the requirements and create a list of tasks that need to be completed to achieve the goals.",
            llm=self._get_bedrock_llm(),
            verbose=True,  
        )
        
        return task_analyzer_agent


    def create_tasks(self, requirements_agent: Agent, behavior_analyzer: Agent, researcher: Agent, task_analyzer: Agent, reporter: Agent):
        """Create comprehensive tasks with proper context flow between agents"""
        
        # Task 1: Gather requirements from user (no context - this is the starting point)
        requirements_task = Task(
            description="""
            Gather requirements from the user about their goals and what they want to achieve.
            Ask clarifying questions if needed to understand their specific needs and objectives.
            """,
            expected_output="A clear summary of the user's goals and requirements.",
            agent=requirements_agent
        )
        
        # Task 2: Analyze user behavior and mental health (uses output from requirements task)
        behavior_analysis_task = Task(
            description="""
            Analyze the user's conversation and requirements to identify any potential mental health challenges or issues.
            Use the requirements gathered to understand the user's context and needs.
            """,
            expected_output="An analysis of the user's mental health status and any challenges identified.",
            agent=behavior_analyzer,
            context=[requirements_task]  # This agent receives input from requirements_task
        )
        
        # Task 3: Research solutions (uses output from both previous tasks)
        research_task = Task(
            description="""
            Conduct comprehensive research based on the user's requirements and mental health analysis.
            Find relevant information, resources, and solutions that can help the user achieve their goals.
            """,
            expected_output="A comprehensive research report with relevant resources and solutions.",
            agent=researcher,
            context=[requirements_task, behavior_analysis_task]  # Uses output from both previous tasks
        )
        
        # Task 4: Create task breakdown (uses output from all previous tasks)
        task_analysis_task = Task(
            description="""
            Based on the requirements, behavior analysis, and research findings, create a detailed list of tasks
            that need to be completed to help the user achieve their goals.
            """,
            expected_output="A prioritized list of tasks with clear steps to achieve the user's goals.",
            agent=task_analyzer,
            context=[requirements_task, behavior_analysis_task, research_task]  # Uses all previous outputs
        )
        
        # Task 5: Final report (uses output from all previous tasks)
        reporting_task = Task(
            description="""
            Create a final comprehensive report that synthesizes all the information gathered:
            1. User requirements and goals
            2. Mental health analysis and considerations
            3. Research findings and resources
            4. Detailed action plan with tasks
            5. Recommendations and next steps
            """,
            expected_output="A comprehensive report with all findings, analysis, and actionable recommendations.",
            agent=reporter,
            context=[requirements_task, behavior_analysis_task, research_task, task_analysis_task]  # Uses all outputs
        )
        
        return requirements_task, behavior_analysis_task, research_task, task_analysis_task, reporting_task

    def crew(self) -> Crew:
        """Create and return the comprehensive crew"""
        # Create all agents
        requirements_agent = self.create_requirements_agent()
        behavior_analyzer = self.create_behaivor_analyzer_agent()
        researcher = self.create_research_agent()
        task_analyzer = self.create_task_analyzer_agent()
        reporter = self.create_reporting_agent("Mental Health Support")
        
        # Create tasks with proper context flow
        requirements_task, behavior_analysis_task, research_task, task_analysis_task, reporting_task = self.create_tasks(
            requirements_agent, behavior_analyzer, researcher, task_analyzer, reporter)
        
        return Crew(
            agents=[requirements_agent, behavior_analyzer, researcher, task_analyzer, reporter],
            tasks=[requirements_task, behavior_analysis_task, research_task, task_analysis_task, reporting_task],
            process=Process.sequential,
            verbose=True,)

def main():
    """Example usage of comprehensive LangChain tools with CrewAI"""
    print("🚀 Mental Health Support Crew with LangChain Tools")
    
    # Create crew instance
    crew_instance = ComprehensiveLangChainCrew()
    
    # Create the crew
    crew = crew_instance.crew()
    
    # Execute the crew
    print(f"\n🧪 Starting Mental Health Support Process...")
    result = crew.kickoff()
    
    print(f"\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    main()
