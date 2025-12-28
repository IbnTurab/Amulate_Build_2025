# agents/meeting_agent.py
import os, datetime, json
from typing import Dict, Any, List
from openai import OpenAI
from configs.prompts import MEETING_SYSTEM
from tools.calendar_tool import CalendarTool
from tools.email_tool import EmailTool
from tools.reminder_tool import ReminderTool
from tools.memory_tool import MemoryTool
from tools.github_tool import GitHubTool
from utils.reflection import reflect_meeting

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MeetingAgent:
    def __init__(self, calendar: CalendarTool, email: EmailTool, reminder: ReminderTool, memory: MemoryTool, github: GitHubTool):
        self.calendar = calendar
        self.email = email
        self.reminder = reminder
        self.memory = memory
        self.github = github

    def create_agenda(self, title: str, datetime_: datetime.datetime, attendees: List[str], repo: str = None) -> Dict[str, Any]:
        pr_summary = []
        if repo:
            prs = self.github.list_prs(repo)
            pr_summary = [{"number": p["number"], "title": p["title"], "state": p["state"]} for p in prs]

        prior_context = self.memory.get_meeting_context(title)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":MEETING_SYSTEM},
                      {"role":"user","content":json.dumps({
                          "meeting_title": title,
                          "datetime": str(datetime_),
                          "attendees": attendees,
                          "prior_context": prior_context,
                          "pr_summary": pr_summary
                      })}],
            temperature=0.2
        )
        agenda = completion.choices[0].message.content
        event_id = self.calendar.create_event(
            title=f"Meeting: {title}", start=datetime_, end=datetime_ + datetime.timedelta(hours=1),
            description=f"Agenda:\n{agenda}"
        )
        self.memory.save_meeting(title, datetime_, attendees, agenda)
        return {"agenda": agenda, "calendar_event_id": event_id, "prs": pr_summary}

    def email_attendees(self, attendees: List[str], subject: str, body: str) -> Dict[str, Any]:
        results = [self.email.send(to=a, subject=subject, body=body) for a in attendees]
        return {"sent": results}

    def set_meeting_reminder(self, event_id: str, minutes_before: int = 30) -> Dict[str, Any]:
        reminder_id = self.reminder.create(event_id=event_id, minutes_before=minutes_before)
        return {"reminder_id": reminder_id}

    def run_flow(self, title: str, when: datetime.datetime, attendees: List[str], repo: str = None) -> Dict[str, Any]:
        agenda_res = self.create_agenda(title, when, attendees, repo)
        email_body = f"Agenda for '{title}':\n\n{agenda_res['agenda']}\n\nSee calendar event: {agenda_res['calendar_event_id']}"
        email_res = self.email_attendees(attendees, subject=f"Agenda: {title}", body=email_body)
        rem_res = self.set_meeting_reminder(agenda_res["calendar_event_id"], minutes_before=30)
        reflection = reflect_meeting(
            agenda_created=True, emails_prepared=True, reminders_set=True, issues=[]
        )
        return {"agenda": agenda_res, "email": email_res, "reminder": rem_res, "reflection": reflection}