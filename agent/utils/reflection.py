# utils/reflection.py
def reflect_planner(tasks_scheduled: bool, schedule, issues):
    return {
        "tasks_scheduled": tasks_scheduled,
        "agenda_created": False,
        "emails_prepared": False,
        "reminders_set": False,
        "schedule": schedule,
        "issues": issues
    }

def reflect_meeting(agenda_created: bool, emails_prepared: bool, reminders_set: bool, issues):
    return {
        "tasks_scheduled": False,
        "agenda_created": agenda_created,
        "emails_prepared": emails_prepared,
        "reminders_set": reminders_set,
        "issues": issues
    }