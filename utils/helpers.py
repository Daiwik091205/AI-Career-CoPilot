"""
utils/helpers.py
Helper utilities for authentication, safe sandbox code testing, and UI formatting.
"""

import bcrypt
import ast
import math
import collections
import heapq
from datetime import datetime

# -------------------------------------------------------------
# PASSWORD SECURITY (bcrypt)
# -------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt with salt."""
    if not password:
        raise ValueError("Password cannot be empty.")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against stored bcrypt hash."""
    if not password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

# -------------------------------------------------------------
# SAFE LOCAL CODE EXECUTION FOR CODING PRACTICE
# -------------------------------------------------------------

FORBIDDEN_CALLS = {
    "open", "compile", "exec", "eval", "__import__",
    "globals", "locals", "getattr", "setattr", "delattr", "exit", "quit"
}

FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "socket", "requests", "shutil",
    "pathlib", "ctypes", "multiprocessing", "threading", "pickle"
}

SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
    "True": True,
    "False": False,
    "None": None
}

def analyze_ast_safety(code_str: str):
    """
    Statically analyzes code to ensure no dangerous modules or forbidden builtins are invoked.
    Raises ValueError with explanation if suspicious AST node is detected.
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        raise ValueError(f"Syntax Error in your code: {e}")

    for node in ast.walk(tree):
        # Disallow forbidden imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split('.')[0]
                if root_module in FORBIDDEN_MODULES:
                    raise ValueError(f"Security restriction: Importing '{root_module}' is not allowed in sandbox.")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split('.')[0]
                if root_module in FORBIDDEN_MODULES:
                    raise ValueError(f"Security restriction: Importing from '{root_module}' is not allowed in sandbox.")
        # Disallow forbidden functions
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                raise ValueError(f"Security restriction: Calling '{node.func.id}()' is prohibited.")

def run_safe_python_tests(user_code: str, test_cases: list, target_func_name: str = None) -> dict:
    """
    Executes student Python solution in an isolated, restricted environment against predefined test cases.
    Returns structured results:
    {
        "all_passed": bool,
        "passed_count": int,
        "total_count": int,
        "results": list of case dicts,
        "error": str or None
    }
    """
    if not user_code or not user_code.strip():
        return {
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(test_cases),
            "results": [],
            "error": "No code provided to test."
        }

    # 1. AST Safety check
    try:
        analyze_ast_safety(user_code)
    except Exception as e:
        return {
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(test_cases),
            "results": [],
            "error": str(e)
        }

    # 2. Build restricted namespace
    local_ns = {}
    global_ns = {
        "__builtins__": SAFE_BUILTINS,
        "math": math,
        "collections": collections,
        "Counter": collections.Counter,
        "defaultdict": collections.defaultdict,
        "deque": collections.deque,
        "heapq": heapq
    }

    try:
        exec(user_code, global_ns, local_ns)
    except Exception as e:
        return {
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(test_cases),
            "results": [],
            "error": f"Execution error while defining functions: {type(e).__name__}: {str(e)}"
        }

    # 3. Locate the entry function
    # Search either target_func_name or first defined callable in local_ns
    func = None
    if target_func_name and target_func_name in local_ns and callable(local_ns[target_func_name]):
        func = local_ns[target_func_name]
    else:
        for name, obj in local_ns.items():
            if callable(obj) and not name.startswith("_"):
                func = obj
                break

    if not func:
        return {
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(test_cases),
            "results": [],
            "error": "No callable function found in your code. Ensure you define the requested function."
        }

    # 4. Run test cases
    results = []
    passed_count = 0

    for idx, tc in enumerate(test_cases, start=1):
        args = tc.get("args", [])
        expected = tc.get("expected")
        case_res = {
            "test_case": idx,
            "args": args,
            "expected": expected,
            "got": None,
            "passed": False,
            "error": None
        }

        try:
            # Deepcopy-like behavior for list/dict args to prevent in-place mutation skewing tests
            import copy
            test_args = copy.deepcopy(args)
            output = func(*test_args)
            case_res["got"] = output

            # Handle comparisons (e.g. order of lists if applicable or direct equality)
            if output == expected:
                case_res["passed"] = True
                passed_count += 1
            else:
                case_res["passed"] = False
        except Exception as e:
            case_res["error"] = f"{type(e).__name__}: {str(e)}"
            case_res["passed"] = False

        results.append(case_res)

    all_passed = (passed_count == len(test_cases)) and len(test_cases) > 0
    return {
        "all_passed": all_passed,
        "passed_count": passed_count,
        "total_count": len(test_cases),
        "results": results,
        "error": None
    }

# -------------------------------------------------------------
# FORMATTING & GENERAL UTILS
# -------------------------------------------------------------

def format_timestamp(ts_str: str) -> str:
    """Format an ISO timestamp or date string to readable human format."""
    if not ts_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return ts_str

def get_readiness_badge_color(score: int) -> str:
    """Return color hex code based on readiness score."""
    if score >= 75:
        return "#28a745"  # Green
    elif score >= 50:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red
