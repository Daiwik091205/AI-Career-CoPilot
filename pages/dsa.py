"""
pages/dsa.py
DSA Practice Module.
Provides curated algorithmic challenges across 14 core topics,
safe in-app test execution, AI hints and solution explanations,
progress tracking, and weak-area topic recommendations.
"""

import streamlit as st
import database as db
import dsa_data
import ai_service
from utils.helpers import run_safe_python_tests

def render_dsa(user: dict):
    st.title("💻 Data Structures & Algorithms (DSA) Practice")
    user_id = user["id"]

    # Load data
    all_questions = dsa_data.get_all_dsa_questions()
    user_progress = db.get_user_dsa_progress(user_id)

    # Calculate overall stats
    total_q = len(all_questions)
    solved_count = sum(1 for q in all_questions if user_progress.get(q["id"], {}).get("status") == "solved")
    attempted_count = sum(1 for q in all_questions if user_progress.get(q["id"], {}).get("status") == "attempted")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Available Questions", total_q)
    m2.metric("Solved", solved_count)
    m3.metric("Attempted", attempted_count)
    m4.metric("Completion Rate", f"{int(solved_count / total_q * 100)}%" if total_q > 0 else "0%")

    st.divider()

    # --- AI RECOMMENDATION & QUESTION GENERATOR ---
    with st.expander("🤖 AI DSA Assistant & Topic Recommendations", expanded=False):
        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            st.subheader("💡 Recommended Next Focus Area")
            # Calculate weakest topics
            topic_stats = {}
            for q in all_questions:
                top = q["topic"]
                topic_stats[top] = topic_stats.get(top, {"total": 0, "solved": 0})
                topic_stats[top]["total"] += 1
                if user_progress.get(q["id"], {}).get("status") == "solved":
                    topic_stats[top]["solved"] += 1

            unsolved_topics = [t for t, s in topic_stats.items() if s["solved"] < s["total"]]
            recommended_topic = unsolved_topics[0] if unsolved_topics else "Dynamic Programming"

            st.write(f"Based on your current solved ratio, practice **{recommended_topic}** next.")
            st.caption(f"Progress in {recommended_topic}: {topic_stats[recommended_topic]['solved']} / {topic_stats[recommended_topic]['total']} solved.")

        with col_rec2:
            st.subheader("⚡ Generate Custom AI Question")
            gen_topic = st.selectbox("Topic", dsa_data.DSA_TOPICS, key="gen_topic_sel")
            gen_diff = st.selectbox("Difficulty", dsa_data.DSA_DIFFICULTIES, key="gen_diff_sel")
            if st.button("Generate Original Question", use_container_width=True):
                with st.spinner("AI is formulating a new coding challenge..."):
                    custom_q = ai_service.generate_dsa_question(gen_topic, gen_diff)
                    st.session_state["active_custom_q"] = custom_q
                    st.success(f"Generated: {custom_q.get('title')}!")

    if "active_custom_q" in st.session_state:
        cq = st.session_state["active_custom_q"]
        with st.expander(f"✨ Custom Challenge: {cq.get('title')} ({cq.get('difficulty')})", expanded=True):
            st.write(cq.get("statement"))
            st.code(cq.get("solution"), language="python")
            if st.button("Close Custom Question"):
                del st.session_state["active_custom_q"]
                st.rerun()

    # --- FILTERS ROW ---
    st.subheader("📚 Question Bank")
    fc1, fc2, fc3, fc4 = st.columns([1.5, 1, 1, 1.5])
    with fc1:
        sel_topic = st.selectbox("Filter by Topic", ["All"] + dsa_data.DSA_TOPICS)
    with fc2:
        sel_diff = st.selectbox("Filter by Difficulty", ["All"] + dsa_data.DSA_DIFFICULTIES)
    with fc3:
        sel_status = st.selectbox("Filter by Status", ["All", "Solved", "Attempted", "Not Attempted"])
    with fc4:
        search_query = st.text_input("🔍 Search Questions", placeholder="Search title or keyword...")

    # Filter logic
    questions = dsa_data.filter_dsa_questions(topic=sel_topic, difficulty=sel_diff, search_term=search_query)

    if sel_status != "All":
        filtered_by_status = []
        for q in questions:
            st_val = user_progress.get(q["id"], {}).get("status", "not_attempted")
            if sel_status == "Solved" and st_val == "solved":
                filtered_by_status.append(q)
            elif sel_status == "Attempted" and st_val == "attempted":
                filtered_by_status.append(q)
            elif sel_status == "Not Attempted" and st_val == "not_attempted":
                filtered_by_status.append(q)
        questions = filtered_by_status

    st.write(f"Showing **{len(questions)}** problem(s):")

    if not questions:
        st.info("No questions match your current filter criteria.")
        return

    # Render questions list / selector
    q_titles = [f"[{q['difficulty']}] {q['title']} — {q['topic']} ({'✅ Solved' if user_progress.get(q['id'], {}).get('status') == 'solved' else ('⏳ Attempted' if user_progress.get(q['id'], {}).get('status') == 'attempted' else '⬜ Not Attempted')})" for q in questions]
    selected_idx = st.selectbox("Select a problem to practice:", range(len(questions)), format_func=lambda i: q_titles[i])

    active_q = questions[selected_idx]
    qid = active_q["id"]
    current_status = user_progress.get(qid, {}).get("status", "not_attempted")
    saved_code = user_progress.get(qid, {}).get("code_submitted", "") or active_q.get("starter_code", "")

    st.divider()

    # --- ACTIVE PROBLEM WORKSPACE ---
    p_header, p_status_box = st.columns([3, 1.2])
    with p_header:
        diff_color = "#28a745" if active_q["difficulty"] == "Easy" else ("#fd7e14" if active_q["difficulty"] == "Medium" else "#dc3545")
        st.markdown(f"## {active_q['title']}")
        st.markdown(f"<span style='background-color: {diff_color}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;'>{active_q['difficulty']}</span> &nbsp; **Topic:** `{active_q['topic']}`", unsafe_allow_html=True)

    with p_status_box:
        st.caption("Manual Status Override:")
        status_opts = ["not_attempted", "attempted", "solved"]
        status_labels = {"not_attempted": "Not Attempted", "attempted": "Attempted", "solved": "Solved ✅"}
        new_stat = st.selectbox(
            "Status",
            status_opts,
            index=status_opts.index(current_status),
            format_func=lambda x: status_labels[x],
            key=f"status_sel_{qid}",
            label_visibility="collapsed"
        )
        if new_stat != current_status:
            db.update_dsa_progress(user_id, qid, new_stat, code=saved_code)
            st.toast(f"Status updated to {status_labels[new_stat]}")
            st.rerun()

    st.write("### Problem Statement")
    st.write(active_q["statement"])

    # Examples
    if active_q.get("examples"):
        st.write("#### Examples:")
        for ex_idx, ex in enumerate(active_q["examples"], 1):
            with st.container():
                st.markdown(f"**Example {ex_idx}:**")
                st.code(f"Input: {ex.get('input')}\nOutput: {ex.get('output')}", language="text")
                if ex.get("explanation"):
                    st.caption(f"Explanation: {ex.get('explanation')}")

    st.divider()

    # --- CODE PRACTICE & TEST RUNNER ---
    st.subheader("💻 Code Practice Environment")
    st.caption("Write your solution in Python. Note: Arbitrary code execution is sandboxed using restricted AST inspection and predefined test cases.")

    code_lang = st.selectbox("Programming Language", ["Python 3", "C++ (Prototype)", "Java (Prototype)", "JavaScript (Prototype)"], key=f"lang_{qid}")

    user_code = st.text_area(
        "Code Editor",
        value=saved_code,
        height=220,
        key=f"editor_{qid}"
    )

    col_btn_test, col_btn_save = st.columns([1, 1])
    with col_btn_test:
        test_clicked = st.button("▶️ Run Test Cases", type="primary", use_container_width=True)
    with col_btn_save:
        save_clicked = st.button("💾 Save Code Draft", use_container_width=True)

    if save_clicked:
        db.update_dsa_progress(user_id, qid, "attempted" if current_status == "not_attempted" else current_status, code=user_code)
        st.success("Draft saved successfully!")

    if test_clicked:
        if code_lang != "Python 3":
            st.info(f"Safe automated test runner currently executes Python 3 test cases. For {code_lang}, you can use the AI Solution Checker below!")
        else:
            with st.spinner("Executing test cases in secure sandbox..."):
                test_cases = active_q.get("test_cases", [])
                test_results = run_safe_python_tests(user_code, test_cases)

                if test_results.get("error"):
                    st.error(f"Execution Error: {test_results['error']}")
                else:
                    passed = test_results["passed_count"]
                    total = test_results["total_count"]
                    if test_results["all_passed"]:
                        st.success(f"🎉 All {passed}/{total} Test Cases Passed! Marking problem as Solved.")
                        db.update_dsa_progress(user_id, qid, "solved", code=user_code)
                        st.balloons()
                    else:
                        st.warning(f"Passed {passed} / {total} Test Cases.")
                        db.update_dsa_progress(user_id, qid, "attempted", code=user_code)

                    # Show test case outputs
                    for case in test_results["results"]:
                        with st.container():
                            icon = "✅" if case["passed"] else "❌"
                            st.markdown(f"**Test Case {case['test_case']}**: {icon}")
                            st.text(f"Args: {case['args']}\nExpected: {case['expected']}\nGot: {case['got']}")
                            if case.get("error"):
                                st.caption(f"Error: {case['error']}")

    st.divider()

    # --- AI TUTOR MENTORSHIP PANEL ---
    st.subheader("🤖 AI Algorithmic Mentor")
    st.caption("Need guidance? Use AI hints, conceptual walkthroughs, or code debugging.")

    ai_c1, ai_c2, ai_c3 = st.columns(3)
    with ai_c1:
        hint_btn = st.button("💡 Get Guided Hint", use_container_width=True)
    with ai_c2:
        explain_btn = st.button("📖 Explain Approach & Big-O", use_container_width=True)
    with ai_c3:
        debug_btn = st.button("🐞 Debug My Code", use_container_width=True)

    if hint_btn:
        with st.spinner("AI Mentor is analyzing problem invariants..."):
            hint_res = ai_service.explain_dsa_solution(active_q, user_code, mode="hint")
            st.info(hint_res["content"])

    if explain_btn:
        with st.spinner("Generating step-by-step conceptual walkthrough..."):
            exp_res = ai_service.explain_dsa_solution(active_q, user_code, mode="explain")
            st.markdown(exp_res["content"])

    if debug_btn:
        with st.spinner("AI is inspecting your logic for bugs and edge cases..."):
            dbg_res = ai_service.explain_dsa_solution(active_q, user_code, mode="debug")
            st.markdown(dbg_res["content"])

    # Expandable Reference Solution
    with st.expander("👁️ View Standard Reference Solution & Approach", expanded=False):
        st.markdown(f"**Expected Approach:** {active_q.get('approach')}")
        st.code(active_q.get("solution", "# Solution code"), language="python")

if __name__ == "__main__" or "app" not in globals():
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in from Home.")
    else:
        render_dsa(st.session_state["user"])
