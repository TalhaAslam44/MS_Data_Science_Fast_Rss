import json
from planner import run_plan_execute  # use your current planner.py

# --- Step 2: Mocks ---

# Mock LLM that returns a predictable 3-step plan
class MockLLM:
    def __init__(self):
        self.execution_counter = 0

    def complete(self, prompt: str):
        # If prompt contains "CURRENT PLAN STEP", we are executing
        if "CURRENT PLAN STEP" in prompt:
            self.execution_counter += 1
            if self.execution_counter == 1:
                return json.dumps({"type": "tool", "name": "calc", "args": {"expr": "27+53"}})
            elif self.execution_counter == 2:
                return json.dumps({"type": "tool", "name": "calc", "args": {"expr": "12-7"}})
            else:
                return json.dumps({"type": "final", "answer": "400", "confidence": 1.0})
        else:
            # Planning phase
            return json.dumps({
                "type": "plan",
                "steps": [
                    "Compute 27 + 53",
                    "Compute 12 - 7",
                    "Multiply the results"
                ]
            })

# Mock registry with a calc tool
class MockRegistry:
    def list_names(self):
        return ["calc"]
    def run(self, name, args):
        expr = args.get("expr")
        return eval(expr)  # simple safe eval for testing

# Simple memory
class MockMemory:
    def __init__(self):
        self.data = []
    def add(self, item):
        self.data.append(item)
    def recent(self, n):
        return self.data[-n:]

# Simple logger
class MockLogger:
    def log(self, msg):
        print(msg)

# Simple config
class MockCfg:
    plan_steps = 3
    max_steps = 10
    max_replans = 1

# --- Step 3: Run the planner execute ---
llm = MockLLM()
registry = MockRegistry()
memory = MockMemory()
logger = MockLogger()
cfg = MockCfg()

result = run_plan_execute(llm, "Compute (27+53)*(12-7)", registry, memory, logger, cfg)
print("Final result:", result)
