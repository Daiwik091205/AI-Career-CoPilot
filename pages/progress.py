"""
pages/progress.py
Comprehensive Progress Tracking & Adaptive Career Analytics page.
Monitors multi-dimensional student advancement across skills, projects,
DSA practice, mock interviews, and roadmap milestone completion.
"""

import streamlit as st
import database as db
import ai_service
import career_data
import dsa_data
from utils.helpers import format_timestamp, get_readiness_badge_color

def render_progress(user: dict):
    st.title("📈 Comprehensive Progress & Adaptive Analytics")
    user_id = user["id"]

    # Gather data
    stats = db.get_user_dashboard_stats(user_id)
    user_career = db.get_user_career(user_id)
    career_name = user_career["career_name"] if user_career else "Software Developer"
    skills = db.get_user_skills(user_id)
    projects = db.get_user_projects(user_id)
    roadmap = db.get_user_roadmap(user_id)
    dsa_progress = db.get_user_dsa_progress(user_id)
    interview_history = db.get_user_interview_history(user_id)
    completed_milestones = db.get_completed_items(user_id, "roadmap_item")

    st.markdown(f"""
Tracking your holistic career readiness for **{career_name}**.
As you complete questions, add skills, or check off roadmap items, the adaptive engine recalibrates your career standing.
""")

    # Adaptive Recalibration Trigger
    col_recal1, col_recal2 = st.columns([2.5, 1])
    with col_recal1:
        if roadmap and roadmap.get("readiness_score") is not None:
            r_score = roadmap["readiness_score"]
            b_color = get_readiness_badge_color(r_score)
            st.markdown(f"Current Readiness Standing: <strong style='color:{b_color}; font-size:1.2rem;'>{r_score}%</strong> (Target: {career_name})", unsafe_allow_html=True)
        else:
            st.caption("No readiness score calculated yet. Run an analysis to start tracking.")
    with col_recal2:
        if st.button("🔄 Trigger Adaptive Sync", type="primary", use_container_width=True):
            if not user_career:
                st.warning("Please set a career goal first.")
            else:
                with st.spinner("Synchronizing progress metrics into adaptive roadmap..."):
                    cinfo = career_data.get_career(career_name) or {}
                    creqs = user_career.get("required_skills_list") or cinfo.get("required_skills", [])
                    profile = db.get_profile(user_id)

                    gap_data = ai_service.generate_skill_gap_analysis(profile, skills, projects, career_name, creqs)
                    read_data = ai_service.calculate_readiness_assessment(
                        profile, skills, projects, career_name, creqs, dsa_progress, interview_history
                    )
                    score = read_data.get("readiness_score", 50)
                    gap_data["breakdown"] = read_data.get("breakdown", {})
                    gap_data["key_strengths"] = read_data.get("key_strengths", [])
                    gap_data["critical_gaps"] = read_data.get("critical_gaps", [])

                    new_road = ai_service.generate_roadmap(profile, skills, projects, career_name, gap_data, score)

                    db.save_user_roadmap(
                        user_id=user_id,
                        career_id=user_career["id"],
                        gap_analysis=gap_data,
                        readiness_score=score,
                        roadmap_phases=new_road.get("phases", []),
                        is_adaptive=True
                    )
                    st.success("Adaptive engine synchronized with latest progress!")
                    st.rerun()

    st.divider()

    # Progress Columns: Pillar 1 & 2
    c_p1, c_p2 = st.columns(2)

    with c_p1:
        st.subheader("🛠️ Technical Competency Coverage")
        st.metric("Total Skills Logged", len(skills))
        if skills:
            beg = sum(1 for s in skills if s["proficiency"] == "Beginner")
            inter = sum(1 for s in skills if s["proficiency"] == "Intermediate")
            adv = sum(1 for s in skills if s["proficiency"] == "Advanced")

            st.write(f"- 🟢 **Advanced:** {adv}")
            st.write(f"- 🟡 **Intermediate:** {inter}")
            st.write(f"- ⚪ **Beginner:** {beg}")

            # Skill tags
            st.write("**Top Skills:**")
            st.markdown(" ".join([f"`{s['skill_name']} ({s['proficiency'][:3]})`" for s in skills[:8]]))
        else:
            st.info("No skills registered yet.")

    with c_p2:
        st.subheader("🚀 Portfolio Projects")
        st.metric("Projects Documented", len(projects))
        if projects:
            for p in projects[:3]:
                st.markdown(f"- **{p['project_name']}** ({len(p.get('extracted_skills_list', []))} skills)")
        else:
            st.info("No projects added yet.")

    st.divider()

    # Progress Columns: Pillar 3 & 4
    c_p3, c_p4 = st.columns(2)

    with c_p3:
        st.subheader("💻 DSA Topic Mastery")
        all_dsa = dsa_data.get_all_dsa_questions()
        solved_total = sum(1 for q in all_dsa if dsa_progress.get(q["id"], {}).get("status") == "solved")
        st.metric("DSA Problems Solved", f"{solved_total} / {len(all_dsa)}")
        st.progress(solved_total / len(all_dsa) if all_dsa else 0.0)

        # Break down by topic
        topic_counts = {}
        for q in all_dsa:
            top = q["topic"]
            topic_counts[top] = topic_counts.get(top, {"total": 0, "solved": 0})
            topic_counts[top]["total"] += 1
            if dsa_progress.get(q["id"], {}).get("status") == "solved":
                topic_counts[top]["solved"] += 1

        with st.expander("View DSA Topic Breakdown"):
            for t_name, t_data in topic_counts.items():
                s = t_data["solved"]
                tot = t_data["total"]
                st.write(f"• **{t_name}**: {s}/{tot}")
                st.progress(s / tot)

    with c_p4:
        st.subheader("🎙️ Mock Interview Trajectory")
        if interview_history:
            total_int = len(interview_history)
            avg_sc = round(sum(h["score"] for h in interview_history) / total_int, 1)
            st.metric("Questions Attempted", total_int)
            st.metric("Mean Score", f"{avg_sc} / 10")

            # Scores trend
            scores = [h["score"] for h in reversed(interview_history)]
            st.caption("Recent Performance Scores (out of 10):")
            st.bar_chart(scores)
        else:
            st.info("No interview practices recorded yet.")

    st.divider()

    # Pillar 5: Completed Roadmap Checklist
    st.subheader("🗺️ Roadmap Milestones Completed")
    if completed_milestones:
        st.write(f"Total Completed Items: **{len(completed_milestones)}**")
        for item_name in completed_milestones:
            st.markdown(f"- ✅ **{item_name}**")
    else:
        st.info("Check off completed milestones in the **Personalized Roadmap** tab to track them here.")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_progress(st.session_state["user"])
