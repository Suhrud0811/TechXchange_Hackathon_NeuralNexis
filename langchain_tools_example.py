#!/usr/bin/env python3
"""
Example of using LangChain tools with CrewAI agents
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LangChainToolsCrew:
    """Crew with LangChain tools integration"""

    def _get_watson_llm(self) -> LLM:
        """Configure and return IBM Watson LLM"""
        api_key = os.getenv("WATSONX_APIKEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        model = os.getenv("MODEL", "watsonx/meta-llama/llama-3-2-1b-instruct")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not api_key or not project_id:
            raise ValueError("WATSONX_APIKEY and WATSONX_PROJECT_ID are required")
        
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

    def create_agents_with_langchain_tools(self, topic: str):
        """Create agents with LangChain tools"""
        
        # Initialize LangChain tools
        search_tool = DuckDuckGoSearchRun()
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        
        # Create researcher agent with LangChain tools
        researcher = Agent(
            role=f"{topic} Senior Data Researcher",
            goal=f"Uncover cutting-edge developments in {topic}",
            backstory=f"You're a seasoned researcher with a knack for uncovering the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[search_tool, wikipedia_tool, SerperDevTool()]  # Multiple tools
        )
        
        # Create analyst agent
        analyst = Agent(
            role=f"{topic} Data Analyst",
            goal=f"Analyze and synthesize {topic} research findings",
            backstory=f"You're a meticulous analyst with expertise in {topic}. You excel at analyzing complex data and creating comprehensive reports.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[search_tool]  # Can use search for additional verification
        )
        
        return researcher, analyst

    def create_tasks(self, researcher: Agent, analyst: Agent, topic: str, current_year: str):
        """Create tasks for the crew"""
        
        research_task = Task(
            description=f"Conduct comprehensive research about {topic} using multiple sources. Use search tools to find the latest information from {current_year}. Focus on recent developments, trends, and breakthroughs.",
            expected_output=f"A detailed research summary with 10 key findings about {topic}, including recent developments from {current_year}.",
            agent=researcher
        )
        
        analysis_task = Task(
            description=f"Analyze the research findings about {topic}. Create a comprehensive report that includes market analysis, future trends, and potential applications. Use search tools to verify any claims or find additional supporting data.",
            expected_output=f"A comprehensive analysis report about {topic} with market insights, trends, and future predictions.",
            agent=analyst
        )
        
        return research_task, analysis_task

    def crew(self, topic: str, current_year: str = "2025") -> Crew:
        """Create and return the crew with LangChain tools"""
        researcher, analyst = self.create_agents_with_langchain_tools(topic)
        research_task, analysis_task = self.create_tasks(researcher, analyst, topic, current_year)
        
        return Crew(
            agents=[researcher, analyst],
            tasks=[research_task, analysis_task],
            process=Process.sequential,
            verbose=True,
        )

def main():
    """Example usage of LangChain tools with CrewAI"""
    print("🚀 LangChain Tools with CrewAI Example")
    
    # Create crew instance
    crew_instance = LangChainToolsCrew()
    
    # Test with a topic
    topic = "Artificial Intelligence Ethics"
    crew = crew_instance.crew(topic, "2025")
    
    # Execute the crew
    print(f"\n🧪 Testing with topic: {topic}")
    result = crew.kickoff()
    
    print(f"\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    main()
