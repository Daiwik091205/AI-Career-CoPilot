"""
pages/projects.py
Student Projects management page. Allows students to log technical projects,
trigger AI skill extraction from descriptions, review/edit the extracted skills,
and save them to their portfolio.
"""

import streamlit as st
import database as db
import ai_service

def render_projects(user: dict):
    st.title("🚀 Portfolio Projects & Skill Extraction")
    user_id = user["id"]

    st.markdown("""
Log your practical and academic projects here. Our AI analyzes your project description to identify implied technical skills, frameworks, and architecture tools.
You have complete control to review and edit extracted skills before saving.
""")

    # Project Creation Form with AI Extraction
    with st.expander("➕ Add a New Project", expanded=True):
        proj_name = st.text_input("Project Title", placeholder="e.g. RFID Smart Door Lock System", key="new_proj_name")
        proj_desc = st.text_area(
            "Project Description",
            placeholder="e.g. Built an RFID-based door lock using Arduino and C++. Integrated an RC522 RFID reader with a servo motor and LCD display. Implemented master tag authorization stored in EEPROM.",
            height=120,
            key="new_proj_desc"
        )

        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            if st.button("🤖 Analyze & Extract Skills", use_container_width=True):
                if not proj_name.strip() or not proj_desc.strip():
                    st.error("Please provide both a project title and description.")
                else:
                    with st.spinner("AI is analyzing technical competencies..."):
                        extraction = ai_service.extract_project_skills(proj_name, proj_desc)
                        st.session_state["draft_extracted_skills"] = extraction.get("skills", [])
                        st.session_state["extraction_source"] = extraction.get("source", "ai")
                        st.session_state["draft_proj_name"] = proj_name
                        st.session_state["draft_proj_desc"] = proj_desc
                        st.success(f"Extracted {len(st.session_state['draft_extracted_skills'])} potential skills!")

        # Review & Edit Extracted Skills before saving
        if "draft_extracted_skills" in st.session_state and st.session_state.get("draft_proj_name") == proj_name:
            st.markdown("---")
            st.subheader("🧐 Review Extracted Technical Skills")
            st.caption("AI-extracted skills are shown below. Edit, remove, or add skills to accurately reflect what you built:")

            current_extracted_str = ", ".join(st.session_state["draft_extracted_skills"])
            user_reviewed_skills_str = st.text_input("Skills (comma-separated)", value=current_extracted_str, key="reviewed_skills_input")

            # Checkbox to also add to main skills profile
            add_to_profile = st.checkbox("Also automatically register these skills in my main Technical Skills inventory", value=True)

            if st.button("💾 Finalize & Save Project", type="primary", use_container_width=True):
                clean_skills = [s.strip() for s in user_reviewed_skills_str.split(",") if s.strip()]
                if not clean_skills:
                    st.error("Please include at least one technical skill.")
                else:
                    # Save project
                    db.add_project(user_id, proj_name, proj_desc, clean_skills)

                    # Optionally add to skills inventory
                    if add_to_profile:
                        for sk in clean_skills:
                            db.add_or_update_skill(user_id, sk, "Intermediate")

                    st.success(f"🎉 Project '{proj_name}' saved successfully!")
                    # Clean up draft state
                    del st.session_state["draft_extracted_skills"]
                    if "draft_proj_name" in st.session_state:
                        del st.session_state["draft_proj_name"]
                    st.rerun()

    st.divider()

    # Display Saved Projects
    st.subheader("📁 Saved Portfolio Projects")
    projects = db.get_user_projects(user_id)

    if not projects:
        st.info("No projects added yet. Add a project above to showcase your hands-on engineering capabilities.")
        return

    for proj in projects:
        with st.container():
            p_col1, p_col2 = st.columns([4, 1])
            with p_col1:
                st.markdown(f"### {proj['project_name']}")
                st.caption(f"Added on: {proj.get('created_at', '')[:10]}")
                st.write(proj["description"])

                skills_list = proj.get("extracted_skills_list", [])
                if skills_list:
                    st.markdown("**Associated Skills:**")
                    st.markdown(" ".join([f"`{s}`" for s in skills_list]))
            with p_col2:
                st.write("")
                st.write("")
                if st.button("🗑️ Remove", key=f"del_proj_{proj['id']}", use_container_width=True):
                    db.delete_project(user_id, proj["id"])
                    st.toast(f"Removed {proj['project_name']}")
                    st.rerun()
            st.markdown("---")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_projects(st.session_state["user"])
