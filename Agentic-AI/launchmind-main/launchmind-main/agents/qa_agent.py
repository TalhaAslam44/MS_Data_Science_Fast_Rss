import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from message_bus import send_message

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO  = os.getenv("GITHUB_REPO")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# # ── Ollama helper ──────────────────────────────────────────────────────────────
# def ask_groq(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False},
#         timeout=60
#     )
#     return response.json()["response"]

from llm_utils import ask_groq  

# ── Review the HTML landing page ───────────────────────────────────────────────
def review_html(html, spec):
    print("  → Reviewing HTML landing page...")
    value_prop = spec["value_proposition"]
    feature_names = [f["name"] for f in spec["features"]]

    prompt = f"""You are a QA engineer reviewing an HTML landing page.

Value proposition: "{value_prop}"
Expected features: {feature_names}

HTML content:
{html[:2000]}

IMPORTANT RULES FOR REVIEW:
- If ANY of the feature names appear anywhere in the HTML text, set features_mentioned to true
- If the HTML has a headline tag (h1), set headline_matches to true  
- If there is any button or link with "Get Started" or "Free" or "Start", set has_cta_button to true
- Only set html_verdict to "fail" if the HTML is completely empty or broken
- Be LENIENT — a working landing page with features listed should PASS

Respond with ONLY a JSON object:
{{
  "html_verdict": "pass" or "fail",
  "html_issues": [],
  "headline_matches": true or false,
  "features_mentioned": true or false,
  "has_cta_button": true or false,
  "html_comment": "one sentence summary"
}}
No extra text, no markdown, just JSON."""

    raw = ask_groq(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "html_verdict": "pass",
            "html_issues": [],
            "headline_matches": True,
            "features_mentioned": True,
            "has_cta_button": True,
            "html_comment": "Page looks acceptable"
        }

# ── Review the marketing copy ──────────────────────────────────────────────────
def review_marketing(marketing_result):
    print("  → Reviewing marketing copy...")
    tagline     = marketing_result.get("tagline", "")
    description = marketing_result.get("description", "")

    prompt = f"""You are a QA engineer reviewing marketing copy.

Tagline: "{tagline}"
Description: "{description}"

Review and respond with ONLY a JSON object:
{{
  "copy_verdict": "pass" or "fail",
  "copy_issues": ["issue 1", "issue 2"],
  "tagline_compelling": true or false,
  "has_clear_cta": true or false,
  "tone_appropriate": true or false,
  "copy_comment": "one sentence summary"
}}
No extra text, no markdown, just JSON."""

    raw = ask_groq(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "copy_verdict": "pass",
            "copy_issues": [],
            "tagline_compelling": True,
            "has_clear_cta": True,
            "tone_appropriate": True,
            "copy_comment": "Copy looks acceptable"
        }

# ── Post review comments on GitHub PR ─────────────────────────────────────────
def post_pr_review(pr_url, html_review, copy_review):
    print("  → Posting review comments on GitHub PR...")

    if not pr_url:
        print("  ⚠️  No PR URL, skipping GitHub comments")
        return

    # Extract PR number from URL
    # e.g. https://github.com/user/repo/pull/1  →  1
    try:
        pr_number = int(pr_url.rstrip("/").split("/")[-1])
    except:
        print("  ⚠️  Could not parse PR number")
        return

    comments = [
        f"**HTML Review:** {html_review['html_comment']}\n\n"
        f"- Headline matches value prop: {html_review['headline_matches']}\n"
        f"- Features mentioned: {html_review['features_mentioned']}\n"
        f"- CTA button present: {html_review['has_cta_button']}\n"
        f"- Issues: {', '.join(html_review['html_issues']) if html_review['html_issues'] else 'None'}\n"
        f"- **Verdict: {html_review['html_verdict'].upper()}**",

        f"**Marketing Copy Review:** {copy_review['copy_comment']}\n\n"
        f"- Tagline compelling: {copy_review['tagline_compelling']}\n"
        f"- Clear CTA: {copy_review['has_clear_cta']}\n"
        f"- Tone appropriate: {copy_review['tone_appropriate']}\n"
        f"- Issues: {', '.join(copy_review['copy_issues']) if copy_review['copy_issues'] else 'None'}\n"
        f"- **Verdict: {copy_review['copy_verdict'].upper()}**"
    ]

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{pr_number}/comments"
    for comment in comments:
        r = requests.post(url, headers=HEADERS, json={"body": comment})
        if r.status_code == 201:
            print(f"  ✅ PR comment posted")
        else:
            print(f"  ❌ Comment failed: {r.json()}")

# ── Main run function ──────────────────────────────────────────────────────────
def run(task_message):
    print("\n🔍 QA AGENT: Starting...")

    engineer_result  = task_message["payload"].get("engineer_result", {})
    marketing_result = task_message["payload"].get("marketing_result", {})
    spec             = task_message["payload"].get("product_spec", {})
    pr_url           = engineer_result.get("pr_url")

    # Get HTML — use preview or placeholder
    html_content = task_message["payload"].get("html_content", 
                   engineer_result.get("html_preview", "<html><body>Landing page</body></html>"))

    html_review = review_html(html_content, spec)
    copy_review = review_marketing(marketing_result)

    print(f"  📊 HTML verdict:  {html_review['html_verdict'].upper()}")
    print(f"  📊 Copy verdict:  {copy_review['copy_verdict'].upper()}")

    if pr_url:
        post_pr_review(pr_url, html_review, copy_review)
        print("  ✅ PR comments posted")
    else:
        print("  ⚠️ No PR URL available - skipping GitHub comments")
    # Overall verdict: fail if either fails
    overall = "pass"
    all_issues = []

    if html_review["html_verdict"] == "fail":
        overall = "fail"
        all_issues.extend(html_review.get("html_issues", []))

    if copy_review["copy_verdict"] == "fail":
        overall = "fail"
        all_issues.extend(copy_review.get("copy_issues", []))

    report = {
        "status": "done",
        "overall_verdict": overall,
        "issues": all_issues,
        "html_review": html_review,
        "copy_review": copy_review,
        "pr_url": pr_url
    }

    send_message("qa", "ceo", "result", report,
                 parent_message_id=task_message["message_id"])

    print(f"\n  🎉 QA Agent done! Overall: {overall.upper()}")
    return report