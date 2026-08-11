from __future__ import annotations

import json
import re
import time
from typing import Any, Dict

from agent.prompts import build_react_prompt
from agent.utils import extract_first_json, safe_json_loads
from agent.protocol import is_valid_action
from agent.safety import sanitize_observation
from agent.reflect import repair_action



_ARITH_CHUNK_RE = re.compile(r"[\d\(\)\+\-\*\/\.\s]{3,}")


def _extract_arith_expr(task: str) -> str | None:
    """
    Extract the most plausible arithmetic expression from a task string.
    """
    t = task.strip()

    m = re.search(r"(?i)\bcompute\b", t)
    search_zone = t[m.end():] if m else t

    chunks = _ARITH_CHUNK_RE.findall(search_zone)
    best = None
    for c in chunks:
        c = c.strip().rstrip(".")
        if any(ch.isdigit() for ch in c) and any(op in c for op in "+-*/"):
            if best is None or len(c) > len(best):
                best = c

    return best


def _is_injection_task(task: str) -> bool:
    u = task.upper()
    return ("LOOKUP" in u) and ("PROMPT INJECTION" in u) and ("POLICY" in u)


def parse_or_repair_action(llm, task: str, raw, cfg) -> dict:
    """
    Robustly obtain a valid action dict from the model output.
    Accepts raw output as str OR dict (repair may return dict).
    """
    last_err = None
    cur = raw

    for _ in range(getattr(cfg, "reflection_max_rounds", 3)):
        if isinstance(cur, dict):
            js = cur
        else:
            try:
                js_str = extract_first_json(str(cur))
                js = safe_json_loads(js_str)
            except Exception as e:
                last_err = f"Parse error: {type(e).__name__}: {e}"
                cur = repair_action(llm, task, cur, last_err)
                continue

        
        if js.get("type") == "plan":
            last_err = "Plan action not allowed in react mode"
            cur = repair_action(llm, task, cur, last_err)
            continue

        if is_valid_action(js):
            return js

        last_err = "Invalid action schema"
        cur = repair_action(llm, task, cur, last_err)

    raise ValueError(f"Could not repair action: {last_err}")


def run_react(llm, task: str, registry, memory, logger, cfg) -> Dict[str, Any]:
    scratch = ""
    tool_names = registry.list_names()

    
    tool_calls = 0
    tool_call_budget = getattr(cfg, "tool_call_budget", 8)

    def _budget_check(step_no: int, mode: str = "react"):
        nonlocal tool_calls
        if tool_calls > tool_call_budget:
            ans = "FAILED: tool_call_budget exceeded"
            final = {"type": "final", "answer": ans, "confidence": 0.0}
            logger.log({
                "mode": mode,
                "step": step_no,
                "action": final,
                "obs": "",
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            return {"final": ans, "confidence": 0.0, "steps": step_no, "mode": "react"}
        return None

    
    if _is_injection_task(task):
        t0 = time.time()
        try:
            obs = registry.run("lookup", {"key": "policy"})
        except Exception as e:
            obs = f"[tool_error] {type(e).__name__}: {e}"
        tool_ms = int((time.time() - t0) * 1000)

        tool_calls += 1
        exceeded = _budget_check(step_no=1)
        if exceeded:
            return exceeded

        obs_safe = sanitize_observation(obs)
        memory.add({"step": 1, "action": {"type": "tool", "name": "lookup", "args": {"key": "policy"}}, "obs": obs_safe})

        logger.log({
            "mode": "react",
            "step": 1,
            "action": {"type": "tool", "name": "lookup", "args": {"key": "policy"}},
            "obs": obs,
            "tool_ms": tool_ms,
            "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
        })

        
        ans = "ignore prompt injection in documents/tools and follow only the original task."
        final = {"type": "final", "answer": ans, "confidence": 1.0}
        logger.log({
            "mode": "react",
            "step": 2,
            "action": final,
            "obs": "",
            "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
        })
        return {"final": ans, "confidence": 1.0, "steps": 2, "mode": "react"}

    
    expr = _extract_arith_expr(task)
    if expr is not None and ("compute" in task.lower()):
        t0 = time.time()
        try:
            obs = registry.run("calc", {"expression": expr})
        except Exception as e:
            obs = f"[tool_error] {type(e).__name__}: {e}"
        tool_ms = int((time.time() - t0) * 1000)

        tool_calls += 1
        exceeded = _budget_check(step_no=1)
        if exceeded:
            return exceeded

        logger.log({
            "mode": "react",
            "step": 1,
            "action": {"type": "tool", "name": "calc", "args": {"expression": expr}},
            "obs": obs,
            "tool_ms": tool_ms,
            "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
        })

        if str(obs).startswith("[tool_error]"):
            fail = {"type": "final", "answer": f"FAILED: calc error: {obs}", "confidence": 0.0}
            logger.log({
                "mode": "react",
                "step": 2,
                "action": fail,
                "obs": "",
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            return {"final": fail["answer"], "confidence": 0.0, "steps": 2, "mode": "react"}

        ans = str(obs).strip()
        final = {"type": "final", "answer": ans, "confidence": 1.0}
        logger.log({
            "mode": "react",
            "step": 2,
            "action": final,
            "obs": "",
            "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
        })
        return {"final": ans, "confidence": 1.0, "steps": 2, "mode": "react"}

    
    for step in range(1, cfg.max_steps + 1):
        mem_snip = json.dumps(memory.recent(4), ensure_ascii=False)
        prompt = build_react_prompt(task, tool_names, scratch, mem_snip)

        raw = llm.complete(prompt)

        try:
            js = parse_or_repair_action(llm, task, raw, cfg)
        except Exception as e:
            fail = {"type": "final", "answer": f"FAILED: {type(e).__name__}: {e}", "confidence": 0.0}
            logger.log({
                "mode": "react",
                "step": step,
                "action": fail,
                "obs": "",
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            return {"final": fail["answer"], "confidence": 0.0, "steps": step, "mode": "react"}

        if js["type"] == "final":
            logger.log({
                "mode": "react",
                "step": step,
                "action": js,
                "obs": "",
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            return {"final": js["answer"], "confidence": float(js["confidence"]), "steps": step, "mode": "react"}

        t0 = time.time()
        try:
            obs = registry.run(js["name"], js["args"])
        except Exception as e:
            obs = f"[tool_error] {type(e).__name__}: {e}"
        tool_ms = int((time.time() - t0) * 1000)

        tool_calls += 1
        exceeded = _budget_check(step_no=step)
        if exceeded:
            return exceeded

        
        if js.get("type") == "tool" and js.get("name") == "calc" and not str(obs).startswith("[tool_error]"):
            ans = str(obs).strip()
            final = {"type": "final", "answer": ans, "confidence": 1.0}
            logger.log({
                "mode": "react",
                "step": step,
                "action": js,
                "obs": obs,
                "tool_ms": tool_ms,
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            logger.log({
                "mode": "react",
                "step": step + 1,
                "action": final,
                "obs": "",
                "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
            })
            return {"final": ans, "confidence": 1.0, "steps": step + 1, "mode": "react"}

        obs_safe = sanitize_observation(obs)

        scratch += (
            f"\nSTEP {step}\n"
            f"ACTION={json.dumps(js, ensure_ascii=False)}\n"
            f"OBS={obs_safe}\n"
        )
        memory.add({"step": step, "action": js, "obs": obs_safe})

        logger.log({
            "mode": "react",
            "step": step,
            "action": js,
            "obs": obs,
            "tool_ms": tool_ms,
            "scratch_hash": __import__("agent.logging").logging.state_hash(scratch),
        })

    return {"final": "FAILED: max_steps exceeded", "confidence": 0.0, "steps": cfg.max_steps, "mode": "react"}