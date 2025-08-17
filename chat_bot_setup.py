# setup_project.py
import os, pathlib, textwrap, json

ROOT = pathlib.Path("crew_chatbot")
TOOLS = ROOT / "app" / "tools"
(TOOLS).mkdir(parents=True, exist_ok=True)

def write(p: pathlib.Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"✓ wrote {p}")

# ---------------- files ----------------

write(ROOT / "requirements.txt", """
    crewai>=0.51.0
    crewai-tools>=0.8.0
    litellm>=1.52.0
    python-dotenv>=1.0.1
    requests>=2.32.3
    praw>=7.7.1
    fastapi>=0.111.0
    uvicorn>=0.30.0
    tiktoken>=0.7.0
""")

write(ROOT / ".env.example", """
    # LLM model via LiteLLM
    # OpenAI:
    # LLM_MODEL=gpt-4o-mini
    # OPENAI_API_KEY=sk-...

    # IBM watsonx via LiteLLM:
    # LLM_MODEL=watsonx/ibm/granite-3-8b-instruct
    # WATSONX_URL=https://us-south.ml.cloud.ibm.com
    # WATSONX_APIKEY=your_ibm_api_key
    # WATSONX_PROJECT_ID=your_project_guid

    # Web search (SerpAPI)
    SERPAPI_KEY=your_serpapi_key

    # Reddit API (create at https://www.reddit.com/prefs/apps, app type 'script')
    REDDIT_CLIENT_ID=xxxx
    REDDIT_CLIENT_SECRET=xxxx
    REDDIT_USER_AGENT=crew-chatbot/0.1 by u/yourusername

    # OpenAlex API polite usage
    OPENALEX_MAILTO=you@example.com
""")

write(ROOT / "README.md", """
    # CrewAI Conversational Chatbot (Research + Planning)

    This starter builds a **CrewAI** chatbot that:
    - asks clarifying questions,
    - searches the **web**, **OpenAlex** (scholarly), and **Reddit**,
    - plans ≤7 tasks with time/impact/priority,
    - replies empathetically with citations.

    ## Setup
    ```bash
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env  # fill in keys
    ```

    Choose an LLM via LiteLLM in `.env`:
    - **OpenAI**: `LLM_MODEL=gpt-4o-mini` + `OPENAI_API_KEY=...`
    - **IBM watsonx**: `LLM_MODEL=watsonx/ibm/granite-3-8b-instruct` + `WATSONX_*` vars

    Add keys:
    - `SERPAPI_KEY` (Google web search via SerpAPI)
    - `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
    - `OPENALEX_MAILTO` (your email)

    ## Run the API
    ```bash
    uvicorn app.api:app --reload --port 8000
    # POST http://localhost:8000/chat {"message":"Help me learn PySpark in 2 weeks"}
    ```

    ## Run the CLI
    ```bash
    python run_chat.py
    ```

    ## Files
    - `app/crew_chatbot.py` — agents + tasks + crew pipeline
    - `app/tools/web_search.py` — SerpAPI wrapper
    - `app/tools/openalex.py` — scholarly search (OpenAlex)
    - `app/tools/reddit_tool.py` — Reddit search via PRAW
    - `app/api.py` — FastAPI server
    - `run_chat.py` — simple CLI
""")

write(ROOT / "run_chat.py", """
    import os
    from dotenv import load_dotenv
    from app.crew_chatbot import run_chat

    def main():
        load_dotenv()
        print("CrewAI Conversational Chatbot. Ctrl+C to exit.\\n")
        while True:
            try:
                msg = input("You: ")
                print("\\nThinking...\\n")
                reply = run_chat(msg)
                print(f"Assistant:\\n{reply}\\n")
            except KeyboardInterrupt:
                print("\\nBye!\\n")
                break

    if __name__ == "__main__":
        main()
""")

write(ROOT / "app" / "api.py", """
    import os
    from fastapi import FastAPI
    from pydantic import BaseModel
    from dotenv import load_dotenv
    from app.crew_chatbot import run_chat

    load_dotenv()
    app = FastAPI(title="CrewAI Conversational Chatbot")

    class ChatIn(BaseModel):
        message: str

    @app.post("/chat")
    def chat(inp: ChatIn):
        reply = run_chat(inp.message)
        return {"reply": reply}
""")

write(TOOLS / "web_search.py", """
    import os, requests, json
    from crewai_tools import tool

    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

    @tool("web_search")
    def web_search(query: str, num_results: int = 5) -> str:
        \"\"\"Search the web for relevant links using SerpAPI.
        Returns a JSON string with a list of {'title','url','snippet'}\"\"\"
        if not SERPAPI_KEY:
            return json.dumps({"error": "SERPAPI_KEY missing"})
        params = {
            "engine": "google",
            "q": query,
            "num": num_results,
            "api_key": SERPAPI_KEY
        }
        r = requests.get("https://serpapi.com/search", params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        results = []
        for item in (data.get("organic_results") or [])[:num_results]:
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })
        return json.dumps({"query": query, "results": results}, ensure_ascii=False)
""")

write(TOOLS / "openalex.py", """
    import os, requests, json, urllib.parse
    from crewai_tools import tool

    MAILTO = os.getenv("OPENALEX_MAILTO", "anonymous@example.com")

    @tool("scholar_search")
    def scholar_search(query: str, per_page: int = 5) -> str:
        \"\"\"Search OpenAlex for scholarly works.
        Returns a JSON string with [{'title','year','doi','open_access','url'}].\"\"\"
        q = urllib.parse.quote(query)
        url = f"https://api.openalex.org/works?search={q}&per_page={per_page}&mailto={MAILTO}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        out = []
        for w in data.get("results", [])[:per_page]:
            oa = (w.get("open_access") or {})
            oa_url = oa.get("oa_url")
            primary = (w.get("primary_location") or {})
            work_url = oa_url or primary.get("source", {}).get("host_organization_name") or w.get("id")
            out.append({
                "title": w.get("display_name"),
                "year": w.get("publication_year"),
                "doi": w.get("doi"),
                "open_access": oa.get("is_oa"),
                "url": work_url
            })
        return json.dumps({"query": query, "results": out}, ensure_ascii=False)
""")

write(TOOLS / "reddit_tool.py", """
    import os, json
    import praw
    from crewai_tools import tool

    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    USER_AGENT = os.getenv("REDDIT_USER_AGENT", "crew-chatbot/0.1")

    def _client():
        if not (CLIENT_ID and CLIENT_SECRET and USER_AGENT):
            return None
        return praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            check_for_async=False
        )

    @tool("reddit_search")
    def reddit_search(query: str, subreddits: str = "ADHD+Productivity", limit: int = 5) -> str:
        \"\"\"Search Reddit posts by query (comma-or-plus separated subreddits).
        Returns JSON string with list of {'title','url','score','num_comments'}.\"\"\"
        reddit = _client()
        if reddit is None:
            return json.dumps({"error": "Reddit credentials missing"})
        subs = [s.strip() for s in subreddits.replace(",", "+").split("+") if s.strip()]
        results = []
        for s in subs:
            try:
                for post in reddit.subreddit(s).search(query, sort="relevance", time_filter="year", limit=limit):
                    results.append({
                        "subreddit": s,
                        "title": post.title,
                        "url": f"https://www.reddit.com{post.permalink}",
                        "score": post.score,
                        "num_comments": post.num_comments
                    })
            except Exception as e:
                results.append({"subreddit": s, "error": str(e)})
        return json.dumps({"query": query, "results": results}, ensure_ascii=False)
""")

write(ROOT / "app" / "crew_chatbot.py", """
    import os, json
    from dotenv import load_dotenv
    from crewai import Agent, Task, Crew
    from app.tools.web_search import web_search
    from app.tools.openalex import scholar_search
    from app.tools.reddit_tool import reddit_search

    load_dotenv()

    MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # or watsonx/ibm/granite-3-8b-instruct

    # ---- Agents ----
    conversation_agent = Agent(
        name="ConversationAgent",
        role="Clarifies the user's goal and constraints empathetically.",
        goal="Ask smart follow-ups (≤4) and summarize the request.",
        backstory=(
            "You are an empathetic coach for neurodivergent users. You validate briefly, then clarify. "
            "Produce a concise summary and up to 4 questions if needed."
        ),
        llm=MODEL,
        max_iter=1,
        allow_delegation=False,
        verbose=True
    )

    research_agent = Agent(
        name="ResearchAgent",
        role="Finds relevant web articles, scholarly papers, and Reddit threads.",
        goal="Return a curated list with titles + URLs + why relevant.",
        backstory=(
            "You are a precise researcher. Prioritize high-signal links, avoid duplicates, and "
            "include 1-2 practical Reddit discussions when helpful."
        ),
        tools=[web_search, scholar_search, reddit_search],
        llm=MODEL,
        max_iter=1,
        allow_delegation=False,
        verbose=True
    )

    planner_agent = Agent(
        name="PlannerAgent",
        role="Turns the clarified request + research into a concrete plan of tasks.",
        goal="Produce ≤7 tasks with time_hours, impact_pct (sum≈100), and priority_score=impact_pct/max(time_hours,0.25).",
        backstory=("Expert task architect. Plans for short focus blocks and clear outcomes."),
        llm=MODEL,
        max_iter=1,
        allow_delegation=False,
        verbose=True
    )

    responder_agent = Agent(
        name="ResponderAgent",
        role="Writes the final chatbot response.",
        goal="Be empathetic, cite 3-6 links, and present the prioritized plan + a micro-step for today.",
        backstory="You communicate clearly with brief validation and concrete actions.",
        llm=MODEL,
        max_iter=1,
        allow_delegation=False,
        verbose=True
    )

    # ---- Tasks ----
    clarify = Task(
        description=(
            "Given the user's message, ask up to 4 clarifying questions if needed, then produce a concise summary.\\n"
            "Output JSON with keys: 'summary', 'questions' (list, can be empty)."
        ),
        expected_output="JSON with 'summary' and 'questions' (list).",
        agent=conversation_agent
    )

    research = Task(
        description=(
            "Use tools to find relevant information. Call `web_search` for general links, "
            "`scholar_search` for studies, and `reddit_search` for lived experiences. "
            "Return JSON with 'citations': a list of objects {title,url,why}. Keep 4-8 items."
        ),
        expected_output="JSON with 'citations' list (4-8 curated items).",
        agent=research_agent,
        context=[clarify]
    )

    plan = Task(
        description=(
            "Using the summary and citations, propose a task plan (≤7 tasks). "
            "For each task: name, desc, time_hours (0.25 increments), impact_pct (sum≈100), "
            "priority_score=impact_pct/max(time_hours,0.25). Output JSON with 'tasks' and 'notes'."
        ),
        expected_output="JSON with 'tasks' (list) and 'notes'.",
        agent=planner_agent,
        context=[clarify, research]
    )

    respond = Task(
        description=(
            "Write the final chatbot reply:\\n"
            "1) one-sentence validation\\n"
            "2) brief summary\\n"
            "3) bullet list of prioritized tasks (show time + impact + score)\\n"
            "4) 'Do-today' micro-step (25-50 min)\\n"
            "5) 3-6 citations (titles hyperlinked)\\n"
            "Tone: supportive, concise, and actionable."
        ),
        expected_output="Clear, friendly message with bullets + linked citations.",
        agent=responder_agent,
        context=[clarify, research, plan]
    )

    crew = Crew(
        agents=[conversation_agent, research_agent, planner_agent, responder_agent],
        tasks=[clarify, research, plan, respond],
        verbose=True
    )

    def run_chat(user_message: str) -> str:
        result = crew.kickoff(inputs={"input": user_message})
        return str(result)
""")

print("\nAll files written. Next steps:")
print("1) cd crew_chatbot")
print("2) python -m venv .venv && source .venv/bin/activate")
print("3) pip install -r requirements.txt")
print("4) cp .env.example .env  # fill in keys")
print("5) uvicorn app.api:app --reload --port 8000")
