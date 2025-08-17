#!/usr/bin/env python
import sys
import warnings
import argparse

from datetime import datetime

from techxchange_hackathon_neuralnexis.crew import TechxchangeHackathonNeuralnexis
from crew import LatestAiDevelopmentCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Neurodivergence',
        'current_year': str(datetime.now().year)
    }
    
    try:
        TechxchangeHackathonNeuralnexis().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def run_latest_ai_crew(topic: str, year: str = None):
    """
    Run the LatestAiDevelopmentCrew with a specific topic.
    """
    if year is None:
        year = str(datetime.now().year)
    
    print(f"\n{'='*60}")
    print(f"🧪 RUNNING LATEST AI CREW: {topic}")
    print(f"{'='*60}")
    
    try:
        # Create crew instance
        crew_instance = LatestAiDevelopmentCrew()
        
        # Create crew with topic
        crew = crew_instance.crew(topic, year)
        
        # Execute the crew
        result = crew.kickoff()
        
        print(f"\n✅ SUCCESS: {topic}")
        print(f"{'='*60}")
        print("RESULT:")
        print(result)
        print(f"{'='*60}")
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR with topic '{topic}': {str(e)}")
        return None

def test_multiple_topics():
    """
    Test the LatestAiDevelopmentCrew with multiple predefined topics.
    """
    print("🚀 Starting Multiple Topic Tests")
    print("This will test the LatestAiDevelopmentCrew with different research topics")
    
    # List of topics to test
    topics = [
        "Neurodivergence",
        "Quantum Computing", 
        "Climate Change Solutions",
        "Blockchain Technology",
        "Space Exploration 2025"
    ]
    
    results = {}
    
    # Test each topic
    for topic in topics:
        result = run_latest_ai_crew(topic)
        results[topic] = result
        
    print("\n🎉 All topic tests completed!")
    return results

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        TechxchangeHackathonNeuralnexis().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TechxchangeHackathonNeuralnexis().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        TechxchangeHackathonNeuralnexis().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def main():
    """
    Main function to handle command line arguments and run appropriate functions.
    """
    parser = argparse.ArgumentParser(description='TechXchange Hackathon NeuralNexis Crew Runner')
    parser.add_argument('command', choices=['run', 'train', 'replay', 'test', 'latest-ai', 'multi-test'], 
                       help='Command to execute')
    parser.add_argument('--topic', type=str, help='Topic for latest-ai command')
    parser.add_argument('--year', type=str, help='Year for latest-ai command (defaults to current year)')
    parser.add_argument('--args', nargs='*', help='Additional arguments for train/replay/test commands')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run()
    elif args.command == 'latest-ai':
        if not args.topic:
            print("❌ Error: --topic is required for latest-ai command")
            sys.exit(1)
        run_latest_ai_crew(args.topic, args.year)
    elif args.command == 'multi-test':
        test_multiple_topics()
    elif args.command == 'train':
        if not args.args or len(args.args) < 2:
            print("❌ Error: train command requires n_iterations and filename arguments")
            sys.exit(1)
        sys.argv = [sys.argv[0]] + args.args
        train()
    elif args.command == 'replay':
        if not args.args or len(args.args) < 1:
            print("❌ Error: replay command requires task_id argument")
            sys.exit(1)
        sys.argv = [sys.argv[0]] + args.args
        replay()
    elif args.command == 'test':
        if not args.args or len(args.args) < 2:
            print("❌ Error: test command requires n_iterations and eval_llm arguments")
            sys.exit(1)
        sys.argv = [sys.argv[0]] + args.args
        test()

if __name__ == "__main__":
    main()
