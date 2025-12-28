# agents/planner_agent.py
import os, datetime
from typing import List, Dict, Any
from openai import OpenAI
from configs.prompts import PLANNER_SYSTEM
from tools.calendar_tool import CalendarTool
from tools.memory_tool import MemoryTool
from tools.github_tool import GitHubTool
from utils.ranking import rank_tasks
from utils.reflection import reflect_planner

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PlannerAgent:
    def __init__(self, calendar: CalendarTool, memory: MemoryTool, github: GitHubTool):
        self.calendar = calendar
        self.memory = memory
        self.github = github

    def parse_goals(self, text: str) -> List[Dict[str, Any]]:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":PLANNER_SYSTEM},
                      {"role":"user","content":f"Parse these goals into tasks:\n{text}"}],
            temperature=0.2
        )
        # Expect JSON list in the response; add robust parsing in production
        try:
            import json
            return json.loads(completion.choices[0].message.content)
        except Exception:
            # Fallback: minimal task
            return [{"title": text, "deadline": None, "effort_est": 2, "urgency": 2}]

    def plan_day(self, date: datetime.date, goals_text: str) -> Dict[str, Any]:
        memory_bias = self.memory.get_effort_bias()
        tasks = self.parse_goals(goals_text)
        # Adjust effort estimates based on past performance
        for t in tasks:
            t["effort_est"] = max(1, int((t.get("effort_est") or 2) * (1.0 + memory_bias)))
        ranked = rank_tasks(tasks)

        # Schedule on calendar with focus blocks and buffers
        schedule = []
        start = datetime.datetime.combine(date, datetime.time(9, 0))
        cursor = start
        for t in ranked:
            duration_hours = max(1, t["effort_est"])
            end = cursor + datetime.timedelta(hours=duration_hours)
            event_id = self.calendar.create_event(
                title=f"Task: {t['title']}",
                start=cursor, end=end, description="Agent scheduled task"
            )
            t["calendar_event_id"] = event_id
            schedule.append({"task": t["title"], "start": str(cursor), "end": str(end), "event_id": event_id})
            # Add 15 min buffer
            cursor = end + datetime.timedelta(minutes=15)

        self.memory.save_tasks(ranked)
        return reflect_planner(tasks_scheduled=True, schedule=schedule, issues=[])