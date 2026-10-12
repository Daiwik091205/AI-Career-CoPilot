"""
database.py
SQLite database management module for AI Career Co-Pilot.
Handles connection, initialization, schema migrations, and parameterized queries.
"""

import sqlite3
import json
from datetime import datetime

DB_NAME = "student_career_app.db"

def get_connection():
    """Returns a SQLite connection with foreign keys enabled and row_factory set to sqlite3.Row."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes all required database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # 2. Profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        education TEXT,
        degree TEXT,
        branch TEXT,
        year_semester TEXT,
        experience TEXT,
        interests TEXT,
        career_preferences TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        proficiency TEXT NOT NULL, -- Beginner, Intermediate, Advanced
        updated_at TEXT,
        UNIQUE (user_id, skill_name),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 4. Projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_name TEXT NOT NULL,
        description TEXT NOT NULL,
        extracted_skills TEXT, -- JSON string or comma-separated
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 5. Careers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        career_name TEXT NOT NULL,
        required_skills TEXT, -- JSON array of strings
        selected_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 6. Roadmaps table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        career_id INTEGER,
        gap_analysis TEXT, -- JSON string
        readiness_score INTEGER DEFAULT 0,
        roadmap_json TEXT, -- JSON structured phases
        is_adaptive INTEGER DEFAULT 0,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 7. DSA Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dsa_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'not_attempted', -- not_attempted, attempted, solved
        code_submitted TEXT,
        notes TEXT,
        last_practiced TEXT,
        UNIQUE (user_id, question_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 8. Interview Progress table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id TEXT NOT NULL,
        student_answer TEXT,
        ai_feedback TEXT,
        score INTEGER DEFAULT 0,
        completed_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 9. Learning/Progress tracking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL, -- 'skill', 'roadmap_item', 'dsa_topic'
        item_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        completed_at TEXT,
        UNIQUE (user_id, category, item_name),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# -------------------------------------------------------------
# USER AUTHENTICATION
# -------------------------------------------------------------

def create_user(username: str, password_hash: str):
    """Registers a new user. Returns user_id if successful, or None if username exists."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        now = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?);",
            (username.strip(), password_hash, now)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_username(username: str):
    """Fetch user dictionary by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?;", (username.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int):
    """Fetch user dictionary by user ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# -------------------------------------------------------------
# STUDENT PROFILE
# -------------------------------------------------------------

def get_profile(user_id: int):
    """Fetch profile dict for user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def upsert_profile(user_id: int, education: str, degree: str, branch: str,
                   year_semester: str, experience: str, interests: str, career_preferences: str):
    """Save or update student profile."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO profiles (user_id, education, degree, branch, year_semester, experience, interests, career_preferences, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        education = excluded.education,
        degree = excluded.degree,
        branch = excluded.branch,
        year_semester = excluded.year_semester,
        experience = excluded.experience,
        interests = excluded.interests,
        career_preferences = excluded.career_preferences,
        updated_at = excluded.updated_at;
    """, (user_id, education, degree, branch, year_semester, experience, interests, career_preferences, now))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# SKILLS
# -------------------------------------------------------------

def get_user_skills(user_id: int):
    """Fetch list of skill dicts for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills WHERE user_id = ? ORDER BY skill_name ASC;", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_or_update_skill(user_id: int, skill_name: str, proficiency: str):
    """Add a new skill or update existing proficiency."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    clean_name = skill_name.strip()
    cursor.execute("""
    INSERT INTO skills (user_id, skill_name, proficiency, updated_at)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, skill_name) DO UPDATE SET
        proficiency = excluded.proficiency,
        updated_at = excluded.updated_at;
    """, (user_id, clean_name, proficiency, now))
    conn.commit()
    conn.close()

def delete_skill(user_id: int, skill_id: int):
    """Delete a skill by its ID for the given user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id = ? AND user_id = ?;", (skill_id, user_id))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# PROJECTS
# -------------------------------------------------------------

def get_user_projects(user_id: int):
    """Fetch all projects for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY id DESC;", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    projects = []
    for r in rows:
        d = dict(r)
        try:
            d["extracted_skills_list"] = json.loads(d["extracted_skills"]) if d.get("extracted_skills") else []
        except Exception:
            d["extracted_skills_list"] = [s.strip() for s in d.get("extracted_skills", "").split(",") if s.strip()]
        projects.append(d)
    return projects

def add_project(user_id: int, project_name: str, description: str, extracted_skills: list):
    """Add a new project with its extracted skills list."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    skills_json = json.dumps(extracted_skills)
    cursor.execute("""
    INSERT INTO projects (user_id, project_name, description, extracted_skills, created_at)
    VALUES (?, ?, ?, ?, ?);
    """, (user_id, project_name.strip(), description.strip(), skills_json, now))
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return pid

def delete_project(user_id: int, project_id: int):
    """Delete a project."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ? AND user_id = ?;", (project_id, user_id))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# CAREERS
# -------------------------------------------------------------

def get_user_career(user_id: int):
    """Fetch the student's active target career."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM careers WHERE user_id = ? ORDER BY id DESC LIMIT 1;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d["required_skills_list"] = json.loads(d["required_skills"]) if d.get("required_skills") else []
        except Exception:
            d["required_skills_list"] = []
        return d
    return None

def set_user_career(user_id: int, career_name: str, required_skills: list):
    """Save or update the student's active target career."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    req_json = json.dumps(required_skills)
    # Clear existing active career to maintain single active career per student
    cursor.execute("DELETE FROM careers WHERE user_id = ?;", (user_id,))
    cursor.execute("""
    INSERT INTO careers (user_id, career_name, required_skills, selected_at)
    VALUES (?, ?, ?, ?);
    """, (user_id, career_name.strip(), req_json, now))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid

# -------------------------------------------------------------
# ROADMAPS & SKILL-GAP ANALYSIS
# -------------------------------------------------------------

def get_user_roadmap(user_id: int):
    """Fetch active roadmap and analysis for student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roadmaps WHERE user_id = ? ORDER BY id DESC LIMIT 1;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d["gap_analysis_data"] = json.loads(d["gap_analysis"]) if d.get("gap_analysis") else {}
        except Exception:
            d["gap_analysis_data"] = {}
        try:
            d["roadmap_phases"] = json.loads(d["roadmap_json"]) if d.get("roadmap_json") else []
        except Exception:
            d["roadmap_phases"] = []
        return d
    return None

def save_user_roadmap(user_id: int, career_id: int, gap_analysis: dict, readiness_score: int, roadmap_phases: list, is_adaptive: bool = False):
    """Save newly generated or adapted roadmap."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    gap_json = json.dumps(gap_analysis)
    road_json = json.dumps(roadmap_phases)
    # Remove previous roadmap for user to ensure single active roadmap
    cursor.execute("DELETE FROM roadmaps WHERE user_id = ?;", (user_id,))
    cursor.execute("""
    INSERT INTO roadmaps (user_id, career_id, gap_analysis, readiness_score, roadmap_json, is_adaptive, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (user_id, career_id, gap_json, readiness_score, road_json, 1 if is_adaptive else 0, now))
    conn.commit()
    rid = cursor.lastrowid
    conn.close()
    return rid

# -------------------------------------------------------------
# DSA PRACTICE PROGRESS
# -------------------------------------------------------------

def get_user_dsa_progress(user_id: int):
    """Fetch all DSA progress rows for a user indexed by question_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dsa_progress WHERE user_id = ?;", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {r["question_id"]: dict(r) for r in rows}

def update_dsa_progress(user_id: int, question_id: str, status: str, code: str = "", notes: str = ""):
    """Update progress for a specific DSA question."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO dsa_progress (user_id, question_id, status, code_submitted, notes, last_practiced)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id, question_id) DO UPDATE SET
        status = excluded.status,
        code_submitted = CASE WHEN excluded.code_submitted != '' THEN excluded.code_submitted ELSE dsa_progress.code_submitted END,
        notes = CASE WHEN excluded.notes != '' THEN excluded.notes ELSE dsa_progress.notes END,
        last_practiced = excluded.last_practiced;
    """, (user_id, question_id, status, code, notes, now))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# INTERVIEW PROGRESS
# -------------------------------------------------------------

def get_user_interview_history(user_id: int):
    """Fetch all interview evaluation records for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interview_progress WHERE user_id = ? ORDER BY id DESC;", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_interview_attempt(user_id: int, question_id: str, student_answer: str, ai_feedback: str, score: int):
    """Record an interview answer attempt and AI evaluation."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO interview_progress (user_id, question_id, student_answer, ai_feedback, score, completed_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (user_id, question_id, student_answer, ai_feedback, score, now))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# LEARNING PROGRESS / CHECKLIST ITEMS
# -------------------------------------------------------------

def get_completed_items(user_id: int, category: str = None):
    """Fetch completed items set for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT item_name FROM learning_progress WHERE user_id = ? AND category = ?;", (user_id, category))
    else:
        cursor.execute("SELECT category, item_name FROM learning_progress WHERE user_id = ?;", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    if category:
        return {r["item_name"] for r in rows}
    return [dict(r) for r in rows]

def toggle_completed_item(user_id: int, category: str, item_name: str, is_completed: bool):
    """Mark or unmark an item as completed."""
    conn = get_connection()
    cursor = conn.cursor()
    if is_completed:
        now = datetime.utcnow().isoformat()
        cursor.execute("""
        INSERT INTO learning_progress (user_id, category, item_name, status, completed_at)
        VALUES (?, ?, ?, 'completed', ?)
        ON CONFLICT(user_id, category, item_name) DO UPDATE SET completed_at = excluded.completed_at;
        """, (user_id, category, item_name, now))
    else:
        cursor.execute("DELETE FROM learning_progress WHERE user_id = ? AND category = ? AND item_name = ?;",
                       (user_id, category, item_name))
    conn.commit()
    conn.close()

# -------------------------------------------------------------
# DASHBOARD AGGREGATED STATS
# -------------------------------------------------------------

def get_user_dashboard_stats(user_id: int):
    """Aggregates quick statistics for the student dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Skills count
    cursor.execute("SELECT COUNT(*) AS total FROM skills WHERE user_id = ?;", (user_id,))
    skills_count = cursor.fetchone()["total"]

    # Projects count
    cursor.execute("SELECT COUNT(*) AS total FROM projects WHERE user_id = ?;", (user_id,))
    projects_count = cursor.fetchone()["total"]

    # DSA stats
    cursor.execute("SELECT status, COUNT(*) as cnt FROM dsa_progress WHERE user_id = ? GROUP BY status;", (user_id,))
    dsa_counts = {r["status"]: r["cnt"] for r in cursor.fetchall()}
    dsa_solved = dsa_counts.get("solved", 0)
    dsa_attempted = dsa_counts.get("attempted", 0)

    # Interview stats
    cursor.execute("SELECT COUNT(*) AS total, AVG(score) AS avg_score FROM interview_progress WHERE user_id = ?;", (user_id,))
    interview_row = cursor.fetchone()
    interviews_taken = interview_row["total"] if interview_row else 0
    avg_interview_score = round(interview_row["avg_score"] or 0, 1)

    # Completed roadmap items
    cursor.execute("SELECT COUNT(*) AS total FROM learning_progress WHERE user_id = ? AND category = 'roadmap_item';", (user_id,))
    roadmap_items_completed = cursor.fetchone()["total"]

    conn.close()

    return {
        "skills_count": skills_count,
        "projects_count": projects_count,
        "dsa_solved": dsa_solved,
        "dsa_attempted": dsa_attempted,
        "interviews_taken": interviews_taken,
        "avg_interview_score": avg_interview_score,
        "roadmap_items_completed": roadmap_items_completed
    }

# Ensure database tables exist upon module import
init_db()
