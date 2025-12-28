# mcp_server/server.py
from fastapi import FastAPI
from pydantic import BaseModel
import os, datetime

from agents.planner_agent import PlannerAgent
from agents.meeting_agent import MeetingAgent
from tools.calendar_tool import CalendarTool
from tools.memory_tool import MemoryTool
from tools.email_tool import EmailTool
from tools.reminder_tool import ReminderTool
from tools.github_tool import GitHubTool

app = FastAPI()

calendar = CalendarTool()
memory = MemoryTool(pg_url=os.getenv("PG_URL"))
email = EmailTool()
reminder = ReminderTool(calendar)
github = GitHubTool()

planner = PlannerAgent(calendar=calendar, memory=memory, github=github)
meeting = MeetingAgent(calendar=calendar, email=email, reminder=reminder, memory=memory, github=github)

class PlanDayReq(BaseModel):
    date: str
    goals: str

class MeetingReq(BaseModel):
    title: str
    datetime: str
    attendees: list
    repo: str | None = None

@app.post("/plan_day")
def plan_day(req: PlanDayReq):
    date = datetime.datetime.fromisoformat(req.date).date()
    return planner.plan_day(date=date, goals_text=req.goals)

@app.post("/create_meeting_agenda")
def create_meeting_agenda(req: MeetingReq):
    dt = datetime.datetime.fromisoformat(req.datetime)
    return meeting.create_agenda(req.title, dt, req.attendees, req.repo)

@app.post("/email_attendees")
def email_attendees(req: MeetingReq):
    dt = datetime.datetime.fromisoformat(req.datetime)
    agenda = meeting.create_agenda(req.title, dt, req.attendees, req.repo)
    body = f"Agenda:\n{agenda['agenda']}\nEvent: {agenda['calendar_event_id']}"
    return meeting.email_attendees(req.attendees, subject=f"Agenda: {req.title}", body=body)

@app.post("/set_meeting_reminder")
def set_meeting_reminder(req: MeetingReq):
    dt = datetime.datetime.fromisoformat(req.datetime)
    agenda = meeting.create_agenda(req.title, dt, req.attendees, req.repo)
    return meeting.set_meeting_reminder(agenda["calendar_event_id"], minutes_before=30)