#!/usr/bin/env python3
"""
Test SerpAPI Tool Directly
"""

import os
from dotenv import load_dotenv
from techxchange_hackathon_neuralnexis.tools.serpapi_tool import SerpAPISearchTool

# Load environment variables
load_dotenv()

def test_serpapi_tool():
    """Test the SerpAPI tool directly"""
    
    print("🧪 Testing SerpAPI Tool")
    print("=" * 50)
    
    # Check if SERPAPI_KEY is set
    api_key = os.getenv("SERPAPI_KEY")
    print(f"SERPAPI_KEY: {'✅ Set' if api_key else '❌ Not set'}")
    
    if not api_key:
        print("\n❌ Error: SERPAPI_KEY not found in environment variables")
        print("Please add your SerpAPI key to the .env file:")
        print("SERPAPI_KEY=your_serpapi_key_here")
        return False
    
    # Create the tool
    print("\n🔧 Creating SerpAPI Tool...")
    try:
        serpapi_tool = SerpAPISearchTool()
        print("✅ SerpAPI Tool created successfully")
        print(f"Tool Name: {serpapi_tool.name}")
        print(f"Tool Description: {serpapi_tool.description}")
    except Exception as e:
        print(f"❌ Error creating tool: {e}")
        return False
    
    # Test the tool with a simple query
    print("\n🔍 Testing Web Search...")
    try:
        query = "AI LLMs 2025"
        num_results = 3
        
        print(f"Searching for: '{query}'")
        print(f"Number of results: {num_results}")
        
        result = serpapi_tool._run(query=query, num_results=num_results)
        
        print("\n✅ Search completed!")
        print("=" * 50)
        print("Search Results:")
        print("=" * 50)
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return False

if __name__ == "__main__":
    success = test_serpapi_tool()
    
    if success:
        print("\n🎉 SerpAPI Tool test completed successfully!")
    else:
        print("\n❌ SerpAPI Tool test failed!")
    
    print("\n" + "=" * 50)
