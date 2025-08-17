#!/usr/bin/env python3
"""
Test script to demonstrate LangChain tools integration with CrewAI
"""

from src.techxchange_hackathon_neuralnexis.crew import LatestAiDevelopmentCrew

def test_with_langchain_tools():
    """Test the crew with LangChain tools enabled"""
    print("🚀 Testing CrewAI with LangChain Tools")
    
    # Create crew instance
    crew_instance = LatestAiDevelopmentCrew()
    
    # Test with LangChain tools enabled
    topic = "Quantum Computing"
    crew = crew_instance.crew(topic, "2025", use_langchain_tools=True)
    
    print(f"\n🧪 Testing with topic: {topic} (LangChain tools enabled)")
    print("Tools available: SerperDevTool, DuckDuckGoSearchRun, WikipediaQueryRun")
    
    # Execute the crew
    result = crew.kickoff()
    
    print(f"\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

def test_without_langchain_tools():
    """Test the crew without LangChain tools (original behavior)"""
    print("\n🚀 Testing CrewAI without LangChain Tools")
    
    # Create crew instance
    crew_instance = LatestAiDevelopmentCrew()
    
    # Test without LangChain tools
    topic = "Artificial Intelligence"
    crew = crew_instance.crew(topic, "2025", use_langchain_tools=False)
    
    print(f"\n🧪 Testing with topic: {topic} (LangChain tools disabled)")
    print("Tools available: SerperDevTool only")
    
    # Execute the crew
    result = crew.kickoff()
    
    print(f"\n✅ RESULT:")
    print("="*60)
    print(result)
    print("="*60)

def main():
    """Run both tests to compare"""
    print("🧪 LangChain Tools Integration Test")
    print("="*60)
    
    # Test with LangChain tools
    test_with_langchain_tools()
    
    # Test without LangChain tools
    test_without_langchain_tools()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
