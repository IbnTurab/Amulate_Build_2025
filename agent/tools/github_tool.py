# tools/github_tool.py
import os, requests

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN not found in environment")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def list_issues(self, repo: str, state: str = "open"):
        r = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers=self.headers,
            params={"state": state},
            timeout=15
        )
        r.raise_for_status()
        return [i for i in r.json() if "pull_request" not in i]
    
    def list_prs(self, repo: str):
        r = requests.get(
            f"https://api.github.com/repos/{repo}/pulls",
            headers=self.headers,
            timeout=15
        )
        r.raise_for_status()
        return r.json()
