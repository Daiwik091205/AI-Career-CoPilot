"""
pages/roadmap.py
Personalized & Adaptive Roadmap page.
Displays a 4-phase structured learning path tailored to the student's current profile,
allows tracking milestone completion, and dynamically adapts as the student learns.
"""

import streamlit as st
import database as db
import ai_service
import career_data

def render_roadmap(user: dict):
    st.title("🗺️ Personalized & Adaptive Preparation Roadmap")
    user_id = user["id"]

    user_career = db.get_user_career(user_id)
    if not user_career:
        st.warning("⚠️ Please select a target career in the **Target Career** tab before generating a roadmap.")
        return

    career_name = user_career["career_name"]
    career_info = career_data.get_career(career_name) or {}
    career_reqs = user_career.get("required_skills_list") or career_info.get("required_skills", [])

    roadmap_data = db.get_user_roadmap(user_id)
    profile = db.get_profile(user_id)
    skills = db.get_user_skills(user_id)
    projects = db.get_user_projects(user_id)
    dsa_progress = db.get_user_dsa_progress(user_id)
    interview_progress = db.get_user_interview_history(user_id)

    st.markdown(f"""
Your dynamic learning roadmap for **{career_name}**.
This roadmap is calibrated to skip foundational skills you have already demonstrated,
focus on your specific skill gaps, and adapt as you progress.
""")

    # Adaptive Roadmap Regeneration Trigger
    col_hdr1, col_hdr2 = st.columns([2, 1.2])
    with col_hdr1:
        if roadmap_data and roadmap_data.get("is_adaptive"):
            st.caption("✨ *Adaptive Engine Active: Ready to evolve as you add skills, projects, or practice DSA.*")
    with col_hdr2:
        adapt_btn = st.button("🔄 Adapt & Regenerate Roadmap", type="secondary", use_container_width=True)

    if adapt_btn:
        with st.spinner("🤖 Recalibrating roadmap based on latest skills, DSA progress, and interview performance..."):
            gap_data = ai_service.generate_skill_gap_analysis(
                profile=profile, skills=skills, projects=projects, career_name=career_name, career_reqs=career_reqs
            )
            readiness_data = ai_service.calculate_readiness_assessment(
                profile=profile, skills=skills, projects=projects, career_name=career_name, career_reqs=career_reqs,
                dsa_progress=dsa_progress, interview_progress=interview_progress
            )
            readiness_score = readiness_data.get("readiness_score", 50)
            gap_data["breakdown"] = readiness_data.get("breakdown", {})
            gap_data["key_strengths"] = readiness_data.get("key_strengths", [])
            gap_data["critical_gaps"] = readiness_data.get("critical_gaps", [])

            new_roadmap = ai_service.generate_roadmap(
                profile=profile, skills=skills, projects=projects, career_name=career_name,
                gap_analysis=gap_data, readiness_score=readiness_score
            )

            db.save_user_roadmap(
                user_id=user_id,
                career_id=user_career["id"],
                gap_analysis=gap_data,
                readiness_score=readiness_score,
                roadmap_phases=new_roadmap.get("phases", []),
                is_adaptive=True
            )
            st.success("🎉 Roadmap successfully updated and adapted!")
            st.rerun()

    if not roadmap_data or not roadmap_data.get("roadmap_phases"):
        st.info("No roadmap generated yet. Head over to **Career Gap Analysis** to run your analysis and initialize your roadmap, or click the button above.")
        return

    phases = roadmap_data["roadmap_phases"]
    completed_items = db.get_completed_items(user_id, "roadmap_item")

    # Overall completion metric
    all_milestones = []
    for ph in phases:
        for it in ph.get("items", []):
            all_milestones.append(it.get("topic", ""))

    total_count = len(all_milestones)
    done_count = len([m for m in all_milestones if m in completed_items])
    pct = int((done_count / total_count * 100)) if total_count > 0 else 0

    st.divider()
    st.subheader(f"📊 Roadmap Progress: {done_count} / {total_count} Milestones Completed ({pct}%)")
    st.progress(pct / 100 if total_count > 0 else 0.0)

    st.markdown("---")

    # Render each phase
    for idx, phase in enumerate(phases, start=1):
        phase_title = phase.get("phase_name", f"Phase {idx}")
        duration = phase.get("estimated_duration", "2-3 weeks")
        objective = phase.get("objective", "")
        items = phase.get("items", [])

        # Count completed in this phase
        phase_done = sum(1 for it in items if it.get("topic", "") in completed_items)
        badge = "✅ COMPLETED" if (len(items) > 0 and phase_done == len(items)) else f"{phase_done}/{len(items)} Done"

        with st.expander(f"📍 {phase_title}  •  ⏱️ {duration}  •  [{badge}]", expanded=(phase_done < len(items) or idx == 1)):
            if objective:
                st.caption(f"**Phase Objective:** {objective}")

            for item_idx, item in enumerate(items):
                topic = item.get("topic", "")
                desc = item.get("description", "")
                res = item.get("learning_resource", "")

                c_check, c_content = st.columns([0.08, 0.92])

                is_checked = topic in completed_items
                with c_check:
                    new_checked = st.checkbox(
                        "",
                        value=is_checked,
                        key=f"chk_road_{idx}_{item_idx}_{topic[:10]}",
                        label_visibility="collapsed"
                    )

                if new_checked != is_checked:
                    db.toggle_completed_item(user_id, "roadmap_item", topic, new_checked)
                    st.rerun()

                with c_content:
                    st.markdown(f"**{topic}**" if not new_checked else f"~~**{topic}**~~ *(Completed)*")
                    if desc:
                        st.write(desc)
                    if res:
                        st.caption(f"🔗 Resource Focus: `{res}`")

            st.write("")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_roadmap(st.session_state["user"])
