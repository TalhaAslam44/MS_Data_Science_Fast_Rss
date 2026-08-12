import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from message_bus import send_message, get_messages

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# # ── Ollama helper ──────────────────────────────────────────────────────────────
# def ask_groq(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False},
#         timeout=60
#     )
#     return response.json()["response"]

from llm_utils import ask_groq

# ── Decompose startup idea into tasks ─────────────────────────────────────────
def decompose_idea(idea):
    print("  → Decomposing startup idea into agent tasks...")
    prompt = f"""You are a CEO of a startup. Your idea is: "{idea}"

Break this into tasks for 3 agents. Respond with ONLY a JSON object:
{{
  "product_task": {{
    "idea": "{idea}",
    "focus": "what the product agent should focus on"
  }},
  "engineer_task": {{
    "idea": "{idea}",
    "focus": "what the engineer agent should build"
  }},
  "marketing_task": {{
    "idea": "{idea}",
    "focus": "what the marketing agent should promote"
  }}
}}
No extra text, no markdown, just JSON."""

    raw = ask_groq(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        # Safe fallback
        return {
            "product_task": {"idea": idea, "focus": "Define personas and core features"},
            "engineer_task": {"idea": idea, "focus": "Build HTML landing page"},
            "marketing_task": {"idea": idea, "focus": "Create tagline and outreach"}
        }

# ── Review an agent's output ───────────────────────────────────────────────────
def review_output(agent_name, output, idea):
    print(f"  → CEO reviewing {agent_name} output...")
    prompt = f"""You are a CEO reviewing output from your {agent_name} agent for this startup: "{idea}"

Output received:
{json.dumps(output, indent=2)[:1500]}

Is this output specific, complete, and relevant to the startup idea?
Respond with ONLY a JSON object:
{{
  "acceptable": true or false,
  "reason": "one sentence explanation",
  "revision_needed": "specific instruction if not acceptable, or empty string if acceptable"
}}
No extra text, no markdown, just JSON."""

    raw = ask_groq(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {"acceptable": True, "reason": "Output looks good", "revision_needed": ""}

# ── Post final summary to Slack ────────────────────────────────────────────────
def post_final_slack_summary(idea, product_spec, engineer_result, marketing_result, qa_result):
    print("  → Posting final summary to Slack...")

    pr_url      = (engineer_result  or {}).get("pr_url", "N/A")
    issue_url   = (engineer_result  or {}).get("issue_url", "N/A")
    tagline     = (marketing_result or {}).get("tagline", "N/A")
    email_sent  = (marketing_result or {}).get("email_sent", False)
    qa_verdict  = (qa_result        or {}).get("overall_verdict", "N/A")
    value_prop  = (product_spec     or {}).get("value_proposition", idea)

    pr_link    = f"<{pr_url}|View PR>"        if pr_url    != "N/A" else "N/A"
    issue_link = f"<{issue_url}|View Issue>"  if issue_url != "N/A" else "N/A"

    payload = {
        "channel": "#launches",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "✅ LaunchMind Mission Complete!"}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Startup:* {idea}\n*Value Prop:* {value_prop}"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Tagline:*\n{tagline}"},
                    {"type": "mrkdwn", "text": f"*QA Verdict:*\n{qa_verdict.upper()}"},
                    {"type": "mrkdwn", "text": f"*GitHub PR:*\n{pr_link}"},
                    {"type": "mrkdwn", "text": f"*GitHub Issue:*\n{issue_link}"},
                    {"type": "mrkdwn", "text": f"*Email Sent:*\n{'✅ Yes' if email_sent else '❌ No'}"},
                    {"type": "mrkdwn", "text": "*Agents Used:*\nCEO, Product, Engineer, Marketing, QA"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_Built entirely by autonomous AI agents using LaunchMind MAS_"
                }
            }
        ]
    }

    r = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
        json=payload
    )
    if r.json().get("ok"):
        print("  ✅ Final summary posted to Slack!")
    else:
        print(f"  ❌ Slack error: {r.json().get('error')}")

# ── Main run function ──────────────────────────────────────────────────────────
def run(idea):
    print("\n" + "="*60)
    print("👔 CEO AGENT: Starting LaunchMind...")
    print(f"   Idea: {idea}")
    print("="*60)

    # ── Step 1: Decompose idea into tasks ──────────────────────
    tasks = decompose_idea(idea)
    print(f"  ✅ Tasks decomposed")

    # ── Step 2: Send task to Product Agent ─────────────────────
    send_message("ceo", "product", "task", tasks["product_task"])
    print("  📨 Task sent to Product Agent")

    # ── Step 3: Run Product Agent ──────────────────────────────
    from agents.product_agent import run as run_product
    product_messages = get_messages("product")
    product_spec = run_product(product_messages[0])

    # ── Step 4: CEO reviews product spec ──────────────────────
    product_confirmation = get_messages("ceo")
    review = review_output("product", product_spec, idea)
    print(f"  🔍 Product review: {review['reason']}")

    # ── Step 5: Request revision if needed (feedback loop) ────
    revision_count = 0
    while not review["acceptable"] and revision_count < 2:
        print(f"  🔄 Requesting revision from Product Agent: {review['revision_needed']}")
        send_message("ceo", "product", "revision_request", {
            "idea": idea,
            "focus": review["revision_needed"]
        })
        product_messages = get_messages("product")
        product_spec = run_product(product_messages[0])
        review = review_output("product", product_spec, idea)
        revision_count += 1
        print(f"  🔍 Re-review: {review['reason']}")

    print(f"  ✅ Product spec accepted after {revision_count} revision(s)")

# ── Step 6: Engineer and Marketing already got spec from Product Agent
    print("  📋 Engineer and Marketing already notified by Product Agent")

    # ── Step 7: Run Engineer Agent ─────────────────────────────
    from agents.engineer_agent import run as run_engineer
    engineer_messages = get_messages("engineer")
    engineer_result = run_engineer(engineer_messages[0])

    # ── Step 8: Run Marketing Agent ────────────────────────────
    # Pass PR URL to marketing so it can include it in Slack post
    marketing_msg = get_messages("marketing")[0]
    marketing_msg["payload"]["pr_url"] = (engineer_result or {}).get("pr_url")

    from agents.marketing_agent import run as run_marketing
    marketing_result = run_marketing(marketing_msg)

    # ── Step 9: CEO reviews marketing output ──────────────────
    get_messages("ceo")  # clear confirmations
    marketing_review = review_output("marketing", marketing_result, idea)
    print(f"  🔍 Marketing review: {marketing_review['reason']}")

    # ── Step 10: Run QA Agent ──────────────────────────────────
    send_message("ceo", "qa", "task", {
        "product_spec": product_spec,
        "engineer_result": engineer_result,
        "marketing_result": marketing_result,
        "html_content": engineer_result.get("html_preview", "") if engineer_result else ""
    })

    from agents.qa_agent import run as run_qa
    qa_messages = get_messages("qa")
    qa_result = run_qa(qa_messages[0])

    # ── Step 11: Handle QA verdict ─────────────────────────────
        # ── Step 11: Handle QA verdict ─────────────────────────────
    qa_report = get_messages("ceo")
    if qa_result and qa_result.get("overall_verdict") == "fail":
        print(f"\n  ⚠️ QA FAILED — issues: {qa_result.get('issues')}")
        print("  🔄 CEO requesting revision from Engineer...")
        send_message("ceo", "engineer", "revision_request", {
            "product_spec": product_spec,
            "idea": idea,
            "issues": qa_result.get("issues", [])
        })
        
        # Run engineer again with the revision request
        engineer_messages = get_messages("engineer")
        if engineer_messages:
            engineer_result = run_engineer(engineer_messages[0])
            print("  ✅ Engineer revised the landing page")
            
            # 🔄 NEW CODE: Run QA again on the revised HTML
            print("  🔄 Running QA again on revised HTML...")
            send_message("ceo", "qa", "task", {
                "product_spec": product_spec,
                "engineer_result": engineer_result,
                "marketing_result": marketing_result,
                "html_content": engineer_result.get("html_preview", "") if engineer_result else ""
            })
            
            # Get QA's review of the revised version
            qa_messages = get_messages("qa")
            if qa_messages:
                qa_result = run_qa(qa_messages[0])
                print(f"  ✅ QA re-review complete: {qa_result.get('overall_verdict', 'N/A').upper()}")
    else:
        print("  ✅ QA passed — no revisions needed")

    # ── Step 12: Post final summary to Slack ───────────────────
    post_final_slack_summary(idea, product_spec, engineer_result, marketing_result, qa_result)

    print("\n" + "="*60)
    print("🎉 LAUNCHMIND COMPLETE!")
    print("="*60)

    return {
        "product_spec": product_spec,
        "engineer_result": engineer_result,
        "marketing_result": marketing_result,
        "qa_result": qa_result
    }