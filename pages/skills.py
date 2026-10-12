"""
pages/skills.py
Technical skills management page allowing students to add, view, update,
and delete technical skills with proficiency ratings.
"""

import streamlit as st
import database as db

POPULAR_SKILLS = [
    "Python", "Java", "C++", "JavaScript", "SQL", "Data Structures & Algorithms",
    "Git & Version Control", "Docker", "Machine Learning", "Deep Learning",
    "React.js", "FastAPI", "Django", "PostgreSQL", "MongoDB", "Linux",
    "REST APIs", "Object-Oriented Programming (OOP)", "Pandas & NumPy", "Kubernetes"
]

def render_skills(user: dict):
    st.title("🛠️ Technical Skills Inventory")
    user_id = user["id"]

    st.markdown("Record your technical competencies and self-assessed proficiency levels. These skills are evaluated against your target career requirements.")

    # Two columns: Add Skill form & Quick suggestions
    col_add, col_suggest = st.columns([1.2, 1])

    with col_add:
        st.subheader("➕ Add / Update a Skill")
        with st.form("add_skill_form"):
            skill_name = st.text_input("Skill Name", placeholder="e.g. Python, Docker, PyTorch")
            proficiency = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            submitted = st.form_submit_button("Save Skill", use_container_width=True)

            if submitted:
                if not skill_name.strip():
                    st.error("Please enter a valid skill name.")
                else:
                    db.add_or_update_skill(user_id, skill_name.strip(), proficiency)
                    st.success(f"✅ Saved '{skill_name.strip()}' as **{proficiency}**!")
                    st.rerun()

    with col_suggest:
        st.subheader("⚡ Quick Add Common Skills")
        st.caption("Click to pre-fill a popular industry skill:")
        existing_skills = [s["skill_name"].lower() for s in db.get_user_skills(user_id)]

        quick_cols = st.columns(2)
        for idx, p_skill in enumerate(POPULAR_SKILLS[:10]):
            with quick_cols[idx % 2]:
                is_added = p_skill.lower() in existing_skills
                label = f"✓ {p_skill}" if is_added else f"+ {p_skill}"
                if st.button(label, key=f"quick_{p_skill}", disabled=is_added, use_container_width=True):
                    db.add_or_update_skill(user_id, p_skill, "Intermediate")
                    st.success(f"Added {p_skill} (Intermediate)")
                    st.rerun()

    st.divider()

    # View and Manage Existing Skills
    st.subheader("📋 Your Registered Skills")
    skills = db.get_user_skills(user_id)

    if not skills:
        st.info("You haven't added any skills yet. Add your core languages, frameworks, or tools above!")
        return

    # Counts by proficiency
    beg_count = sum(1 for s in skills if s["proficiency"] == "Beginner")
    int_count = sum(1 for s in skills if s["proficiency"] == "Intermediate")
    adv_count = sum(1 for s in skills if s["proficiency"] == "Advanced")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Skills", len(skills))
    m2.metric("Beginner", beg_count)
    m3.metric("Intermediate", int_count)
    m4.metric("Advanced", adv_count)

    # Search filter
    search = st.text_input("🔍 Filter skills...", placeholder="Type to search your skills...")
    filtered_skills = [s for s in skills if search.lower() in s["skill_name"].lower()] if search else skills

    st.markdown("---")

    # Table / Cards for editing & deleting
    for skill in filtered_skills:
        scol1, scol2, scol3, scol4 = st.columns([2, 1.5, 1, 1])

        with scol1:
            st.markdown(f"**{skill['skill_name']}**")
            st.caption(f"Last updated: {skill.get('updated_at', '')[:10]}")

        with scol2:
            new_prof = st.selectbox(
                "Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(skill["proficiency"]),
                key=f"prof_{skill['id']}",
                label_visibility="collapsed"
            )

        with scol3:
            if st.button("Update", key=f"upd_{skill['id']}", use_container_width=True):
                if new_prof != skill["proficiency"]:
                    db.add_or_update_skill(user_id, skill["skill_name"], new_prof)
                    st.toast(f"Updated {skill['skill_name']} to {new_prof}!")
                    st.rerun()

        with scol4:
            if st.button("🗑️ Delete", key=f"del_{skill['id']}", type="secondary", use_container_width=True):
                db.delete_skill(user_id, skill["id"])
                st.toast(f"Removed {skill['skill_name']}")
                st.rerun()

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_skills(st.session_state["user"])
