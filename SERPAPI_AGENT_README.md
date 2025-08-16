# SerpAPI Agent for TechXchange_Hackathon_NeuralNexis

This document explains how to set up and use the new SerpAPI agent that provides web search capabilities to your CrewAI project.

## 🚀 **What's New**

### **New Agent: Web Research Specialist**
- **Role**: Web Research Specialist with real-time search capabilities
- **Goal**: Conduct comprehensive web research using SerpAPI
- **Tools**: SerpAPI web search tool
- **Output**: `web_research_results.md` with current web findings

### **New Files Created**
- `src/techxchange_hackathon_neuralnexis/tools/serpapi_tool.py` - SerpAPI search tool
- `src/techxchange_hackathon_neuralnexis/serpapi_main.py` - Separate runner for SerpAPI agent
- Updated `config/agents.yaml` - Added web_researcher agent
- Updated `config/tasks.yaml` - Added web_research_task
- Updated `crew.py` - Integrated SerpAPI agent

## 🔧 **Setup Instructions**

### **Step 1: Get SerpAPI Key**
1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard

### **Step 2: Set Environment Variables**
```bash
# Add SerpAPI key to your .env file
echo "SERPAPI_KEY=your_serpapi_key_here" >> .env
```

### **Step 3: Install Dependencies**
```bash
# Sync dependencies with UV
uv sync
```

## 🎯 **How to Run**

### **Option 1: Run Only SerpAPI Agent**
```bash
source .venv/bin/activate && python -m techxchange_hackathon_neuralnexis.serpapi_main web_only
```

### **Option 2: Run Full Crew with SerpAPI**
```bash
source .venv/bin/activate && python -m techxchange_hackathon_neuralnexis.serpapi_main
```

### **Option 3: Run Original Crew (without SerpAPI)**
```bash
source .venv/bin/activate && python -m techxchange_hackathon_neuralnexis.main
```

## 📋 **Agent Workflow**

### **Three-Agent Workflow (with SerpAPI)**
1. **Researcher Agent** - Traditional research using training data
2. **Web Research Specialist** - Real-time web search using SerpAPI
3. **Reporting Analyst** - Combines both research sources into final report

### **Output Files**
- `report.md` - Final comprehensive report
- `web_research_results.md` - Web search findings only

## 🔍 **SerpAPI Tool Features**

### **Search Capabilities**
- **Google Search**: Primary search engine
- **Result Count**: Configurable (1-10 results)
- **Timeout**: 30 seconds per request
- **Error Handling**: Graceful fallback for API issues

### **Tool Input**
```python
{
    "query": "AI LLMs latest developments 2025",
    "num_results": 5
}
```

### **Tool Output**
```
Search Results for 'AI LLMs latest developments 2025':

1. Latest AI LLM Developments in 2025
   URL: https://example.com/ai-llm-2025
   Description: Recent breakthroughs in large language models...

2. New AI Models Released This Year
   URL: https://example.com/new-models-2025
   Description: Overview of new language models...
```

## ⚙️ **Customization**

### **Change Search Topic**
Edit `serpapi_main.py`:
```python
inputs = {
    'topic': 'Your Topic Here',  # Change this
    'current_year': str(datetime.now().year)
}
```

### **Modify Search Parameters**
Edit `serpapi_tool.py`:
```python
params = {
    "q": query,
    "api_key": api_key,
    "num": num_results,
    "engine": "google",  # Can change to "bing", "yahoo", etc.
    "gl": "us",          # Add country
    "hl": "en"           # Add language
}
```

### **Add More Search Engines**
You can extend the tool to support:
- Bing Search
- Yahoo Search
- DuckDuckGo
- News Search
- Image Search

## 💡 **Use Cases**

### **Perfect For**
- **Current Events**: Get latest news and developments
- **Market Research**: Find recent industry trends
- **Fact Checking**: Verify information with current sources
- **Competitive Analysis**: Research competitors and products
- **Academic Research**: Find recent papers and studies

### **Example Queries**
- "AI LLMs latest developments 2025"
- "OpenAI GPT-5 release date"
- "Google Gemini latest features"
- "AI regulation news 2025"
- "Machine learning conferences 2025"

## 🚨 **Important Notes**

### **API Limits**
- **Free Plan**: 100 searches per month
- **Paid Plans**: Higher limits available
- **Rate Limiting**: Built-in timeout and error handling

### **Cost Considerations**
- SerpAPI has usage-based pricing
- Monitor your usage in the SerpAPI dashboard
- Consider upgrading for higher volume usage

### **Data Privacy**
- Search queries are sent to SerpAPI
- Results are processed locally
- No data is stored permanently

## 🔧 **Troubleshooting**

### **Common Issues**

**"SERPAPI_KEY not found"**
```bash
# Check if .env file exists and has the key
cat .env | grep SERPAPI_KEY
```

**"No search results found"**
- Check your internet connection
- Verify the search query is valid
- Check SerpAPI dashboard for API status

**"Error performing web search"**
- Verify your SerpAPI key is correct
- Check your API usage limits
- Ensure you have an active SerpAPI subscription

### **Debug Mode**
Add debug logging to `serpapi_tool.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 **Support**

- **SerpAPI Documentation**: https://serpapi.com/docs
- **CrewAI Documentation**: https://docs.crewai.com
- **Project Issues**: Check the main project repository

---

**Happy Searching! 🔍✨**
