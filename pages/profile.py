"""
pages/profile.py
Student Profile management page allowing students to view and update
education, degree, branch, year/semester, experience, interests, and career preferences.
"""

import streamlit as st
import database as db

def render_profile(user: dict):
    st.title("👤 Student Academic & Professional Profile")
    user_id = user["id"]

    st.markdown("Keep your academic details and career aspirations up to date. The AI uses this context to tailor your readiness assessment and roadmap.")

    # Fetch existing profile
    profile = db.get_profile(user_id)

    with st.form("profile_form"):
        st.subheader("🎓 Academic Information")
        c1, c2 = st.columns(2)
        with c1:
            education_level = st.selectbox(
                "Education Level",
                ["Undergraduate (B.Tech / B.E. / B.Sc / BCA)", "Postgraduate (M.Tech / M.Sc / MCA)", "Diploma", "Doctorate"],
                index=["Undergraduate (B.Tech / B.E. / B.Sc / BCA)", "Postgraduate (M.Tech / M.Sc / MCA)", "Diploma", "Doctorate"].index(
                    profile.get("education", "Undergraduate (B.Tech / B.E. / B.Sc / BCA)")
                ) if profile.get("education") in ["Undergraduate (B.Tech / B.E. / B.Sc / BCA)", "Postgraduate (M.Tech / M.Sc / MCA)", "Diploma", "Doctorate"] else 0
            )
            degree = st.text_input("Degree Title", value=profile.get("degree", "B.Tech"), placeholder="e.g. B.Tech in Computer Science")
        with c2:
            branch = st.text_input("Major / Branch", value=profile.get("branch", "Computer Science & Engineering"), placeholder="e.g. Information Technology / AI & Data Science")
            year_semester = st.selectbox(
                "Current Academic Standing",
                ["1st Year (Sem 1-2)", "2nd Year (Sem 3-4)", "3rd Year (Sem 5-6)", "4th Year (Sem 7-8)", "Recent Graduate", "Working Professional"],
                index=["1st Year (Sem 1-2)", "2nd Year (Sem 3-4)", "3rd Year (Sem 5-6)", "4th Year (Sem 7-8)", "Recent Graduate", "Working Professional"].index(
                    profile.get("year_semester", "3rd Year (Sem 5-6)")
                ) if profile.get("year_semester") in ["1st Year (Sem 1-2)", "2nd Year (Sem 3-4)", "3rd Year (Sem 5-6)", "4th Year (Sem 7-8)", "Recent Graduate", "Working Professional"] else 2
            )

        st.divider()
        st.subheader("💼 Experience & Background")
        experience = st.text_area(
            "Internships, Research, or Work Experience",
            value=profile.get("experience", ""),
            placeholder="e.g. Completed a 2-month summer internship building REST APIs with Python & FastAPI. Collaborated with a team of 4 using Git and agile sprints.",
            help="Detail any internships, campus roles, freelance projects, or research papers."
        )

        st.divider()
        st.subheader("💡 Interests & Career Goals")
        c3, c4 = st.columns(2)
        with c3:
            interests = st.text_area(
                "Technical Interests & Passions",
                value=profile.get("interests", ""),
                placeholder="e.g. Distributed backend systems, Natural Language Processing, Machine Learning, Cloud Architecture.",
                help="Topics you enjoy studying or building in your free time."
            )
        with c4:
            career_preferences = st.text_area(
                "Target Role Preferences & Aspirations",
                value=profile.get("career_preferences", ""),
                placeholder="e.g. Aspiring to join a high-growth tech company or product startup as a Software Engineer or ML Engineer.",
                help="Types of organizations, work environments, or domains you target."
            )

        submitted = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)
        if submitted:
            if not degree.strip() or not branch.strip():
                st.error("Please fill in both Degree and Branch fields.")
            else:
                db.upsert_profile(
                    user_id=user_id,
                    education=education_level,
                    degree=degree.strip(),
                    branch=branch.strip(),
                    year_semester=year_semester,
                    experience=experience.strip(),
                    interests=interests.strip(),
                    career_preferences=career_preferences.strip()
                )
                st.success("✅ Profile successfully updated!")
                st.rerun()

    # Display Current Profile Card
    if profile:
        st.divider()
        st.subheader("📋 Active Profile Summary")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Degree:** {profile.get('degree')} ({profile.get('branch')})")
            st.markdown(f"**Level:** {profile.get('education')}")
            st.markdown(f"**Standing:** {profile.get('year_semester')}")
        with col_b:
            st.markdown(f"**Last Updated:** {profile.get('updated_at', '')[:10]}")
            st.markdown(f"**Interests:** {profile.get('interests') or 'None specified'}")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_profile(st.session_state["user"])
