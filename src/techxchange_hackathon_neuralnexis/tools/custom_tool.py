from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


class SerpAPISearchInput(BaseModel):
    """Input schema for SerpAPI search tool."""
    query: str = Field(..., description="The search query to look up on the web.")
    num_results: int = Field(default=5, description="Number of results to return (default: 5, max: 10)")

class SerpAPISearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the web for current information about a topic. "
        "Use this tool when you need to find recent news, facts, or information "
        "that might not be in your training data. Provide a clear search query."
    )
    args_schema: Type[BaseModel] = SerpAPISearchInput

    def _run(self, query: str, num_results: int = 5) -> str:
        """
        Perform a web search using SerpAPI.

        Args:
            query: The search query
            num_results: Number of results to return (max 10)

        Returns:
            Formatted search results as a string
        """
        api_key = os.getenv("SERPAPI_KEY")

        if not api_key:
            return "Error: SERPAPI_KEY not found in environment variables. Please set your SerpAPI key."

        # Limit results to 10
        num_results = min(num_results, 10)

        try:
            # SerpAPI endpoint
            url = "https://serpapi.com/search"

            params = {
                "q": query,
                "api_key": api_key,
                "num": num_results,
                "engine": "google"
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Extract organic results
            organic_results = data.get("organic_results", [])

            if not organic_results:
                return f"No search results found for: {query}"

            # Format results
            formatted_results = []
            for i, result in enumerate(organic_results[:num_results], 1):
                title = result.get("title", "No title")
                link = result.get("link", "No link")
                snippet = result.get("snippet", "No description")

                formatted_results.append(
                    f"{i}. {title}\n"
                    f"   URL: {link}\n"
                    f"   Description: {snippet}\n"
                )

            return f"Search Results for '{query}':\n\n" + "\n".join(formatted_results)

        except requests.exceptions.RequestException as e:
            return f"Error performing web search: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
