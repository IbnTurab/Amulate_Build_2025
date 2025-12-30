# Amulate Build 2025 – Console Productivity Agent

This project is a **console‑based AI productivity agent** designed to help developers, product managers, and team leads manage tasks, check GitHub activity, and plan their day. It integrates with GitHub using a Personal Access Token (PAT), supports multiple personas, and routes natural language prompts either to the OpenAI model or directly to tools like GitHub.

---

## 📂 Project Architecture

The project is organized into modular folders so each integration is isolated and easy to extend:

AMULATE_PROJECT_2025/
│
├── agent/
│   ├── app.py                     # Main entry point (orchestrates agents & tools)
│   ├── .env                       # Environment variables (API keys, DB URLs)
│   │
│   ├── agents/
│   │   ├── planner_agent.py       # Daily planner & task reasoning agent
│   │   ├── meeting_agent.py       # Meeting agenda & coordination agent
│   │   └── __pycache__/
│   │
│   ├── tools/
│   │   ├── github_tool.py         # GitHub integration (PRs, issues)
│   │   ├── calendar_tool.py       # Calendar scheduling & events
│   │   ├── email_tool.py          # Email sending (meeting invites, follow-ups)
│   │   ├── reminder_tool.py       # Reminders & notifications
│   │   ├── memory_tool.py         # Persistent memory (Postgres / vector DB)
│   │   └── __pycache__/
│   │
│   ├── configs/
│   │   ├── prompts.py             # System prompts (PLANNER, MEETING, etc.)
│   │   └── __pycache__/
│   │
│   ├── mcp_server/
│   │   ├── server.py              # MCP server exposing tools to agents
│   │   └── __pycache__/
│   │
│   ├── storage/
│   │   └── schema.sql             # Database schema for memory & state
│   │
│   ├── utils/
│   │   ├── logging.py             # Centralized logging
│   │   ├── ranking.py             # Task prioritization logic
│   │   ├── reflection.py          # Agent reflection & self-improvement
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── .gitignore
├── README.md
└── requirements.txt


## 🧩 Components

### `app.py`
- Console loop where the user interacts with the agent.
- Loads persona policies (allowed tools, response formats).
- Routes GitHub‑related commands directly to `GitHubTool`.
- Sends all other prompts to the OpenAI model.

### `tools/github_tool.py`
- Wraps GitHub REST API using your Personal Access Token (PAT).
- Methods:
  - `list_repos()` → shows repositories you own.
  - `list_issues(repo)` → lists issues for a given repo.
  - `list_prs(repo)` → lists pull requests for a given repo.

### `tools/date_tool.py`
- Simple helper to return today’s date in human‑readable format.

### Personas
- **Developer** → diffs, checklists, commands; access to GitHub, filesystem, Postgres, web fetch.
- **PM** → briefs, PRDs, stakeholder notes; access to GitHub issues and web fetch.
- **Lead** → dashboards, risks, decisions; access to GitHub, Postgres, web fetch.

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/Amulate_Build_2025.git
   cd Amulate_Build_2025
2. **Create a virtual environment**
   python3 -m venv venv
   source venv/bin/activate
4. **Install dependencies**
   pip install -r requirements.txt
6. **Configure environment variables**
   OPENAI_API_KEY=sk-your-openai-key
   GITHUB_TOKEN=github_pat_yourtokenhere
   AGENT_PERSONA=developer
8. **Run the Agent**
   python3 app.py

## 🖥️ Usage

1. **Start the App**
   [persona=developer] Ready. Type your request. Ctrl+C to exit.
2. **Example GitHub commands**
   > what is in my github
  - username/repo1
  - username/repo2

  > show prs octocat/Hello-World
  - Add new feature (#42)
3. **Example Natural Language Prompts**
  > plan my tasks for today
  AI: Here’s a checklist for your day…
  
---

## 🔒 Security Guidelines

To keep your credentials and data safe while using this agent:

- **Do not share your `.env` file** or commit it to version control. It contains sensitive keys.
- **Use your own API keys**: You must provide your own OpenAI API key and GitHub Personal Access Token (PAT). These are not included in this project.
- **Rotate your tokens regularly** to reduce risk in case of accidental exposure.
- **Keep your keys private**: Never post your API keys or tokens publicly.

## 👨‍💻 Author

Built by Mohd Anas, and Arham Moin for the Amulate Hackathon 2025
If you find this project useful or inspiring, feel free to fork it, contribute, or reach out!
   
