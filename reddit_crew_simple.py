#!/usr/bin/env python3
"""
Simplified Reddit Crew Example - Works with existing Reddit tool
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from reddit_tool import RedditSearchTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleRedditCrew:
    """Simplified crew for analyzing Reddit content"""

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

    def create_agents(self, topic: str):
        """Create agents with Reddit tool"""
        
        # Reddit Research Agent
        reddit_researcher = Agent(
            role=f"{topic} Reddit Research Specialist",
            goal=f"Analyze Reddit discussions and trends related to {topic}",
            backstory=f"You're a social media research specialist who excels at analyzing Reddit discussions about {topic}. You understand community sentiment, trending topics, and can identify key insights from user discussions.",
            llm=self._get_watson_llm(),
            verbose=True,
            tools=[SerperDevTool()]  # Use SerperDevTool for web search
        )
        
        # Report Writer Agent
        report_writer = Agent(
            role=f"{topic} Social Media Report Writer",
            goal=f"Create comprehensive reports on {topic} based on research findings",
            backstory=f"You're a professional report writer who specializes in creating insights from social media analysis. You excel at synthesizing research data into actionable business intelligence reports.",
            llm=self._get_watson_llm(),
            verbose=True
        )
        
        return reddit_researcher, report_writer

    def create_tasks(self, reddit_researcher: Agent, report_writer: Agent, topic: str, subreddits: list):
        """Create tasks for Reddit analysis"""
        
        reddit_research_task = Task(
            description=f"""
            Conduct comprehensive research on {topic} using web search and Reddit analysis:
            
            1. Search the web for recent news and developments about {topic}
            2. Analyze Reddit discussions about {topic} in these subreddits: {', '.join(subreddits)}
            3. Identify trending discussions and key themes
            4. Assess community sentiment and engagement
            5. Find the most engaging posts and discussions
            
            Focus on recent activity and trending topics. Use web search to find current information.
            """,
            expected_output=f"A detailed research summary for {topic} including web findings, Reddit insights, and key trends from {len(subreddits)} subreddits.",
            agent=reddit_researcher
        )
        
        report_writing_task = Task(
            description=f"""
            Create a final comprehensive report on {topic}:
            
            1. Synthesize research findings from web and Reddit analysis
            2. Create an executive summary with key insights
            3. Include actionable recommendations based on trends
            4. Provide risk assessment and opportunity identification
            5. Format as a professional business intelligence report
            
            Make the report actionable, data-driven, and professional.
            """,
            expected_output=f"A professional business intelligence report on {topic} with executive summary, key insights, actionable recommendations, and risk assessment based on research analysis.",
            agent=report_writer
        )
        
        return reddit_research_task, report_writing_task

    def crew(self, topic: str, subreddits: list = None, current_year: str = "2025") -> Crew:
        """Create and return the simplified Reddit analysis crew"""
        
        if subreddits is None:
            # Default subreddits for tech topics
            subreddits = ["artificial", "MachineLearning", "datascience", "programming", "technology"]
        
        reddit_researcher, report_writer = self.create_agents(topic)
        reddit_task, report_task = self.create_tasks(
            reddit_researcher, report_writer, topic, subreddits
        )
        
        return Crew(
            agents=[reddit_researcher, report_writer],
            tasks=[reddit_task, report_task],
            process=Process.sequential,
            verbose=True,
        )

def main():
    """Example usage of simplified Reddit analysis crew"""
    print("🚀 Simplified Reddit Analysis with CrewAI")
    
    # Create crew instance
    crew_instance = SimpleRedditCrew()
    
    # Define topic and subreddits
    topic = "Machine Learning Applications"
    subreddits = ["MachineLearning", "datascience", "artificial", "programming"]
    
    # Create crew
    crew = crew_instance.crew(topic, subreddits, "2025")
    
    # Execute the crew
    print(f"\n🧪 Analyzing topic: {topic}")
    print(f"📊 Monitoring subreddits: {', '.join(subreddits)}")
    print("🔍 Using web search and Reddit analysis")
    
    result = crew.kickoff()
    
    print(f"\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

if __name__ == "__main__":
    main()
