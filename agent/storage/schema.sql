-- storage/schema.sql
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  deadline TIMESTAMP WITH TIME ZONE,
  effort_est INT,
  urgency INT,
  status TEXT DEFAULT 'pending',
  calendar_event_id TEXT,
  tags TEXT[],
  notes TEXT
);
CREATE TABLE IF NOT EXISTS memory_snapshots (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  tasks_completed INT DEFAULT 0,
  tasks_deferred INT DEFAULT 0,
  avg_effort_bias REAL DEFAULT 0.0,
  preferences JSONB DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS meetings (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  datetime TIMESTAMP WITH TIME ZONE,
  attendees TEXT[],
  agenda JSONB,
  reminders JSONB,
  context_refs JSONB
);