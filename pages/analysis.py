"""
pages/analysis.py
AI Skill-Gap Analysis & Readiness Assessment page.
Analyzes student's academic profile, verified skills, and practical projects
against target career requirements to compute an estimated readiness score and categorize gaps.
"""

import streamlit as st
import database as db
import ai_service
import career_data
from utils.helpers import get_readiness_badge_color

def render_analysis(user: dict):
    st.title("🔍 AI Skill-Gap Analysis & Readiness Score")
    user_id = user["id"]

    user_career = db.get_user_career(user_id)
    if not user_career:
        st.warning("⚠️ No target career selected. Please select a career goal in the **Target Career** tab before running an analysis.")
        return

    career_name = user_career["career_name"]
    career_info = career_data.get_career(career_name) or {}
    career_reqs = user_career.get("required_skills_list") or career_info.get("required_skills", [])

    profile = db.get_profile(user_id)
    skills = db.get_user_skills(user_id)
    projects = db.get_user_projects(user_id)
    dsa_progress = db.get_user_dsa_progress(user_id)
    interview_progress = db.get_user_interview_history(user_id)

    st.markdown(f"""
Comparing your profile against **{career_name}** requirements.
- Target Core Skills: **{len(career_reqs)}**
- Your Logged Skills: **{len(skills)}**
- Your Projects: **{len(projects)}**
- DSA Solved: **{sum(1 for v in dsa_progress.values() if v.get('status') == 'solved')}**
""")

    # AI Status Notice
    ai_status = ai_service.check_ai_status()
    if not ai_status["available"]:
        st.caption(f"ℹ️ {ai_status['message']}")

    # Analysis Action Button
    col_act, _ = st.columns([1.5, 2])
    with col_act:
        run_btn = st.button("🚀 Run Comprehensive AI Gap Analysis", type="primary", use_container_width=True)

    # Check for existing analysis
    existing_roadmap = db.get_user_roadmap(user_id)
    gap_data = existing_roadmap.get("gap_analysis_data", {}) if existing_roadmap else {}
    readiness_score = existing_roadmap.get("readiness_score") if existing_roadmap else None

    if run_btn:
        with st.spinner("🤖 Evaluating skill alignments, portfolio depth, and estimating readiness score..."):
            # 1. Skill Gap Analysis
            gap_data = ai_service.generate_skill_gap_analysis(
                profile=profile,
                skills=skills,
                projects=projects,
                career_name=career_name,
                career_reqs=career_reqs
            )

            # 2. Readiness Assessment
            readiness_data = ai_service.calculate_readiness_assessment(
                profile=profile,
                skills=skills,
                projects=projects,
                career_name=career_name,
                career_reqs=career_reqs,
                dsa_progress=dsa_progress,
                interview_progress=interview_progress
            )
            readiness_score = readiness_data.get("readiness_score", 50)
            gap_data["breakdown"] = readiness_data.get("breakdown", {})
            gap_data["key_strengths"] = readiness_data.get("key_strengths", [])
            gap_data["critical_gaps"] = readiness_data.get("critical_gaps", [])
            gap_data["verdict_summary"] = readiness_data.get("verdict_summary", "")

            # 3. Generate initial/adapted roadmap
            roadmap_data = ai_service.generate_roadmap(
                profile=profile,
                skills=skills,
                projects=projects,
                career_name=career_name,
                gap_analysis=gap_data,
                readiness_score=readiness_score
            )

            # 4. Save to Database
            db.save_user_roadmap(
                user_id=user_id,
                career_id=user_career["id"],
                gap_analysis=gap_data,
                readiness_score=readiness_score,
                roadmap_phases=roadmap_data.get("phases", []),
                is_adaptive=True
            )
            st.success("✅ Analysis completed and saved to your profile and roadmap!")
            st.rerun()

    if not gap_data:
        st.info("Click the button above to run your personalized Skill-Gap Analysis.")
        return

    st.divider()

    # --- READINESS SCORE BANNER ---
    st.subheader("⚡ Estimated Career Readiness Score")
    badge_color = get_readiness_badge_color(readiness_score)

    st.markdown(
        f"""
        <div style="background-color: #fbfcfd; border-left: 8px solid {badge_color}; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
            <div style="display: flex; align-items: baseline; gap: 15px;">
                <h1 style="margin: 0; color: {badge_color}; font-size: 2.8rem;">{readiness_score} / 100</h1>
                <span style="font-size: 1.1rem; color: #495057; font-weight: 500;">Career Readiness Estimate</span>
            </div>
            <p style="margin: 8px 0 0 0; font-size: 0.85rem; color: #6c757d;">
                ⚠️ <em>Important Disclaimer: This score is an AI-generated learning guidance estimate based on your provided academic profile, verified skills, and project experience. It is not an objective measurement of hiring employability.</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.progress(readiness_score / 100)

    # Contributing Factors
    breakdown = gap_data.get("breakdown", {})
    if breakdown:
        st.write("#### 📊 Contributing Factors to Readiness Score:")
        bc1, bc2, bc3, bc4 = st.columns(4)
        with bc1:
            st.metric("Skill Coverage", f"{breakdown.get('skill_coverage_score', 0)}%")
        with bc2:
            st.metric("Project Depth", f"{breakdown.get('project_experience_score', 0)}%")
        with bc3:
            st.metric("DSA Solved", f"{breakdown.get('dsa_preparedness_score', 0)}%")
        with bc4:
            st.metric("Interview Drill", f"{breakdown.get('interview_performance_score', 0)}%")

    if gap_data.get("summary"):
        st.info(f"**Executive Summary:** {gap_data['summary']}")

    st.divider()

    # --- CATEGORIZED GAP TABS ---
    st.subheader("📑 Categorized Skills & Priorities")
    tab_miss, tab_pri, tab_part, tab_str, tab_proj, tab_top = st.tabs([
        "🔴 Missing Skills",
        "⚡ Priority Focus",
        "🟡 Partial Skills",
        "🟢 Strong Skills",
        "🚀 Recommended Projects",
        "📚 Recommended Topics"
    ])

    with tab_miss:
        missing = gap_data.get("missing_skills", [])
        if missing:
            st.markdown(f"Found **{len(missing)}** required competencies with no recorded experience:")
            for m in missing:
                with st.container():
                    st.markdown(f"#### 🔴 {m.get('skill')}")
                    st.markdown(f"**Why it matters:** {m.get('why_it_matters')}")
                    st.markdown("---")
        else:
            st.success("No missing skills identified! Great coverage.")

    with tab_pri:
        prioritized = gap_data.get("prioritized_skills", [])
        if prioritized:
            st.markdown("Skills recommended for immediate learning focus:")
            for p in prioritized:
                st.markdown(f"- ⚡ **{p.get('skill')}** (Priority: `{p.get('priority', 'High')}`): {p.get('why_it_matters')}")
        else:
            st.info("No urgent priorities flagged.")

    with tab_part:
        partial = gap_data.get("partial_skills", [])
        if partial:
            st.markdown("Skills you have touched upon, but need deeper practical application:")
            for p in partial:
                st.markdown(f"- 🟡 **{p.get('skill')}** [Proficiency: *{p.get('proficiency')}*]: {p.get('reason')}")
        else:
            st.info("No partial skills listed.")

    with tab_str:
        strong = gap_data.get("strong_skills", [])
        if strong:
            st.markdown("Competencies where you demonstrate solid capability or project evidence:")
            for s in strong:
                st.markdown(f"- 🟢 **{s.get('skill')}** [Proficiency: *{s.get('proficiency')}*]: {s.get('reason')}")
        else:
            st.info("No strong skills logged yet. Add more verified skills or projects to boost this.")

    with tab_proj:
        rec_projects = gap_data.get("recommended_projects", [])
        if rec_projects:
            st.markdown("Building these projects will bridge your primary technical gaps:")
            for rp in rec_projects:
                with st.expander(f"🛠️ {rp.get('title')}", expanded=True):
                    st.write(rp.get("description"))
                    skills_targeted = rp.get("skills_targeted", [])
                    if skills_targeted:
                        st.markdown("**Skills Targeted:** " + " ".join([f"`{sk}`" for sk in skills_targeted]))
        else:
            st.info("No specific project recommendations available.")

    with tab_top:
        topics = gap_data.get("recommended_learning_topics", [])
        if topics:
            for t in topics:
                st.markdown(f"- 📖 **{t}**")
        else:
            st.info("No learning topics listed.")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_analysis(st.session_state["user"])
