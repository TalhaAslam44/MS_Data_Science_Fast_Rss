from protocol import is_valid_action

# Examples of actions
tool_action = {"type": "tool", "name": "calc", "args": {"expression": "3*(4+5)"}}
final_action = {"type": "final", "answer": "27", "confidence": 0.95}
invalid_action = {"type": "tool", "name": "calc"}  # missing args

actions = [tool_action, final_action, invalid_action]

for action in actions:
    print(action, "->", is_valid_action(action))