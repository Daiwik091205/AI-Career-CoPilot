"""
ai_service.py
Dedicated AI Service module for AI Career Co-Pilot.
Supports Google Gemini API (via google-genai) and OpenAI API (via openai).
Enforces structured JSON output validation and includes robust fallback handling.
"""

import os
import json
import re
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Clients cache
_gemini_client = None
_openai_client = None

def get_active_provider():
    """Detects available AI provider based on environment keys."""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()

    # Check for Gemini key format (e.g., starts with AQ. or AIzaSy)
    if gemini_key.startswith("AQ.") or gemini_key.startswith("AIza") or (gemini_key and not gemini_key.startswith("sk-") and gemini_key != "your_openai_api_key_here"):
        return "gemini", gemini_key

    # Check for OpenAI key format (starts with sk-)
    if openai_key.startswith("sk-") and openai_key != "your_openai_api_key_here":
        return "openai", openai_key

    # Check if either has a valid non-placeholder key
    if gemini_key and gemini_key != "your_openai_api_key_here":
        return "gemini", gemini_key
    if openai_key and openai_key != "your_openai_api_key_here":
        return "openai", openai_key

    return None, None

def get_gemini_client():
    """Returns Google GenAI client instance."""
    global _gemini_client
    provider, key = get_active_provider()
    if provider != "gemini" or not key:
        return None
    if _gemini_client is None:
        try:
            from google import genai
            _gemini_client = genai.Client(api_key=key)
        except Exception:
            return None
    return _gemini_client

def get_openai_client():
    """Returns OpenAI client instance."""
    global _openai_client
    provider, key = get_active_provider()
    if provider != "openai" or not key:
        return None
    if _openai_client is None:
        try:
            from openai import OpenAI
            _openai_client = OpenAI(api_key=key)
        except Exception:
            return None
    return _openai_client

def check_ai_status():
    """Checks whether the AI API key is configured and functional."""
    provider, key = get_active_provider()
    if not provider or not key:
        return {
            "available": False,
            "provider": "None",
            "message": "AI API key not configured or placeholder detected in .env. Using intelligent algorithmic engine as safe fallback."
        }

    if provider == "gemini":
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
        return {
            "available": True,
            "provider": "Google Gemini",
            "model": model_name,
            "message": f"Google Gemini API connected successfully (Model: {model_name})."
        }
    else:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return {
            "available": True,
            "provider": "OpenAI",
            "model": model_name,
            "message": f"OpenAI API connected successfully (Model: {model_name})."
        }

def clean_json_response(raw_text: str) -> dict:
    """Extract and parse JSON object from LLM response text safely."""
    if not raw_text:
        raise ValueError("Empty response from AI model.")

    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)

    match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)

def call_llm(prompt: str, system_prompt: str = "", json_mode: bool = False) -> str:
    """
    Unified LLM caller that routes to Gemini or OpenAI based on configured keys.
    Returns response text string.
    """
    provider, key = get_active_provider()

    # Route 1: Google Gemini
    if provider == "gemini":
        client = get_gemini_client()
        if client:
            model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            config = {}
            if json_mode:
                config["response_mime_type"] = "application/json"

            # Attempt primary model, fallback to alternative if 503 or 404
            candidate_models = [model_name, "gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]
            seen = set()
            for m in candidate_models:
                if m in seen:
                    continue
                seen.add(m)
                try:
                    res = client.models.generate_content(
                        model=m,
                        contents=full_prompt,
                        config=config if config else None
                    )
                    if res and res.text:
                        return res.text
                except Exception:
                    continue

    # Route 2: OpenAI
    if provider == "openai":
        client = get_openai_client()
        if client:
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            kwargs = {
                "model": model_name,
                "messages": messages,
                "temperature": 0.3
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            try:
                response = client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
            except Exception:
                pass

    raise RuntimeError("No active AI provider available or call failed.")

# -------------------------------------------------------------
# 1. PROJECT SKILL EXTRACTION
# -------------------------------------------------------------

def extract_project_skills(project_name: str, description: str) -> dict:
    """Extracts technical skills from a student's project name and description."""
    sys_prompt = "You are an expert technical resume reviewer. Extract technical skills (languages, frameworks, libraries, databases, tools, hardware) as JSON: {\"skills\": [\"Skill1\", \"Skill2\"]}"
    prompt = f"Project Title: {project_name}\nProject Description: {description}\nReturn ONLY valid JSON: {{\"skills\": [...]}}"

    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        skills = data.get("skills", [])
        if isinstance(skills, list) and skills:
            clean_skills = [s.strip() for s in skills if isinstance(s, str) and s.strip()]
            return {"skills": clean_skills, "source": "ai", "error": None}
    except Exception:
        pass

    # Heuristic Keyword Fallback
    text = f"{project_name} {description}".lower()
    keywords = {
        "python": "Python", "java": "Java", "c++": "C++", "c#": "C#", "javascript": "JavaScript",
        "typescript": "TypeScript", "html": "HTML5", "css": "CSS3", "react": "React.js", "vue": "Vue.js",
        "angular": "Angular", "node": "Node.js", "express": "Express.js", "django": "Django", "flask": "Flask",
        "fastapi": "FastAPI", "sql": "SQL", "mysql": "MySQL", "postgresql": "PostgreSQL", "sqlite": "SQLite",
        "mongodb": "MongoDB", "redis": "Redis", "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS",
        "azure": "Azure", "gcp": "Google Cloud", "git": "Git", "github": "GitHub", "linux": "Linux",
        "arduino": "Arduino", "rfid": "RFID", "embedded": "Embedded Systems", "iot": "Internet of Things (IoT)",
        "machine learning": "Machine Learning", "deep learning": "Deep Learning", "pytorch": "PyTorch",
        "tensorflow": "TensorFlow", "keras": "Keras", "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn",
        "nlp": "Natural Language Processing (NLP)", "computer vision": "Computer Vision", "opencv": "OpenCV",
        "rest api": "REST APIs", "graphql": "GraphQL", "microservices": "Microservices", "firebase": "Firebase",
        "ci/cd": "CI/CD", "bash": "Bash Scripting", "cryptography": "Cryptography", "cybersecurity": "Cybersecurity",
        "tableau": "Tableau", "power bi": "Power BI", "excel": "Excel"
    }
    extracted = []
    for k, v in keywords.items():
        if re.search(r'\b' + re.escape(k) + r'\b', text):
            if v not in extracted:
                extracted.append(v)

    if not extracted:
        extracted = ["Problem Solving", "Software Architecture"]

    return {"skills": extracted, "source": "fallback", "error": None}

# -------------------------------------------------------------
# 2. AI SKILL-GAP ANALYSIS
# -------------------------------------------------------------

def generate_skill_gap_analysis(profile: dict, skills: list, projects: list, career_name: str, career_reqs: list) -> dict:
    """Performs comprehensive skill-gap analysis comparing student's profile against career requirements."""
    student_skills_summary = [f"{s['skill_name']} ({s['proficiency']})" for s in skills]
    project_skills_summary = [f"{p['project_name']}: {', '.join(p.get('extracted_skills_list', []))}" for p in projects]

    sys_prompt = "You are a professional technical career mentor. Output only valid JSON."
    prompt = f"""
Perform a Skill-Gap Analysis for a student targeting '{career_name}'.
STUDENT PROFILE:
- Degree & Branch: {profile.get('degree', 'Computer Science')} - {profile.get('branch', 'Engineering')}
- Year: {profile.get('year_semester', 'Not specified')}
- Prior Experience: {profile.get('experience', 'None')}
- Stated Skills: {json.dumps(student_skills_summary)}
- Projects: {json.dumps(project_skills_summary)}

TARGET CAREER REQUIREMENTS: {json.dumps(career_reqs)}

Compare student's capabilities against career requirements. Return ONLY valid JSON:
{{
    "strong_skills": [{{"skill": "Skill Name", "proficiency": "Advanced/Intermediate", "reason": "Why strong"}}],
    "partial_skills": [{{"skill": "Skill Name", "proficiency": "Beginner", "reason": "Needs improvement"}}],
    "missing_skills": [{{"skill": "Skill Name", "why_it_matters": "Why critical"}}],
    "prioritized_skills": [{{"skill": "Skill Name", "priority": "High", "why_it_matters": "Why prioritize"}}],
    "recommended_projects": [{{"title": "Title", "description": "Desc", "skills_targeted": ["Skill1", "Skill2"]}}],
    "recommended_learning_topics": ["Topic 1", "Topic 2"],
    "summary": "2-sentence executive summary"
}}
"""
    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        if "strong_skills" in data and "missing_skills" in data:
            data["source"] = "ai"
            return data
    except Exception:
        pass

    # Heuristic Fallback
    user_skill_map = {s["skill_name"].lower(): s["proficiency"] for s in skills}
    project_skill_names = set()
    for p in projects:
        for sk in p.get("extracted_skills_list", []):
            project_skill_names.add(sk.lower())

    strong_skills = []
    partial_skills = []
    missing_skills = []
    prioritized_skills = []

    for req in career_reqs:
        req_lower = req.lower()
        matched_user_skill = None
        for us, prof in user_skill_map.items():
            if us in req_lower or req_lower in us:
                matched_user_skill = (us, prof)
                break

        in_projects = any(ps in req_lower or req_lower in ps for ps in project_skill_names)

        if matched_user_skill:
            prof = matched_user_skill[1]
            if prof in ("Advanced", "Intermediate") or in_projects:
                strong_skills.append({
                    "skill": req,
                    "proficiency": prof,
                    "reason": f"Validated by {prof.lower()} proficiency and hands-on exposure."
                })
            else:
                partial_skills.append({
                    "skill": req,
                    "proficiency": prof,
                    "reason": f"Self-rated as {prof}; needs deeper portfolio project application."
                })
        else:
            missing_skills.append({
                "skill": req,
                "why_it_matters": f"Essential core competency for industry-level {career_name} roles."
            })
            if len(prioritized_skills) < 3:
                prioritized_skills.append({
                    "skill": req,
                    "priority": "High",
                    "why_it_matters": f"Immediate prerequisite for entry-level hiring in {career_name}."
                })

    rec_projects = [
        {
            "title": f"Production-Ready {career_name} Portfolio Capstone",
            "description": f"Build and deploy an end-to-end application integrating {', '.join(career_reqs[:3])}.",
            "skills_targeted": career_reqs[:3]
        }
    ]

    return {
        "strong_skills": strong_skills,
        "partial_skills": partial_skills,
        "missing_skills": missing_skills,
        "prioritized_skills": prioritized_skills,
        "recommended_projects": rec_projects,
        "recommended_learning_topics": [f"Deep Dive into {s['skill']}" for s in prioritized_skills] or ["System Design Fundamentals", "Advanced Data Structures"],
        "summary": f"Your current profile covers {len(strong_skills)} out of {len(career_reqs)} key areas for {career_name}. Focus first on bridging {len(missing_skills)} missing skills.",
        "source": "fallback"
    }

# -------------------------------------------------------------
# 3. READINESS ASSESSMENT
# -------------------------------------------------------------

def calculate_readiness_assessment(profile: dict, skills: list, projects: list,
                                  career_name: str, career_reqs: list,
                                  dsa_progress: dict, interview_progress: list) -> dict:
    """Computes an estimated career readiness score (0-100) and multidimensional breakdown."""
    total_reqs = max(len(career_reqs), 1)
    user_skill_names = {s["skill_name"].lower(): s["proficiency"] for s in skills}

    matched_strong = 0
    matched_partial = 0
    for req in career_reqs:
        req_l = req.lower()
        for sname, prof in user_skill_names.items():
            if sname in req_l or req_l in sname:
                if prof in ("Advanced", "Intermediate"):
                    matched_strong += 1
                else:
                    matched_partial += 1
                break

    skill_coverage = min(100, int(((matched_strong * 1.0 + matched_partial * 0.5) / total_reqs) * 100))
    project_score = min(100, len(projects) * 35)

    solved_dsa = sum(1 for v in dsa_progress.values() if v.get("status") == "solved")
    dsa_score = min(100, solved_dsa * 12 + len(dsa_progress) * 5)

    avg_interview = 0
    if interview_progress:
        scores = [item.get("score", 0) for item in interview_progress if item.get("score")]
        if scores:
            avg_interview = min(100, int((sum(scores) / (len(scores) * 10)) * 100))

    base_readiness = int(
        (skill_coverage * 0.45) +
        (project_score * 0.25) +
        (dsa_score * 0.15) +
        (avg_interview * 0.15)
    )
    base_readiness = max(10, min(95, base_readiness))

    sys_prompt = "You are a realistic career evaluator. Output only valid JSON."
    prompt = f"""
Estimate a Career Readiness Score (0-100) for student pursuing '{career_name}'.
Career Requirements: {json.dumps(career_reqs)}
Student Skills ({len(skills)}): {json.dumps([s['skill_name'] + ' (' + s['proficiency'] + ')' for s in skills])}
Student Projects ({len(projects)}): {json.dumps([p['project_name'] for p in projects])}
DSA Solved: {solved_dsa}
Interview Practices: {len(interview_progress)}
Baseline Calculated Score: {base_readiness}

Return ONLY valid JSON:
{{
    "readiness_score": integer between 0 and 100,
    "breakdown": {{
        "skill_coverage_score": integer (0-100),
        "proficiency_score": integer (0-100),
        "project_experience_score": integer (0-100),
        "dsa_preparedness_score": integer (0-100),
        "interview_performance_score": integer (0-100)
    }},
    "key_strengths": ["Strength 1", "Strength 2"],
    "critical_gaps": ["Gap 1", "Gap 2"],
    "verdict_summary": "Concise summary"
}}
"""
    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        if "readiness_score" in data and "breakdown" in data:
            data["source"] = "ai"
            return data
    except Exception:
        pass

    return {
        "readiness_score": base_readiness,
        "breakdown": {
            "skill_coverage_score": skill_coverage,
            "proficiency_score": min(100, matched_strong * 25 + matched_partial * 10),
            "project_experience_score": project_score,
            "dsa_preparedness_score": dsa_score,
            "interview_performance_score": avg_interview
        },
        "key_strengths": [
            f"Demonstrated proficiency in {matched_strong} key target technologies",
            f"{len(projects)} verified practical project(s) added to portfolio"
        ] if matched_strong > 0 or projects else ["Clear career target selected"],
        "critical_gaps": [
            f"{total_reqs - matched_strong} technical requirements still need mastery",
            "Additional mock interview and DSA test cases needed"
        ],
        "verdict_summary": f"Estimated at {base_readiness}%. Good foundation with significant opportunities to boost readiness through targeted gap closure.",
        "source": "fallback"
    }

# -------------------------------------------------------------
# 4. PERSONALIZED & ADAPTIVE ROADMAP
# -------------------------------------------------------------

def generate_roadmap(profile: dict, skills: list, projects: list, career_name: str, gap_analysis: dict, readiness_score: int) -> dict:
    """Generates a personalized 4-phase learning and preparation roadmap."""
    strong_skill_names = [s.get("skill", "") for s in gap_analysis.get("strong_skills", [])]
    missing_skill_names = [s.get("skill", "") for s in gap_analysis.get("missing_skills", [])]
    partial_skill_names = [s.get("skill", "") for s in gap_analysis.get("partial_skills", [])]

    sys_prompt = "You are an expert curriculum designer. Output only valid JSON."
    prompt = f"""
Design a structured 4-phase preparation roadmap for a student aiming for '{career_name}'.
Current Readiness Score: {readiness_score}/100.
Skills student ALREADY possesses (DO NOT RE-TEACH): {json.dumps(strong_skill_names)}
Skills with PARTIAL proficiency: {json.dumps(partial_skill_names)}
CRITICAL MISSING SKILLS: {json.dumps(missing_skill_names)}

Create exactly 4 phases:
Phase 1: Foundations & Core Prerequisites
Phase 2: Core Domain Competencies
Phase 3: Advanced Specialization
Phase 4: Capstone Projects & Interview Readiness

Return ONLY valid JSON:
{{
    "phases": [
        {{
            "phase_number": 1,
            "phase_name": "Phase 1 — Foundations",
            "objective": "Brief statement",
            "estimated_duration": "3-4 weeks",
            "items": [
                {{"topic": "Topic Name", "description": "What to learn and practice", "learning_resource": "Doc/Resource"}}
            ]
        }}
    ]
}}
"""
    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        if "phases" in data and len(data["phases"]) >= 4:
            data["source"] = "ai"
            return data
    except Exception:
        pass

    # Fallback roadmap
    p1_items = [
        {"topic": s, "description": f"Master fundamental concepts, syntax, and workflows of {s}.", "learning_resource": "Official Documentation & Practical Labs"}
        for s in (missing_skill_names[:2] or ["Programming Fundamentals", "Data Structures"])
    ]
    p2_items = [
        {"topic": s, "description": f"Deep dive into production usage and framework internals of {s}.", "learning_resource": "Coursework & Medium Exercises"}
        for s in (missing_skill_names[2:4] or partial_skill_names[:2] or ["Database Schema Design", "REST API Development"])
    ]
    p3_items = [
        {"topic": f"Advanced {career_name} Architectures", "description": "Scalability, concurrency, security best practices, and caching patterns.", "learning_resource": "System Design Primer & Tech Blogs"},
        {"topic": "Testing & CI/CD Pipelines", "description": "Automated unit tests, integration testing, and GitHub Actions.", "learning_resource": "Hands-on Workshop Labs"}
    ]
    p4_items = [
        {"topic": f"Full-Stack {career_name} Capstone Project", "description": "Develop, document, and deploy a production-grade portfolio project with live URL.", "learning_resource": "GitHub Portfolio"},
        {"topic": "DSA & Mock Interview Drills", "description": "Solve high-frequency coding patterns and rehearse behavioral STAR questions.", "learning_resource": "Interview Module Practice"}
    ]

    return {
        "phases": [
            {"phase_number": 1, "phase_name": "Phase 1 — Foundations", "objective": "Establish fundamental competencies and bridge core prerequisite gaps.", "estimated_duration": "3-4 Weeks", "items": p1_items},
            {"phase_number": 2, "phase_name": "Phase 2 — Core Domain Competencies", "objective": f"Solidify intermediate hands-on skills required for {career_name}.", "estimated_duration": "4-6 Weeks", "items": p2_items},
            {"phase_number": 3, "phase_name": "Phase 3 — Advanced Specialization", "objective": "Tackle advanced architectural patterns and production-level tooling.", "estimated_duration": "3-4 Weeks", "items": p3_items},
            {"phase_number": 4, "phase_name": "Phase 4 — Portfolio Projects & Interview Prep", "objective": "Synthesize learning into tangible portfolio artifacts and ace technical interviews.", "estimated_duration": "2-3 Weeks", "items": p4_items}
        ],
        "source": "fallback"
    }

# -------------------------------------------------------------
# 5. DSA AI MENTOR
# -------------------------------------------------------------

def explain_dsa_solution(question: dict, student_code: str = "", mode: str = "explain") -> dict:
    """Provides AI hints, explanations, or code debugging."""
    if mode == "hint":
        instruction = "Provide a guided, progressive hint that helps the student think in the right direction WITHOUT directly revealing the complete code or solution."
    elif mode == "debug":
        instruction = "Inspect the student's code below, identify any bugs, edge cases not handled, or time complexity issues, and suggest how to fix them."
    else:
        instruction = "Provide a clear, step-by-step conceptual walkthrough of the optimal approach, including time and space complexity analysis (Big-O)."

    prompt = f"""
{instruction}
Problem: {question.get('title')} ({question.get('topic')}, {question.get('difficulty')})
Statement: {question.get('statement')}
Approach Notes: {question.get('approach')}
Solution: {question.get('solution')}
Student's Code: {student_code if student_code.strip() else 'No code submitted yet.'}
Format response with clear markdown headings and bullet points.
"""
    try:
        content = call_llm(prompt, system_prompt="You are an encouraging computer science tutor.", json_mode=False)
        return {"content": content, "source": "ai"}
    except Exception:
        pass

    if mode == "hint":
        hints = question.get("hints", ["Think about breaking the problem down into smaller subproblems."])
        hint_text = "\n\n".join([f"💡 **Hint {i+1}**: {h}" for i, h in enumerate(hints)])
        return {"content": hint_text, "source": "fallback"}
    elif mode == "debug":
        return {
            "content": f"### 🔍 Debugging Guidance\n- **Check base cases**: Does your solution handle empty arrays, single elements, or boundary values?\n- **Expected Complexity**: Approach using `{question.get('approach', 'recommended approach')}`.\n- **Reference Implementation**:\n```python\n{question.get('solution', '')}\n```",
            "source": "fallback"
        }
    else:
        return {
            "content": f"### 💡 Approach: {question.get('approach')}\n\n**Standard Implementation**:\n```python\n{question.get('solution')}\n```",
            "source": "fallback"
        }

def generate_dsa_question(topic: str, difficulty: str) -> dict:
    """Generates an original DSA question using AI."""
    sys_prompt = "You are a DSA problem setter. Output only valid JSON."
    prompt = f"""
Generate an original DSA practice problem for college students.
Topic: {topic}, Difficulty: {difficulty}
Return ONLY valid JSON:
{{
    "title": "Title",
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "statement": "Detailed problem statement",
    "examples": [{{"input": "...", "output": "...", "explanation": "..."}}],
    "hints": ["Hint 1", "Hint 2"],
    "approach": "Algorithmic explanation",
    "starter_code": "def solution_func(args):\\n    pass\\n",
    "solution": "def solution_func(args):\\n    return True\\n",
    "test_cases": [{{"args": ["sample_arg"], "expected": "expected_result"}}]
}}
"""
    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        data["id"] = f"custom_{topic[:3].lower()}_{os.urandom(2).hex()}"
        data["source"] = "ai"
        return data
    except Exception:
        pass

    return {
        "id": f"custom_{topic[:3].lower()}_fb",
        "title": f"Practice Challenge: {topic} Mastery",
        "topic": topic,
        "difficulty": difficulty,
        "statement": f"Implement an efficient algorithm demonstrating core properties of {topic}.",
        "examples": [{"input": "Sample test", "output": "Expected output", "explanation": "Demonstrates concept."}],
        "hints": ["Review foundational invariants of the data structure."],
        "approach": f"Leverage {topic} principles for optimal space-time trade-off.",
        "starter_code": f"def solve_{topic.lower().replace(' ', '_')}():\n    pass\n",
        "solution": f"def solve_{topic.lower().replace(' ', '_')}():\n    return True\n",
        "test_cases": [],
        "source": "fallback"
    }

# -------------------------------------------------------------
# 6. INTERVIEW ANSWER EVALUATION
# -------------------------------------------------------------

def evaluate_interview_answer(question_text: str, question_category: str, career_name: str, key_points: list, student_answer: str) -> dict:
    """Evaluates a student's answer to an interview question with constructive feedback and scoring (0-10)."""
    if not student_answer or len(student_answer.strip()) < 10:
        return {
            "score": 2,
            "verdict": "Insufficient Answer",
            "strengths": ["Attempted response."],
            "weaknesses": ["Answer is too brief to evaluate properly."],
            "constructive_feedback": "Please provide a more elaborate answer explaining your approach, examples, and technical reasoning.",
            "ideal_points_covered": [],
            "missed_points": key_points or ["Elaborate on core principles"],
            "suggested_improvement": "Use the STAR method for behavioral questions or define terms, trade-offs, and examples for technical questions.",
            "source": "fallback"
        }

    sys_prompt = "You are a professional hiring manager providing constructive interview evaluations. Output only valid JSON."
    prompt = f"""
Evaluate a student candidate for a '{career_name}' role.
QUESTION ({question_category}): "{question_text}"
EXPECTED CONCEPTS: {json.dumps(key_points)}
STUDENT ANSWER: "{student_answer}"

Score out of 10. Return ONLY valid JSON:
{{
    "score": integer from 1 to 10,
    "verdict": "Excellent / Strong / Satisfactory / Needs Improvement / Weak",
    "strengths": ["Good points"],
    "weaknesses": ["Gaps or inaccuracies"],
    "constructive_feedback": "Paragraph of actionable feedback",
    "ideal_points_covered": ["Concepts covered well"],
    "missed_points": ["Concepts omitted"],
    "suggested_improvement": "Specific way to structure or expand this answer"
}}
"""
    try:
        raw = call_llm(prompt, system_prompt=sys_prompt, json_mode=True)
        data = clean_json_response(raw)
        if "score" in data and "constructive_feedback" in data:
            data["source"] = "ai"
            return data
    except Exception:
        pass

    # Heuristic Fallback
    words = student_answer.strip().split()
    length = len(words)
    covered = []
    missed = []
    for kp in key_points:
        key_terms = [t.lower() for t in re.findall(r'\b\w{4,}\b', kp)]
        if any(term in student_answer.lower() for term in key_terms):
            covered.append(kp)
        else:
            missed.append(kp)

    score = 5
    if length > 50:
        score += 2
    if len(covered) >= len(missed):
        score += 2
    score = min(9, max(3, score))

    verdict = "Strong" if score >= 8 else ("Satisfactory" if score >= 6 else "Needs Improvement")

    return {
        "score": score,
        "verdict": verdict,
        "strengths": ["Clear communication and effort demonstrated.", f"Addressed {len(covered)} key discussion points."],
        "weaknesses": [f"Could elaborate more deeply on: {', '.join([m.split('(')[0] for m in missed[:2]])}"] if missed else ["Minor depth additions possible."],
        "constructive_feedback": f"Your response covers foundational ideas well with {length} words. To improve, provide concrete metrics, trade-offs, and examples from personal projects.",
        "ideal_points_covered": covered if covered else ["General domain terminology"],
        "missed_points": missed if missed else ["None"],
        "suggested_improvement": "Structure your answers using the STAR method for behavioral questions or Definition -> Mechanics -> Trade-offs for technical questions.",
        "source": "fallback"
    }
