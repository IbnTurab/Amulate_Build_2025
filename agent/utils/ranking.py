# utils/ranking.py
from datetime import datetime

def _deadline_score(deadline):
    if not deadline: return 3
    try:
        d = deadline if isinstance(deadline, datetime) else datetime.fromisoformat(str(deadline))
        days = (d - datetime.now()).days
        if days <= 0: return 1
        if days <= 2: return 2
        if days <= 7: return 3
        return 4
    except Exception:
        return 3

def rank_tasks(tasks):
    # Lower score = higher priority
    def score(t):
        dscore = _deadline_score(t.get("deadline"))
        effort = int(t.get("effort_est", 2))
        urgency = int(t.get("urgency", 2))
        return (dscore, effort, 6 - urgency)
    return sorted(tasks, key=score)