# tools/reminder_tool.py
import uuid

class ReminderTool:
    def __init__(self, calendar_tool):
        self.calendar = calendar_tool
        self._reminders = {}

    def create(self, event_id: str, minutes_before: int = 30) -> str:
        rem_id = f"rem_{uuid.uuid4().hex[:8]}"
        self._reminders[rem_id] = {"event_id": event_id, "minutes_before": minutes_before}
        return rem_id