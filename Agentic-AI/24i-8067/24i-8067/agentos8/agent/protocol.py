from __future__ import annotations

from typing import Any, Dict


def is_valid_tool_action(x: Dict[str, Any]) -> bool:
    return (
        isinstance(x, dict)
        and x.get("type") == "tool"
        and isinstance(x.get("name"), str)
        and len(x["name"]) > 0
        and isinstance(x.get("args"), dict)
    )


def is_valid_final_action(x: Dict[str, Any]) -> bool:
    return (
        isinstance(x, dict)
        and x.get("type") == "final"
        and isinstance(x.get("answer"), str)
        and "confidence" in x
        and isinstance(x.get("confidence"), (int, float))
        and 0.0 <= float(x["confidence"]) <= 1.0
    )


def is_valid_plan(x: Dict[str, Any]) -> bool:
    # Plan schema expected by tests: {"type":"plan","steps":[...]}
    if not (isinstance(x, dict) and x.get("type") == "plan"):
        return False
    steps = x.get("steps")
    if not isinstance(steps, list) or len(steps) == 0:
        return False
    # tests use list[str], keep it strict
    return all(isinstance(s, str) and len(s) > 0 for s in steps)


def is_valid_action(x: Dict[str, Any]) -> bool:
    """
    Public tests expect this to accept tool/final/plan.
    """
    return is_valid_tool_action(x) or is_valid_final_action(x) or is_valid_plan(x)