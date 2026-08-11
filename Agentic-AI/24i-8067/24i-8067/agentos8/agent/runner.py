from __future__ import annotations
import argparse, json, hashlib

from agent.config import AgentConfig
from agent.llm import LLM
from agent.tools import ToolRegistry
from agent.memory import Memory
from agent.logging import TraceLogger
from harness.tools_harness import load_harness_tools
from agent.react import run_react
from agent.planner import run_plan_execute
from agent.tot import run_tot_execute


def _state_id(seed: int, task: str) -> str:
    h = hashlib.sha256(f"{seed}:{task}".encode("utf-8")).hexdigest()[:10]
    return f"s{seed}-{h}"


def build_llm(backend: str, cfg: AgentConfig):
    return LLM(backend=backend, timeout_s=cfg.llm_timeout_s)



import ast
import operator as op

_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _safe_arith_eval(expr: str) -> float:
    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _ALLOWED:
            return _ALLOWED[type(n.op)](_eval(n.left), _eval(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _ALLOWED:
            return _ALLOWED[type(n.op)](_eval(n.operand))
        raise ValueError("Unsupported expression")

    return _eval(node)

class CalculatorTool:
    name = "calc"

    def run(self, args):
        expr = (args or {}).get("expression", "")
        return str(_safe_arith_eval(expr))


def run_task(task: str, backend: str, mode: str, trace_path: str, seed: int) -> dict:
    cfg = AgentConfig(seed=seed)
    llm = build_llm(backend, cfg)

    reg = ToolRegistry()
    reg.register(CalculatorTool())
    load_harness_tools(registry=reg, seed=seed)

    mem = Memory()
    logger = TraceLogger(path=trace_path, state_id=_state_id(seed, task))

    if mode == "react":
        return run_react(llm, task, reg, mem, logger, cfg)

    if mode == "plan":
        return run_plan_execute(llm, task, reg, mem, logger, cfg)

    if mode == "tot":
        return run_tot_execute(llm, task, reg, mem, logger, cfg)

    if mode == "reflect":
        return run_react(llm, task, reg, mem, logger, cfg) | {"mode": "reflect"}

    raise ValueError("mode must be one of: react, plan, reflect, tot")


def run_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--backend", choices=["ollama", "groq"], default="ollama")
    ap.add_argument("--mode", choices=["react", "plan", "reflect", "tot"], default="react")
    ap.add_argument("--trace", default="trace.jsonl")
    ap.add_argument("--seed", type=int, default=123)
    args = ap.parse_args()

    res = run_task(args.task, args.backend, args.mode, args.trace, args.seed)
    print(json.dumps(res, ensure_ascii=False))