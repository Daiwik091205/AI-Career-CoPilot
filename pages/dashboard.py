"""
pages/dashboard.py
Student Dashboard providing an integrated overview of target career,
readiness score estimate, skill gaps, projects, DSA progress, and interview preparation.
"""

import streamlit as st
import database as db
import career_data
from utils.helpers import get_readiness_badge_color

def render_dashboard(user: dict):
    st.title("📊 Student Career Dashboard")
    user_id = user["id"]
    username = user["username"]

    st.markdown(f"Welcome back, **{username}**! Here is an overview of your career preparation journey.")

    # Fetch relevant data
    stats = db.get_user_dashboard_stats(user_id)
    profile = db.get_profile(user_id)
    skills = db.get_user_skills(user_id)
    projects = db.get_user_projects(user_id)
    user_career = db.get_user_career(user_id)
    roadmap = db.get_user_roadmap(user_id)
    dsa_progress = db.get_user_dsa_progress(user_id)

    # Top KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Technical Skills", value=stats["skills_count"], help="Total verified skills added to profile")
    with c2:
        st.metric(label="Projects Logged", value=stats["projects_count"], help="Portfolio projects with extracted technical skills")
    with c3:
        st.metric(label="DSA Problems Solved", value=f"{stats['dsa_solved']} / 14", help="Solved algorithmic coding questions")
    with c4:
        st.metric(label="Interview Avg Score", value=f"{stats['avg_interview_score']} / 10", help="Average AI evaluation score on mock interviews")

    st.divider()

    # Active Career Target & Readiness Section
    col_career, col_readiness = st.columns([1.2, 1])

    with col_career:
        st.subheader("🎯 Target Career")
        if user_career:
            cname = user_career["career_name"]
            cinfo = career_data.get_career(cname) or {}
            st.success(f"### {cname}")
            st.caption(f"**Domain:** {cinfo.get('domain', 'Technology')} | **Selected:** {user_career.get('selected_at', '')[:10]}")
            st.write(cinfo.get("description", "Target career track."))

            reqs = user_career.get("required_skills_list", [])
            st.markdown(f"**Core Requirements ({len(reqs)} items):**")
            # Show required skills as badges
            st.markdown(" ".join([f"`{r}`" for r in reqs[:8]]) + ("..." if len(reqs) > 8 else ""))
        else:
            st.info("💡 You have not selected a target career yet.")
            st.write("Head over to the **Target Career** tab to choose a specialization such as *Software Developer*, *Data Scientist*, or *AI Engineer*.")

    with col_readiness:
        st.subheader("⚡ Career Readiness Assessment")
        if roadmap and roadmap.get("readiness_score") is not None:
            score = roadmap["readiness_score"]
            badge_color = get_readiness_badge_color(score)

            st.markdown(
                f"""
                <div style="background-color: #f8f9fa; border-left: 6px solid {badge_color}; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
                    <h2 style="margin: 0; color: {badge_color};">{score} / 100</h2>
                    <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #6c757d;">
                        Estimated Career Readiness (AI Approximation)
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.progress(score / 100)

            # Show contributing factors
            gap_data = roadmap.get("gap_analysis_data", {})
            breakdown = gap_data.get("breakdown")
            if breakdown:
                st.caption("Readiness Contributing Factors:")
                st.write(f"- Skill Coverage: **{breakdown.get('skill_coverage_score', 0)}%**")
                st.write(f"- Project Experience: **{breakdown.get('project_experience_score', 0)}%**")
                st.write(f"- DSA Preparedness: **{breakdown.get('dsa_preparedness_score', 0)}%**")
                st.write(f"- Interview Score: **{breakdown.get('interview_performance_score', 0)}%**")
        else:
            st.warning("No Career Readiness Score generated yet.")
            st.caption("Once you configure your skills and target career, run a **Career Gap Analysis** to generate your readiness score and personalized roadmap.")

    st.divider()

    # Skill Gap & Roadmap Progress Section
    col_gaps, col_roadmap = st.columns(2)

    with col_gaps:
        st.subheader("🔍 Skill Gaps Summary")
        if roadmap and roadmap.get("gap_analysis_data"):
            gaps = roadmap["gap_analysis_data"]
            strong = gaps.get("strong_skills", [])
            missing = gaps.get("missing_skills", [])
            partial = gaps.get("partial_skills", [])

            t1, t2, t3 = st.tabs([f"Missing ({len(missing)})", f"Partial ({len(partial)})", f"Strong ({len(strong)})"])
            with t1:
                if missing:
                    for m in missing[:5]:
                        st.markdown(f"- 🔴 **{m.get('skill')}**: {m.get('why_it_matters')}")
                else:
                    st.success("No critical missing skills detected!")
            with t2:
                if partial:
                    for p in partial[:5]:
                        st.markdown(f"- 🟡 **{p.get('skill')}** ({p.get('proficiency')}): {p.get('reason')}")
                else:
                    st.info("No partial skills listed.")
            with t3:
                if strong:
                    for s in strong[:5]:
                        st.markdown(f"- 🟢 **{s.get('skill')}** ({s.get('proficiency')}): {s.get('reason')}")
                else:
                    st.info("No strong skills logged yet.")
        else:
            st.info("Run **Career Gap Analysis** to view your categorized skill strengths and gaps.")

    with col_roadmap:
        st.subheader("🗺️ Roadmap Progress")
        if roadmap and roadmap.get("roadmap_phases"):
            phases = roadmap["roadmap_phases"]
            completed_items = db.get_completed_items(user_id, "roadmap_item")

            total_items = 0
            for phase in phases:
                total_items += len(phase.get("items", []))

            done_count = len(completed_items)
            pct = int((done_count / total_items * 100)) if total_items > 0 else 0

            st.write(f"Milestones Completed: **{done_count} / {total_items}** ({pct}%)")
            st.progress(pct / 100 if total_items > 0 else 0.0)

            for phase in phases:
                with st.expander(f"{phase.get('phase_name', 'Phase')} ({phase.get('estimated_duration', '')})"):
                    st.caption(phase.get("objective", ""))
                    for item in phase.get("items", []):
                        it_name = item.get("topic", "")
                        is_done = it_name in completed_items
                        st.write(f"{'✅' if is_done else '⬜'} **{it_name}** - {item.get('description', '')}")
        else:
            st.info("No roadmap generated yet. Generate your personalized roadmap under **Personalized Roadmap**.")

    st.divider()

    # DSA & Interview Preparation Section
    col_dsa_box, col_int_box = st.columns(2)

    with col_dsa_box:
        st.subheader("💻 DSA Practice By Topic")
        import dsa_data
        all_dsa = dsa_data.get_all_dsa_questions()
        topic_counts = {}
        for q in all_dsa:
            topic = q["topic"]
            topic_counts[topic] = topic_counts.get(topic, {"total": 0, "solved": 0})
            topic_counts[topic]["total"] += 1
            if dsa_progress.get(q["id"], {}).get("status") == "solved":
                topic_counts[topic]["solved"] += 1

        for top, data in list(topic_counts.items())[:6]:
            solved = data["solved"]
            total = data["total"]
            st.write(f"**{top}**: {solved}/{total} solved")
            st.progress(solved / total)
        st.caption("Visit **DSA Practice** to solve questions across all 14 topics with in-app test verification.")

    with col_int_box:
        st.subheader("🎙️ Mock Interview Preparation")
        history = db.get_user_interview_history(user_id)
        if history:
            st.write(f"Total Interview Questions Answered: **{len(history)}**")
            for h in history[:3]:
                st.markdown(f"- **Q ID `{h['question_id']}`**: Score **{h['score']}/10** ({h.get('completed_at', '')[:10]})")
                st.caption(f"Feedback snippet: {h.get('ai_feedback', '')[:120]}...")
        else:
            st.info("No interview attempts logged yet. Rehearse technical & behavioral questions in **Interview Preparation**.")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_dashboard(st.session_state["user"])
