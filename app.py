"""
app.py
Main entry point and authentication router for AI Career Co-Pilot.
Coordinates user sessions, bcrypt authentication, navigation sidebar,
and imports modular pages.
"""

import streamlit as st
import database as db
import ai_service
from utils.helpers import hash_password, verify_password

# Modular page renders
from pages.dashboard import render_dashboard
from pages.profile import render_profile
from pages.skills import render_skills
from pages.projects import render_projects
from pages.career import render_career
from pages.analysis import render_analysis
from pages.roadmap import render_roadmap
from pages.dsa import render_dsa
from pages.interviews import render_interviews
from pages.progress import render_progress

# Configure Streamlit page
st.set_page_config(
    page_title="AI Career Co-Pilot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "user" not in st.session_state:
    st.session_state["user"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

def login_user(user_dict: dict):
    st.session_state["user"] = user_dict
    st.session_state["current_page"] = "Dashboard"

def logout_user():
    st.session_state["user"] = None
    st.session_state["current_page"] = "Dashboard"
    st.rerun()

def render_auth():
    """Render Login & Registration portal."""
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="color: #1f77b4; font-size: 2.8rem; margin-bottom: 5px;">🎓 AI Career Co-Pilot</h1>
            <p style="font-size: 1.15rem; color: #555;">
                AI-Powered Career Guidance & Technical Preparation Platform for College Students
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_center = st.columns([1, 2, 1])[1]

    with col_center:
        tab_login, tab_register, tab_about = st.tabs(["🔐 Sign In", "📝 Create Account", "ℹ️ About System"])

        with tab_login:
            st.write("### Welcome Back")
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="e.g. daiwik_student").strip()
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

                if login_submitted:
                    if not username or not password:
                        st.error("Please provide both username and password.")
                    else:
                        user = db.get_user_by_username(username)
                        if user and verify_password(password, user["password_hash"]):
                            st.success(f"Welcome back, {username}!")
                            login_user(user)
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")

            # Quick Demo User Shortcut
            st.markdown("---")
            st.caption("🚀 College Demonstration Quick Access:")
            if st.button("Load Demo Student Account", use_container_width=True):
                demo_user = db.get_user_by_username("demo_student")
                if not demo_user:
                    # Seed demo user
                    pwd_hash = hash_password("demo1234")
                    uid = db.create_user("demo_student", pwd_hash)
                    demo_user = db.get_user_by_id(uid)

                    # Seed initial profile & skills for realistic showcase
                    db.upsert_profile(
                        user_id=uid,
                        education="Undergraduate (B.Tech / B.E. / B.Sc / BCA)",
                        degree="B.Tech in Computer Science",
                        branch="Computer Science & Engineering",
                        year_semester="3rd Year (Sem 5-6)",
                        experience="Completed a 2-month summer internship building REST APIs with Python & FastAPI.",
                        interests="Backend engineering, Distributed systems, Machine Learning.",
                        career_preferences="Product software engineering or ML systems."
                    )
                    db.add_or_update_skill(uid, "Python", "Advanced")
                    db.add_or_update_skill(uid, "SQL", "Intermediate")
                    db.add_or_update_skill(uid, "Data Structures & Algorithms", "Intermediate")
                    db.add_or_update_skill(uid, "Git & Version Control", "Intermediate")
                    db.add_or_update_skill(uid, "FastAPI", "Beginner")

                    db.add_project(
                        uid,
                        "Smart Campus RFID Gate",
                        "Built an RFID-based access control system using Arduino and C++. Integrated RC522 reader with SQLite log database.",
                        ["Arduino", "RFID", "Embedded Systems", "C++", "SQLite"]
                    )
                    db.set_user_career(uid, "Software Developer", [
                        "Data Structures & Algorithms", "Python", "Java", "Object-Oriented Programming (OOP)",
                        "Relational Databases (SQL)", "Git & Version Control", "REST APIs", "Operating Systems & Multithreading",
                        "Computer Networks", "Unit Testing"
                    ])

                login_user(demo_user)
                st.rerun()

        with tab_register:
            st.write("### Create Student Account")
            with st.form("register_form"):
                reg_username = st.text_input("Choose Username", placeholder="e.g. alex_coder").strip()
                reg_password = st.text_input("Choose Password", type="password", placeholder="Minimum 6 characters")
                reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                reg_submitted = st.form_submit_button("Register Account", use_container_width=True, type="primary")

                if reg_submitted:
                    if not reg_username or not reg_password:
                        st.error("All fields are required.")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    elif reg_password != reg_confirm:
                        st.error("Passwords do not match.")
                    else:
                        hashed = hash_password(reg_password)
                        user_id = db.create_user(reg_username, hashed)
                        if user_id:
                            st.success("Account registered successfully! Signing you in...")
                            new_user = db.get_user_by_id(user_id)
                            login_user(new_user)
                            st.rerun()
                        else:
                            st.error("Username already taken. Please select a different username.")

        with tab_about:
            st.markdown(
                """
                ### About AI Career Co-Pilot
                **AI Career Co-Pilot** is an end-to-end guidance platform for college engineering students:
                - **Profile & Project Analysis**: Extracts technical skills directly from project descriptions using LLMs.
                - **Skill-Gap Analysis**: Benchmarks student abilities against industry career roles.
                - **Adaptive Roadmap**: Multi-phase customized study roadmap that updates as you solve problems and build projects.
                - **DSA Practice Suite**: 14 core topics with safe sandboxed test cases and AI mentor hints.
                - **Mock Interview Engine**: Technical and behavioral interview drills with rubric-based AI scoring.
                """
            )

def render_app():
    """Render authenticated application UI with sidebar navigation."""
    user = st.session_state["user"]
    user_id = user["id"]
    username = user["username"]

    # Sidebar Header & User Profile
    with st.sidebar:
        st.markdown(f"## 🎓 AI Career Co-Pilot")
        st.markdown(f"Signed in as: **{username}**")

        active_career = db.get_user_career(user_id)
        if active_career:
            st.caption(f"🎯 Target: **{active_career['career_name']}**")
        else:
            st.caption("🎯 Target: *No career selected*")

        st.divider()

        # Navigation Options
        pages_nav = [
            "Dashboard",
            "Profile",
            "Skills",
            "Projects",
            "Target Career",
            "Career Analysis",
            "Roadmap",
            "DSA Practice",
            "Interview Preparation",
            "Progress"
        ]

        icons = {
            "Dashboard": "📊",
            "Profile": "👤",
            "Skills": "🛠️",
            "Projects": "🚀",
            "Target Career": "🎯",
            "Career Analysis": "🔍",
            "Roadmap": "🗺️",
            "DSA Practice": "💻",
            "Interview Preparation": "🎙️",
            "Progress": "📈"
        }

        # Sidebar navigation radio
        current = st.session_state.get("current_page", "Dashboard")
        if current not in pages_nav:
            current = "Dashboard"

        selected = st.radio(
            "Navigation",
            pages_nav,
            index=pages_nav.index(current),
            format_func=lambda p: f"{icons.get(p, '•')} {p}",
            label_visibility="collapsed"
        )
        st.session_state["current_page"] = selected

        st.divider()

        # AI Status in Sidebar
        status = ai_service.check_ai_status()
        if status["available"]:
            st.caption("🟢 AI Service: Online (OpenAI API)")
        else:
            st.caption("🟡 AI Service: Local Rule-Based Fallback")

        # Logout button
        if st.button("🚪 Sign Out", use_container_width=True):
            logout_user()

    # Route to selected page
    page = st.session_state["current_page"]

    if page == "Dashboard":
        render_dashboard(user)
    elif page == "Profile":
        render_profile(user)
    elif page == "Skills":
        render_skills(user)
    elif page == "Projects":
        render_projects(user)
    elif page == "Target Career":
        render_career(user)
    elif page == "Career Analysis":
        render_analysis(user)
    elif page == "Roadmap":
        render_roadmap(user)
    elif page == "DSA Practice":
        render_dsa(user)
    elif page == "Interview Preparation":
        render_interviews(user)
    elif page == "Progress":
        render_progress(user)

def main():
    if st.session_state["user"] is None:
        render_auth()
    else:
        render_app()

if __name__ == "__main__":
    main()
