import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from message_bus import send_message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SLACK_TOKEN     = os.getenv("SLACK_BOT_TOKEN")
SENDGRID_KEY    = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL      = os.getenv("SENDGRID_FROM_EMAIL")
TO_EMAIL        = os.getenv("SENDGRID_TO_EMAIL")

# # ── Ollama helper ──────────────────────────────────────────────────────────────
# def ask_groq(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False},
#         timeout=60
#     )
#     return response.json()["response"]

from llm_utils import ask_groq

# ── Generate all marketing copy ────────────────────────────────────────────────
def generate_copy(spec):
    vp = spec["value_proposition"]
    features = ", ".join([f["name"] for f in spec["features"][:3]])

    print("  → Generating tagline...")
    tagline = ask_groq(
        f'Write a product tagline under 10 words for: "{vp}". Reply with ONLY the tagline, no quotes, no extra text.'
    ).strip().strip('"').strip("'")

    print("  → Generating landing page description...")
    description = ask_groq(
        f'Write a 2-sentence product description for a landing page about: "{vp}". Be compelling and concise.'
    ).strip()

    print("  → Generating cold outreach email...")
    email_body = ask_groq(
        f'''Write a cold outreach email to a potential early user for this startup: "{vp}"
Key features: {features}
The email should have: a subject line on the first line starting with "Subject: ", then a blank line, then the email body.
Keep it under 150 words. Be friendly and specific.'''
    ).strip()

    print("  → Generating social media posts...")
    twitter = ask_groq(
        f'Write a Twitter/X post (max 280 chars) announcing this product: "{vp}". Include relevant hashtags.'
    ).strip()

    linkedin = ask_groq(
        f'Write a LinkedIn post (3-4 sentences) announcing this product: "{vp}". Professional tone.'
    ).strip()

    instagram = ask_groq(
        f'Write an Instagram caption (2-3 sentences + emojis) for: "{vp}".'
    ).strip()

    return {
        "tagline": tagline,
        "description": description,
        "email_body": email_body,
        "social": {
            "twitter": twitter,
            "linkedin": linkedin,
            "instagram": instagram
        }
    }

# ── Send email via SendGrid ────────────────────────────────────────────────────
def send_email(copy):
    print("  → Sending email via SendGrid...")

    # FIX SSL CERTIFICATE ERROR
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Get real values
    recipient_name = "Student"
    your_name = "LaunchMind AI Team"
    your_contact = "team@launchmind.ai"
    
    # Get product spec for features
    product_spec = copy.get('product_spec', {})
    features = product_spec.get('features', [])
    feature_names = [f.get('name', 'Tutor Matching') for f in features[:3]]
    
    # Professional, specific email prompt
    prompt = f"""Write a professional cold outreach email for "TutorConnect" - a mobile app connecting students with local tutors.

REQUIREMENTS:
1. Use recipient name: "{recipient_name}"
2. Mention "TutorConnect" in the first sentence
3. List these 3 specific features: {', '.join(feature_names)}
4. Include a clear benefit (e.g., "find a tutor in 5 minutes", "get help tonight")
5. Call-to-action: "Download TutorConnect today and get matched with your perfect tutor"
6. Signature: "Regards, {your_name}"
7. No brackets [] or placeholders
8. Keep under 150 words

Return ONLY the email body text, no subject line."""
    
    email_body = ask_groq(prompt).strip()
    
    # Professional subject line
    subject = "TutorConnect - Find Your Perfect Local Tutor Today"
    
    # Clean up the body
    lines = email_body.split('\n')
    clean_lines = []
    for line in lines:
        if not line.lower().startswith(('subject:', 'subject -', 're:', 'subject line')):
            # Replace any remaining placeholders
            line = line.replace('[Recipient Name]', recipient_name)
            line = line.replace('[Recipient\'s Name]', recipient_name)
            line = line.replace('[Your Name]', your_name)
            line = line.replace('[Your Contact Information]', your_contact)
            line = line.replace('[Your Contact Info]', your_contact)
            clean_lines.append(line)
    
    body_text = '\n'.join(clean_lines).strip()
    
    # Ensure proper signature exists
    if "Regards" not in body_text and "regards" not in body_text:
        body_text += f"\n\nRegards,\n{your_name}"
    if your_contact not in body_text:
        body_text += f"\n{your_contact}"
    
    body_html = body_text.replace('\n', '<br>')

    print(f"  📧 To: {TO_EMAIL}")
    print(f"  📧 Subject: {subject}")
    print(f"  📧 Body preview: {body_text[:200]}...")

    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=subject,
            html_content=f"<p>{body_html}</p>"
        )
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"  ✅ Email accepted by SendGrid (status 202)")
            print(f"  📧 Check inbox/spam in 2-5 minutes")
            return True
        else:
            print(f"  ❌ Email failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Email exception: {e}")
        return False
                    
# ── Post to Slack with Block Kit ───────────────────────────────────────────────
def post_to_slack(tagline, description, pr_url):
    print("  → Posting to Slack #launches...")

    pr_text = f"<{pr_url}|View PR>" if pr_url else "Not available yet"

    payload = {
        "channel": "#launches",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚀 New Launch: {tagline}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": description
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*GitHub PR:* {pr_text}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Status:* ✅ Ready for review"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Built by:* LaunchMind AI Agents"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Platform:* TutorConnect"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Social Posts Ready:*\n• Twitter ✅\n• LinkedIn ✅\n• Instagram ✅"
                }
            }
        ]
    }

    r = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
        json=payload
    )

    data = r.json()
    if data.get("ok"):
        print("  ✅ Slack message posted to #launches!")
        return True
    else:
        print(f"  ❌ Slack failed: {data.get('error')}")
        return False

# ── Main run function ──────────────────────────────────────────────────────────
def run(task_message, pr_url=None):
    print("\n📢 MARKETING AGENT: Starting...")
    spec    = task_message["payload"]["product_spec"]
    pr_url  = task_message["payload"].get("pr_url", pr_url)

    copy = generate_copy(spec)

    print(f"\n  📌 Tagline: {copy['tagline']}")
    print(f"  📝 Description: {copy['description'][:80]}...")

    email_sent = send_email(copy)
    slack_sent = post_to_slack(copy["tagline"], copy["description"], pr_url)

    result = {
        "status": "done",
        "tagline": copy["tagline"],
        "description": copy["description"],
        "email_sent": email_sent,
        "slack_sent": slack_sent,
        "social_posts": copy["social"]
    }

    send_message("marketing", "ceo", "result", result,
                 parent_message_id=task_message["message_id"])

    print("\n  🎉 Marketing Agent done!")
    return result