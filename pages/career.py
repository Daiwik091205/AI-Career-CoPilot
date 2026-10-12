"""
pages/career.py
Target Career selection and exploration page.
Allows students to browse career tracks, inspect industry requirements,
and set their active target career goal.
"""

import streamlit as st
import database as db
import career_data

def render_career(user: dict):
    st.title("🎯 Target Career Exploration & Goal Setting")
    user_id = user["id"]

    st.markdown("""
Select your target career path. Each career includes industry-standard required competencies,
recommended skills, interview topics, and suggested project architectures.
""")

    # Current Active Target Career
    active_career = db.get_user_career(user_id)
    if active_career:
        st.success(f"🏆 Current Active Career Goal: **{active_career['career_name']}** (Selected: {active_career.get('selected_at', '')[:10]})")
    else:
        st.warning("⚠️ You haven't set an active career goal yet. Choose one below to calibrate your readiness.")

    all_careers = career_data.get_all_careers()
    career_names = career_data.get_career_names()

    # Dropdown to explore
    selected_name = st.selectbox(
        "Choose a Career Track to Explore:",
        career_names,
        index=career_names.index(active_career["career_name"]) if active_career and active_career["career_name"] in career_names else 0
    )

    career_info = career_data.get_career(selected_name)
    if not career_info:
        st.error("Career information not found.")
        return

    st.divider()

    # Detailed Career Card
    st.subheader(f"💼 {career_info['title']}")
    st.caption(f"**Domain:** {career_info['domain']}")
    st.write(career_info["description"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Core Required Skills")
        st.caption("Fundamental competencies tested in hiring loops:")
        for r_skill in career_info["required_skills"]:
            st.markdown(f"- **{r_skill}**")

        st.markdown("### 🌟 Recommended / Nice-to-Have")
        for rec in career_info.get("recommended_skills", []):
            st.markdown(f"- {rec}")

    with col2:
        st.markdown("### 🎙️ Core Interview Focus Areas")
        for topic in career_info.get("key_interview_topics", []):
            st.markdown(f"- 🔹 {topic}")

        st.markdown("### 💡 Recommended Portfolio Concepts")
        for proj in career_info.get("recommended_project_ideas", []):
            st.markdown(f"- 🚀 *{proj}*")

    st.divider()

    # Action button to set as active career
    is_currently_active = active_career and active_career["career_name"] == selected_name
    if st.button(
        "✅ Set as My Target Career Goal",
        type="primary",
        disabled=bool(is_currently_active),
        use_container_width=True
    ):
        db.set_user_career(user_id, selected_name, career_info["required_skills"])
        st.success(f"🎯 Target career set to **{selected_name}**! Proceed to **Career Gap Analysis** to calculate your readiness.")
        st.rerun()

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_career(st.session_state["user"])
