import json
import uuid
from datetime import datetime

# This is the shared message bus - a dictionary where each key is an agent name
# and the value is a list of messages waiting for that agent
message_bus = {
    "ceo": [],
    "product": [],
    "engineer": [],
    "marketing": [],
    "qa": []
}

# Keeps a log of every single message ever sent - for your demo
message_log = []

def send_message(from_agent, to_agent, message_type, payload, parent_message_id=None):
    """Send a structured JSON message from one agent to another."""
    message = {
        "message_id": str(uuid.uuid4())[:8],
        "from_agent": from_agent,
        "to_agent": to_agent,
        "message_type": message_type,  # task / result / revision_request / confirmation
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "parent_message_id": parent_message_id
    }
    message_bus[to_agent].append(message)
    message_log.append(message)
    print(f"\n📨 [{from_agent.upper()} → {to_agent.upper()}] type={message_type}")
    return message["message_id"]

def get_messages(agent_name):
    """Get all pending messages for an agent and clear the queue."""
    messages = message_bus[agent_name].copy()
    message_bus[agent_name] = []
    return messages

def print_full_log():
    """Print every message ever sent - useful for demo."""
    print("\n" + "="*60)
    print("FULL MESSAGE LOG")
    print("="*60)
    for msg in message_log:
        print(json.dumps(msg, indent=2))
        print("-"*40)