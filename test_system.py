"""
test_system.py
Automated end-to-end integration and sanity tests for AI Career Co-Pilot.
Tests all database operations, bcrypt security, AST sandbox execution,
AI service fallbacks, and career gap logic.
"""

import sys
import os

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database as db
import career_data
import dsa_data
import interview_data
import ai_service
from utils.helpers import hash_password, verify_password, run_safe_python_tests, analyze_ast_safety

def run_tests():
    print("=" * 60)
    print("[TEST] RUNNING AI CAREER CO-PILOT INTEGRATION TESTS")
    print("=" * 60)

    # 1. Database Initialization
    print("1. Testing Database Initialization...")
    db.init_db()
    print("   [OK] SQLite database initialized successfully.")

    # 2. Authentication & bcrypt Security
    print("2. Testing Password Hashing & Authentication...")
    test_user = "test_engineer"
    test_pass = "SecurePass123!"
    hashed = hash_password(test_pass)
    assert verify_password(test_pass, hashed) is True, "Password verification failed"
    assert verify_password("WrongPass", hashed) is False, "False positive in password verification"

    # Register user
    # Clean up any existing test user
    conn = db.get_connection()
    conn.execute("DELETE FROM users WHERE username = ?", (test_user,))
    conn.commit()
    conn.close()

    uid = db.create_user(test_user, hashed)
    assert uid is not None, "Failed to create user"
    user_fetched = db.get_user_by_username(test_user)
    assert user_fetched["id"] == uid, "Fetched user ID does not match"
    print("   [OK] User created and verified with bcrypt.")

    # 3. Student Profile
    print("3. Testing Student Profile CRUD...")
    db.upsert_profile(
        user_id=uid,
        education="Undergraduate (B.Tech / B.E. / B.Sc / BCA)",
        degree="B.Tech",
        branch="Computer Science",
        year_semester="3rd Year (Sem 5-6)",
        experience="Built full-stack applications",
        interests="AI & Web Development",
        career_preferences="Product Engineering"
    )
    prof = db.get_profile(uid)
    assert prof["degree"] == "B.Tech", "Profile degree mismatch"
    assert prof["branch"] == "Computer Science", "Profile branch mismatch"
    print("   [OK] Student profile saved and retrieved.")

    # 4. Skills Management
    print("4. Testing Skills Management...")
    db.add_or_update_skill(uid, "Python", "Advanced")
    db.add_or_update_skill(uid, "SQL", "Intermediate")
    db.add_or_update_skill(uid, "Docker", "Beginner")
    skills = db.get_user_skills(uid)
    assert len(skills) == 3, f"Expected 3 skills, got {len(skills)}"

    # Update skill
    db.add_or_update_skill(uid, "Docker", "Intermediate")
    skills = db.get_user_skills(uid)
    docker_skill = next(s for s in skills if s["skill_name"] == "Docker")
    assert docker_skill["proficiency"] == "Intermediate", "Skill update failed"

    # Delete skill
    db.delete_skill(uid, docker_skill["id"])
    skills = db.get_user_skills(uid)
    assert len(skills) == 2, "Skill deletion failed"
    print("   [OK] Skills added, updated, and deleted successfully.")

    # 5. Projects & Skill Extraction
    print("5. Testing Projects & Skill Extraction...")
    proj_title = "Smart RFID Attendance"
    proj_desc = "Built an attendance system using Arduino and C++ with SQLite database integration."
    extracted = ai_service.extract_project_skills(proj_title, proj_desc)
    assert len(extracted.get("skills", [])) > 0, "No skills extracted"
    print(f"   Extracted skills: {extracted['skills']}")

    pid = db.add_project(uid, proj_title, proj_desc, extracted["skills"])
    projects = db.get_user_projects(uid)
    assert len(projects) == 1, "Project insertion failed"
    assert projects[0]["id"] == pid
    print("   [OK] Projects logged with extracted skills.")

    # 6. Target Career Goal
    print("6. Testing Career Goal Setting...")
    target_role = "Software Developer"
    c_info = career_data.get_career(target_role)
    assert c_info is not None, f"Career {target_role} not found"
    cid = db.set_user_career(uid, target_role, c_info["required_skills"])
    active_career = db.get_user_career(uid)
    assert active_career["career_name"] == target_role, "Career goal mismatch"
    print(f"   [OK] Active career set to {target_role}.")

    # 7. AI Skill-Gap Analysis & Readiness Score
    print("7. Testing Skill-Gap Analysis & Readiness Engine...")
    gap_result = ai_service.generate_skill_gap_analysis(
        profile=prof,
        skills=skills,
        projects=projects,
        career_name=target_role,
        career_reqs=c_info["required_skills"]
    )
    assert "strong_skills" in gap_result, "Gap analysis missing strong_skills"
    assert "missing_skills" in gap_result, "Gap analysis missing missing_skills"

    readiness = ai_service.calculate_readiness_assessment(
        profile=prof,
        skills=skills,
        projects=projects,
        career_name=target_role,
        career_reqs=c_info["required_skills"],
        dsa_progress={},
        interview_progress=[]
    )
    assert 0 <= readiness["readiness_score"] <= 100, "Readiness score out of bounds"
    print(f"   [OK] Gap analysis generated with Readiness Score: {readiness['readiness_score']}/100.")

    # 8. Personalized Roadmap Generation
    print("8. Testing Roadmap Generation...")
    roadmap = ai_service.generate_roadmap(
        profile=prof,
        skills=skills,
        projects=projects,
        career_name=target_role,
        gap_analysis=gap_result,
        readiness_score=readiness["readiness_score"]
    )
    assert "phases" in roadmap and len(roadmap["phases"]) >= 4, "Roadmap must contain at least 4 phases"

    rid = db.save_user_roadmap(
        user_id=uid,
        career_id=cid,
        gap_analysis=gap_result,
        readiness_score=readiness["readiness_score"],
        roadmap_phases=roadmap["phases"],
        is_adaptive=True
    )
    saved_road = db.get_user_roadmap(uid)
    assert saved_road["readiness_score"] == readiness["readiness_score"]
    print(f"   [OK] 4-Phase Roadmap saved (ID: {rid}).")

    # 9. Safe AST Code Execution Sandbox for DSA
    print("9. Testing Safe DSA Code Runner...")
    two_sum_q = dsa_data.get_dsa_question_by_id("arr_01")
    assert two_sum_q is not None, "DSA Question arr_01 not found"

    # Test passing code
    correct_code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
"""
    runner_res = run_safe_python_tests(correct_code, two_sum_q["test_cases"], "two_sum")
    assert runner_res["all_passed"] is True, f"Correct solution failed tests: {runner_res}"
    assert runner_res["passed_count"] == len(two_sum_q["test_cases"])

    # Test malicious code block
    malicious_code = """
import os
os.system("echo hacked")
def two_sum(nums, target):
    return [0, 1]
"""
    mal_res = run_safe_python_tests(malicious_code, two_sum_q["test_cases"], "two_sum")
    assert mal_res["all_passed"] is False
    assert "Security restriction" in mal_res["error"]
    print("   [OK] Safe AST sandbox passed legitimate code and blocked unsafe imports.")

    # 10. DSA Progress Tracking
    print("10. Testing DSA Progress Tracking...")
    db.update_dsa_progress(uid, "arr_01", "solved", code=correct_code)
    dsa_prog = db.get_user_dsa_progress(uid)
    assert dsa_prog["arr_01"]["status"] == "solved", "DSA status update failed"
    print("   [OK] DSA progress recorded.")

    # 11. Mock Interview Evaluation
    print("11. Testing Mock Interview Evaluation...")
    int_q = interview_data.get_interview_question_by_id("tech_oop_01")
    assert int_q is not None, "Interview question tech_oop_01 not found"

    eval_res = ai_service.evaluate_interview_answer(
        question_text=int_q["question"],
        question_category=int_q["category"],
        career_name=target_role,
        key_points=int_q["key_points_to_cover"],
        student_answer="Encapsulation bundles data and methods. Abstraction hides complexity. Inheritance allows subclassing and code reuse. Polymorphism allows methods to behave differently based on the object."
    )
    assert "score" in eval_res, "Evaluation result missing score"
    assert "constructive_feedback" in eval_res, "Evaluation missing feedback"

    db.save_interview_attempt(
        user_id=uid,
        question_id="tech_oop_01",
        student_answer="Sample answer",
        ai_feedback=eval_res["constructive_feedback"],
        score=eval_res["score"]
    )
    history = db.get_user_interview_history(uid)
    assert len(history) == 1, "Interview attempt not saved"
    print(f"   [OK] Mock interview evaluated (Score: {eval_res['score']}/10) and persisted.")

    # 12. Dashboard Aggregated Stats
    print("12. Testing Dashboard Statistics...")
    stats = db.get_user_dashboard_stats(uid)
    assert stats["skills_count"] == 2
    assert stats["projects_count"] == 1
    assert stats["dsa_solved"] == 1
    assert stats["interviews_taken"] == 1
    print(f"   [OK] Aggregated Dashboard Metrics: {stats}")

    print("=" * 60)
    print("[SUCCESS] ALL 12 INTEGRATION & SECURITY TESTS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
