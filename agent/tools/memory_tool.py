# tools/memory_tool.py
import os, psycopg2, json, datetime
from psycopg2.extras import RealDictCursor

class MemoryTool:
    def __init__(self, pg_url: str):
        self.pg_url = pg_url

    def _conn(self):
        return psycopg2.connect(self.pg_url)

    def get_effort_bias(self) -> float:
        with self._conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT avg_effort_bias FROM memory_snapshots ORDER BY date DESC LIMIT 1;")
            row = cur.fetchone()
            return float(row["avg_effort_bias"]) if row else 0.0

    def save_tasks(self, tasks):
        with self._conn() as conn, conn.cursor() as cur:
            for t in tasks:
                cur.execute("""
                  INSERT INTO tasks(title, deadline, effort_est, urgency, status, tags, notes)
                  VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (t.get("title"), t.get("deadline"), t.get("effort_est"), t.get("urgency"),
                      t.get("status","scheduled"), t.get("tags"), t.get("notes")))
            conn.commit()

    def get_meeting_context(self, title: str):
        with self._conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT agenda, datetime FROM meetings WHERE title=%s ORDER BY datetime DESC LIMIT 1;", (title,))
            row = cur.fetchone()
            return {"last_agenda": row["agenda"], "last_datetime": str(row["datetime"])} if row else {}

    def save_meeting(self, title, datetime_, attendees, agenda):
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("""
              INSERT INTO meetings(title, datetime, attendees, agenda, reminders, context_refs)
              VALUES (%s, %s, %s, %s, %s, %s);
            """, (title, datetime_, attendees, json.dumps({"agenda": agenda}), json.dumps([]), json.dumps({})))
            conn.commit()