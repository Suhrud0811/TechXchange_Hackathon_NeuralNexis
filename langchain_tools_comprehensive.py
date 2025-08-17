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

    def create_research_agent(self, topic: str):
        """Create a research agent with multiple search tools"""
        
        # Initialize various LangChain tools
        search_tool = DuckDuckGoSearchRun()
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        youtube_tool = YouTubeSearchTool()
        
        # Note: Arxiv and PubMed might require additional setup
        # arxiv_tool = ArxivAPIWrapper()
        # pubmed_tool = PubmedQueryRun(api_wrapper=PubMedAPIWrapper())
        
        researcher = Agent(
            role=f"{topic} Research Specialist",
            goal=f"Conduct comprehensive research on {topic} using multiple sources",
            backstory=f"You're an expert researcher specializing in {topic}. You use multiple research tools to gather comprehensive information from web searches, Wikipedia, and video content.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[search_tool, wikipedia_tool, youtube_tool, SerperDevTool()]
        )
        
        return researcher

    def create_analysis_agent(self, topic: str):
        """Create an analysis agent with verification tools"""
        
        search_tool = DuckDuckGoSearchRun()
        
        analyst = Agent(
            role=f"{topic} Data Analyst",
            goal=f"Analyze and verify {topic} research findings",
            backstory=f"You're a data analyst with expertise in {topic}. You verify claims, cross-reference information, and create detailed analysis reports.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[search_tool]  # For verification purposes
        )
        
        return analyst

    def create_reporting_agent(self, topic: str):
        """Create a reporting agent for final synthesis"""
        
        reporter = Agent(
            role=f"{topic} Report Writer",
            goal=f"Create comprehensive reports on {topic}",
            backstory=f"You're a professional report writer specializing in {topic}. You synthesize research findings into clear, actionable reports.",
            llm=self._get_watson_llm(),
            verbose=True
        )
        
        return reporter

    def create_tasks(self, researcher: Agent, analyst: Agent, reporter: Agent, topic: str, current_year: str):
        """Create comprehensive tasks"""
        
        research_task = Task(
            description=f"""
            Conduct comprehensive research on {topic} using all available tools:
            1. Use web search to find the latest news and developments
            2. Check Wikipedia for foundational information
            3. Search YouTube for video content and presentations
            4. Focus on information from {current_year}
            
            Provide a detailed research summary with sources.
            """,
            expected_output=f"A comprehensive research summary on {topic} with multiple sources and recent developments from {current_year}.",
            agent=researcher
        )
        
        analysis_task = Task(
            description=f"""
            Analyze the research findings on {topic}:
            1. Verify key claims using search tools
            2. Identify trends and patterns
            3. Assess the credibility of sources
            4. Provide market analysis and future predictions
            """,
            expected_output=f"A detailed analysis report on {topic} with verified information, trends, and predictions.",
            agent=analyst
        )
        
        reporting_task = Task(
            description=f"""
            Create a final comprehensive report on {topic}:
            1. Synthesize research and analysis findings
            2. Create an executive summary
            3. Include actionable insights
            4. Format as a professional report
            """,
            expected_output=f"A professional report on {topic} with executive summary, key findings, and actionable insights.",
            agent=reporter
        )
        
        return research_task, analysis_task, reporting_task

    def crew(self, topic: str, current_year: str = "2025") -> Crew:
        """Create and return the comprehensive crew"""
        researcher = self.create_research_agent(topic)
        analyst = self.create_analysis_agent(topic)
        reporter = self.create_reporting_agent(topic)
        
        research_task, analysis_task, reporting_task = self.create_tasks(
            researcher, analyst, reporter, topic, current_year
        )
        
        return Crew(
            agents=[researcher, analyst, reporter],
            tasks=[research_task, analysis_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

def main():
    """Example usage of comprehensive LangChain tools with CrewAI"""
    print("🚀 Comprehensive LangChain Tools with CrewAI Example")
    
    # Create crew instance
    crew_instance = ComprehensiveLangChainCrew()
    
    # Test with a topic
    topic = "Machine Learning in Healthcare"
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
