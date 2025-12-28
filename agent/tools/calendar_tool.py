# tools/calendar_tool.py
import uuid
from typing import Optional
from datetime import datetime

class CalendarTool:
    def __init__(self):
        # Replace with real Calendar MCP client
        self._events = {}

    def create_event(self, title: str, start: datetime, end: datetime, description: Optional[str] = None) -> str:
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        self._events[event_id] = {"title": title, "start": start, "end": end, "description": description}
        return event_id

    def update_event(self, event_id: str, **kwargs) -> bool:
        if event_id in self._events:
            self._events[event_id].update(kwargs)
            return True
        return False