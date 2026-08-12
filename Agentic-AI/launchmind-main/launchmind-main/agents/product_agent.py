import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from message_bus import send_message, get_messages

# def ask_groq(prompt):
#     """Call the local Ollama model."""
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "qwen2.5:1.5b",
#             "prompt": prompt,
#             "stream": False
#         },
#         timeout=60
#     )
#     return response.json()["response"]

from llm_utils import ask_groq

def parse_json_from_llm(text):
    """Extract JSON from LLM output even if it has extra text around it."""
    try:
        # Try direct parse first
        return json.loads(text)
    except:
        # Find the first { and last } and try parsing that
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != 0:
            try:
                return json.loads(text[start:end])
            except:
                pass
        # Return a safe fallback
        return None

def run(task_message):
    print("\n🧠 PRODUCT AGENT: Starting...")
    idea = task_message["payload"]["idea"]
    focus = task_message["payload"].get("focus", "")

    prompt = f"""You are a product manager. Given this startup idea: "{idea}"
{f'Focus on: {focus}' if focus else ''}

Respond with ONLY a JSON object, no extra text, no markdown, no backticks. Use this exact structure:
{{
  "value_proposition": "one sentence describing what the product does and for whom",
  "personas": [
    {{"name": "Name", "role": "their role", "pain_point": "specific problem they have"}},
    {{"name": "Name", "role": "their role", "pain_point": "specific problem they have"}}
  ],
  "features": [
    {{"name": "Feature name", "description": "what it does", "priority": 1}},
    {{"name": "Feature name", "description": "what it does", "priority": 2}},
    {{"name": "Feature name", "description": "what it does", "priority": 3}},
    {{"name": "Feature name", "description": "what it does", "priority": 4}},
    {{"name": "Feature name", "description": "what it does", "priority": 5}}
  ],
  "user_stories": [
    "As a [user], I want to [action] so that [benefit]",
    "As a [user], I want to [action] so that [benefit]",
    "As a [user], I want to [action] so that [benefit]"
  ]
}}"""

    print("  → Calling Ollama for product spec...")
    raw = ask_groq(prompt)
    spec = parse_json_from_llm(raw)

    if not spec:
        # Fallback spec if LLM output can't be parsed
        print("  ⚠️  Could not parse JSON, using structured fallback")
        spec = {
            "value_proposition": f"A platform that helps users with: {idea}",
            "personas": [
                {"name": "Alice", "role": "Primary user", "pain_point": "Lacks an easy solution"},
                {"name": "Bob", "role": "Secondary user", "pain_point": "Wastes time on manual tasks"}
            ],
            "features": [
                {"name": "Core feature", "description": "Main functionality", "priority": 1},
                {"name": "User accounts", "description": "Sign up and login", "priority": 2},
                {"name": "Dashboard", "description": "Overview of activity", "priority": 3},
                {"name": "Notifications", "description": "Alert users of updates", "priority": 4},
                {"name": "Search", "description": "Find content quickly", "priority": 5}
            ],
            "user_stories": [
                "As a user, I want to sign up easily so that I can start using the product",
                "As a user, I want to see a dashboard so that I can track my activity",
                "As a user, I want notifications so that I stay informed"
            ]
        }

    print(f"  ✅ Product spec ready: {spec['value_proposition']}")

    # Send spec to engineer and marketing
    send_message("product", "engineer", "task", {
        "product_spec": spec,
        "idea": idea
    }, parent_message_id=task_message["message_id"])

    send_message("product", "marketing", "task", {
        "product_spec": spec,
        "idea": idea
    }, parent_message_id=task_message["message_id"])

    # Send confirmation back to CEO
    send_message("product", "ceo", "confirmation", {
        "status": "done",
        "product_spec": spec
    }, parent_message_id=task_message["message_id"])

    return spec