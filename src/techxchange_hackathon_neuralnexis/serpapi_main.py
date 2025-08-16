#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from techxchange_hackathon_neuralnexis.crew import TechxchangeHackathonNeuralnexis

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_serpapi_agent():
    """
    Run only the SerpAPI web researcher agent.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        # Create crew instance
        crew_instance = TechxchangeHackathonNeuralnexis()
        
        # Get the web researcher agent
        web_researcher = crew_instance.web_researcher()
        
        # Get the web research task
        web_research_task = crew_instance.web_research_task()
        
        # Create a simple crew with just the web researcher
        from crewai import Crew, Process
        
        web_crew = Crew(
            agents=[web_researcher],
            tasks=[web_research_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("🚀 Starting SerpAPI Web Research Agent...")
        result = web_crew.kickoff(inputs=inputs)
        
        print("\n✅ Web Research completed!")
        print("--- Web Research Results ---")
        print(result)
        
        return result
        
    except Exception as e:
        raise Exception(f"An error occurred while running the SerpAPI agent: {e}")

def run_full_crew_with_serpapi():
    """
    Run the full crew including the SerpAPI agent.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("🚀 Starting Full Crew with SerpAPI Web Research...")
        TechxchangeHackathonNeuralnexis().crew().kickoff(inputs=inputs)
        print("\n✅ Full crew execution completed!")
        
    except Exception as e:
        raise Exception(f"An error occurred while running the full crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web_only":
        # Run only the SerpAPI agent
        run_serpapi_agent()
    else:
        # Run the full crew with SerpAPI
        run_full_crew_with_serpapi()
