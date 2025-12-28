# tools/github_tool.py
import os, requests

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.token}", "Accept":"application/vnd.github+json"}

    def list_prs(self, repo: str):
        r = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json()

    def list_issues(self, repo: str, state: str = "open"):
        r = requests.get(f"https://api.github.com/repos/{repo}/issues?state={state}", headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json()