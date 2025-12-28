# app.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Personas and their allowed tools (expand later if needed)
PERSONAS = {
    "developer": {
        "tools": ["github_list_issues", "fs_read", "fs_write", "pg_query", "web_fetch"],
        "format": "diffs, checklists, commands"
    },
    "pm": {
        "tools": ["github_list_issues", "web_fetch"],
        "format": "briefs, PRDs, stakeholder notes"
    },
    "lead": {
        "tools": ["github_list_issues", "web_fetch", "pg_query"],
        "format": "status dashboards, risks, decisions"
    }
}

# System prompt for the agent
SYSTEM_PROMPT = """
You are a productivity agent.
- Parse natural language goals.
- Rank tasks by urgency and effort.
- Rearrange schedules intelligently.
- Learn from past chats.
- Plan days with memory.
- Check GitHub PRs.
- Track delivery.
- Store tasks in calendar.
Respond in clear, natural language text, not JSON.
"""

def call_agent(messages, allowed_tools):
    """
    Call the OpenAI model with the current conversation.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=0.3,
    )
    return {"type": "text", "content": completion.choices[0].message.content}

def session(persona: str):
    """
    Interactive console loop.
    """
    policy = PERSONAS.get(persona, PERSONAS["developer"])
    allowed_tools = set(policy["tools"])
    messages = []
    print(f"[persona={persona}] Ready. Type your request. Ctrl+C to exit.")
    while True:
        try:
            user = input("> ").strip()
            if not user:
                continue
            messages.append({"role": "user", "content": user})
            res = call_agent(messages, list(allowed_tools))
            print(res["content"])   # plain text response
            messages.append({"role": "assistant", "content": res["content"]})
        except KeyboardInterrupt:
            print("\nBye.")
            break

if __name__ == "__main__":
    persona = os.environ.get("AGENT_PERSONA") or "developer"
    session(persona)