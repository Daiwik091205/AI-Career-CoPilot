"""
pages/interviews.py
Mock Interview Preparation module.
Provides career-tailored technical and behavioral interview questions,
evaluates student answers using AI with structured rubric feedback,
and records historical performance.
"""

import streamlit as st
import database as db
import interview_data
import ai_service
from utils.helpers import format_timestamp

def render_interviews(user: dict):
    st.title("🎙️ Career-Specific Mock Interview Preparation")
    user_id = user["id"]

    # Retrieve student's target career
    user_career = db.get_user_career(user_id)
    career_name = user_career["career_name"] if user_career else "Software Developer"

    st.markdown(f"""
Prepare for real technical and behavioral interviews tailored for **{career_name}**.
Submit your responses to receive structured AI feedback, scoring (0–10), and actionable improvement tips.
""")

    # Overview Metrics Row
    history = db.get_user_interview_history(user_id)
    total_attempts = len(history)
    avg_score = round(sum(h["score"] for h in history) / total_attempts, 1) if total_attempts > 0 else 0.0

    m1, m2, m3 = st.columns(3)
    m1.metric("Interview Questions Practiced", total_attempts)
    m2.metric("Average Score", f"{avg_score} / 10")
    m3.metric("Tailored Track", career_name)

    st.divider()

    # --- FILTER INTERVIEW QUESTIONS ---
    st.subheader("📋 Select Interview Question")
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_type = st.selectbox("Interview Type", ["All", "Technical", "HR"])
    with fc2:
        categories = ["All"] + (interview_data.TECHNICAL_CATEGORIES if sel_type == "Technical" else (interview_data.BEHAVIORAL_CATEGORIES if sel_type == "HR" else interview_data.TECHNICAL_CATEGORIES + interview_data.BEHAVIORAL_CATEGORIES))
        sel_category = st.selectbox("Topic Category", categories)

    questions = interview_data.filter_interview_questions(qtype=sel_type, category=sel_category, career_name=career_name)

    if not questions:
        st.info("No questions found for this specific filter combination.")
        return

    q_options = [f"[{q['type']} - {q['category']}] {q['question'][:80]}..." for q in questions]
    selected_idx = st.selectbox("Choose a question to answer:", range(len(questions)), format_func=lambda i: q_options[i])
    active_q = questions[selected_idx]
    qid = active_q["id"]

    st.divider()

    # --- ACTIVE QUESTION DISPLAY ---
    st.markdown(f"### ❓ Question ({active_q['type']} • {active_q['category']})")
    st.markdown(f"**Difficulty:** `{active_q.get('difficulty', 'Medium')}`")
    st.info(f"### \"{active_q['question']}\"")

    with st.expander("💡 View Key Expected Discussion Points (Rubric Hints)"):
        st.caption("A strong answer should touch upon:")
        for kp in active_q.get("key_points_to_cover", []):
            st.markdown(f"- {kp}")

    # Student Answer Box
    st.subheader("✍️ Your Response")
    st.caption("Tip: For technical questions, explain definition, architecture, and trade-offs. For behavioral questions, use the STAR format (Situation, Task, Action, Result).")

    student_answer = st.text_area(
        "Type your verbal/written response here:",
        height=180,
        placeholder="Structure your answer clearly...",
        key=f"answer_{qid}"
    )

    col_sub, _ = st.columns([1, 2])
    with col_sub:
        eval_btn = st.button("🚀 Submit for AI Evaluation", type="primary", use_container_width=True)

    if eval_btn:
        if not student_answer.strip() or len(student_answer.strip()) < 15:
            st.error("Please provide a more complete answer before requesting evaluation.")
        else:
            with st.spinner("🤖 AI Interviewer is assessing your response against industry benchmarks..."):
                eval_result = ai_service.evaluate_interview_answer(
                    question_text=active_q["question"],
                    question_category=active_q["category"],
                    career_name=career_name,
                    key_points=active_q.get("key_points_to_cover", []),
                    student_answer=student_answer
                )

                score = eval_result.get("score", 5)
                feedback_text = eval_result.get("constructive_feedback", "")

                # Save attempt in database
                db.save_interview_attempt(
                    user_id=user_id,
                    question_id=qid,
                    student_answer=student_answer,
                    ai_feedback=feedback_text,
                    score=score
                )
                st.session_state["latest_interview_eval"] = eval_result
                st.success("✅ Evaluation complete and saved to your progress profile!")

    # Display Evaluation Feedback
    if "latest_interview_eval" in st.session_state:
        res = st.session_state["latest_interview_eval"]
        st.markdown("---")
        st.subheader("🎯 Evaluation & Feedback Report")

        score = res.get("score", 0)
        verdict = res.get("verdict", "Evaluated")
        badge_col = "#28a745" if score >= 8 else ("#fd7e14" if score >= 6 else "#dc3545")

        st.markdown(
            f"""
            <div style="background-color: #f8f9fa; border-left: 6px solid {badge_col}; padding: 15px; border-radius: 8px;">
                <h2 style="margin: 0; color: {badge_col};">Score: {score} / 10 &nbsp; ({verdict})</h2>
                <p style="margin: 6px 0 0 0; color: #495057;">{res.get('constructive_feedback')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        col_str, col_weak = st.columns(2)
        with col_str:
            st.markdown("#### ✅ Demonstrated Strengths")
            for s in res.get("strengths", []):
                st.markdown(f"- {s}")
            if res.get("ideal_points_covered"):
                st.markdown("**Key Points Covered:**")
                for c in res.get("ideal_points_covered"):
                    st.caption(f"✓ {c}")

        with col_weak:
            st.markdown("#### ⚠️ Areas for Improvement")
            for w in res.get("weaknesses", []):
                st.markdown(f"- {w}")
            if res.get("missed_points"):
                st.markdown("**Points Missed or Glanced Over:**")
                for m in res.get("missed_points"):
                    st.caption(f"✕ {m}")

        if res.get("suggested_improvement"):
            st.info(f"💡 **Suggested Answer Refinement:**\n\n{res['suggested_improvement']}")

    st.divider()

    # --- PREVIOUS ATTEMPTS HISTORY ---
    st.subheader("📜 Practice History")
    if history:
        for idx, h in enumerate(history[:5]):
            with st.expander(f"Attempt #{len(history)-idx}: Q ID `{h['question_id']}` — Score: {h['score']}/10 ({format_timestamp(h.get('completed_at'))})"):
                st.markdown(f"**Your Answer:**\n> {h['student_answer']}")
                st.markdown(f"**AI Feedback:**\n{h['ai_feedback']}")
    else:
        st.info("No interview attempts logged yet.")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_interviews(st.session_state["user"])
