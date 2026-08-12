import requests
import json
import base64
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from message_bus import send_message

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO  = os.getenv("GITHUB_REPO")
GITHUB_EMAIL = os.getenv("GITHUB_EMAIL", "agent@launchmind.ai")
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

# ── HTML generator ─────────────────────────────────────────────────────────────
def generate_landing_page(spec):
    value_prop = spec["value_proposition"]
    features = spec["features"][:5]
    
    # Stronger prompt for Groq - demand complete HTML
    prompt = f"""You are an expert web developer. Create a COMPLETE HTML landing page for a startup with this value proposition: "{value_prop}"

REQUIREMENTS (MUST include all):
1. A catchy headline (max 10 words)
2. A subheadline (one sentence)
3. A "Get Started Free" call-to-action button (green, clickable)
4. A features section with exactly {len(features)} feature cards
5. Each feature card must have a title and description

The features are:
{chr(10).join([f'- {f["name"]}: {f["description"]}' for f in features])}

Return ONLY complete HTML code (starting with <!DOCTYPE html> and ending with </html>). Include CSS styling. Do not add any explanations."""
    
    full_html = ask_groq(prompt).strip()
    
    # Extract just the HTML if LLM added extra text
    if "<!DOCTYPE html" in full_html:
        start = full_html.find("<!DOCTYPE html")
        end = full_html.rfind("</html>") + 7
        html = full_html[start:end]
    else:
        html = full_html
    
    # Fallback: ensure CTA button exists
    if "Get Started" not in html and "cta" not in html.lower():
        # Add CTA button if missing
        html = html.replace("</header>", '<a class="cta" href="#">Get Started Free</a>\n</header>')
    
    return html

# ── GitHub helpers ─────────────────────────────────────────────────────────────
def get_main_sha():
    """Get the latest commit SHA from main branch."""
    for branch in ["main", "master"]:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/git/refs/heads/{branch}"
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        if r.status_code == 200 and isinstance(data, dict) and "object" in data:
            print(f"  ✅ Found branch: {branch}")
            return data["object"]["sha"]
        elif r.status_code == 200 and isinstance(data, list) and len(data) > 0:
            print(f"  ✅ Found branch: {branch}")
            return data[0]["object"]["sha"]
    raise Exception("Could not find main or master branch. Make sure your repo has at least one commit.")

def create_branch(sha):
    """Create a new branch with unique name using timestamp."""
    timestamp = int(time.time())
    branch_name = f"agent-landing-page-{timestamp}"
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/git/refs"
    r = requests.post(url, headers=HEADERS, json={
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    })
    if r.status_code == 422:
        print(f"  ⚠️ Branch {branch_name} already exists? Retrying with new timestamp...")
        time.sleep(1)
        return create_branch(sha)
    elif r.status_code == 201:
        print(f"  ✅ Branch created: {branch_name}")
        return branch_name
    else:
        print(f"  ❌ Branch creation failed: {r.status_code}")
        return None

def commit_file(html_content, sha, branch_name):
    """Commit index.html to the specified branch."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/index.html"
    encoded = base64.b64encode(html_content.encode()).decode()

    # Check if file already exists on this branch
    try:
        existing = requests.get(
            url + f"?ref={branch_name}",
            headers=HEADERS,
            timeout=30
        )
        existing_sha = existing.json().get("sha") if existing.status_code == 200 else None
    except Exception:
        existing_sha = None

    body = {
        "message": f"Add landing page [by EngineerAgent <agent@launchmind.ai>]",
        "content": encoded,
        "branch": branch_name,
        "author": {
            "name": "EngineerAgent",
            "email": GITHUB_EMAIL
        }
    }
    if existing_sha:
        body["sha"] = existing_sha

    # Retry up to 3 times
    for attempt in range(1, 4):
        try:
            print(f"  → Commit attempt {attempt}/3...")
            r = requests.put(
                url,
                headers=HEADERS,
                json=body,
                timeout=30
            )
            if r.status_code in [200, 201]:
                print(f"  ✅ index.html committed to {branch_name}")
                return True
            else:
                print(f"  ⚠️  Attempt {attempt} failed: {r.status_code}")
        except Exception as e:
            print(f"  ⚠️  Attempt {attempt} error: {e}")
        time.sleep(3)

    print("  ❌ All commit attempts failed")
    return False

def create_issue(spec):
    """Create a GitHub issue for the landing page task."""
    prompt = f"""Write a short GitHub issue description (3-4 sentences) for creating a landing page for this startup: {spec['value_proposition']}. Be specific and technical. No markdown headers."""
    body = ask_groq(prompt).strip()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    r = requests.post(url, headers=HEADERS, timeout=15,json={
        "title": "Initial landing page",
        "body": body,
        "labels": []
    })
    if r.status_code == 201:
        issue_url = r.json()["html_url"]
        print(f"  ✅ Issue created: {issue_url}")
        return issue_url
    else:
        print(f"  ❌ Issue failed: {r.json()}")
        return None
    
def get_existing_pr(branch_name):
    """Check if a PR already exists for the given branch and return its URL."""
    repo_owner = GITHUB_REPO.split('/')[0]
    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls?head={repo_owner}:{branch_name}&state=open"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200 and r.json():
        pr_url = r.json()[0]["html_url"]
        print(f"  ℹ️ Existing PR found: {pr_url}")
        return pr_url
    return None

def create_pull_request(spec, branch_name):
    """Open a pull request from branch → main. Check if PR already exists first."""
    # First check if PR already exists
    existing_pr = get_existing_pr(branch_name)
    if existing_pr:
        return existing_pr
    
    # Otherwise create new
    prompt = f"""Write a short GitHub pull request description (3-4 sentences) for a landing page for: {spec['value_proposition']}. Mention what was built and why. No markdown headers."""
    body = ask_groq(prompt).strip()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls"
    r = requests.post(url, headers=HEADERS, json={
        "title": "Initial landing page — built by EngineerAgent",
        "body": body,
        "head": branch_name,
        "base": "main"
    })
    if r.status_code == 201:
        pr_url = r.json()["html_url"]
        print(f"  ✅ Pull request opened: {pr_url}")
        return pr_url
    else:
        print(f"  ❌ PR failed: {r.json()}")
        return None

# ── Main run function ──────────────────────────────────────────────────────────
def run(task_message):
    print("\n🔧 ENGINEER AGENT: Starting...")
    spec = task_message["payload"]["product_spec"]

    print("  → Generating HTML landing page...")
    html = generate_landing_page(spec)
    print(f"  ✅ HTML generated ({len(html)} characters)")

    print("  → Getting main branch SHA from GitHub...")
    try:
        sha = get_main_sha()
    except Exception as e:
        print(f"  ❌ Could not get SHA: {e}")
        send_message("engineer", "ceo", "result", {
            "status": "error",
            "error": str(e)
        }, parent_message_id=task_message["message_id"])
        return None

    print("  → Creating branch...")
    branch_name = create_branch(sha)
    if not branch_name:
        print("  ❌ Branch creation failed")
        send_message("engineer", "ceo", "result", {
            "status": "error",
            "error": "Branch creation failed"
        }, parent_message_id=task_message["message_id"])
        return None
    time.sleep(1)

    print("  → Committing index.html...")
    commit_file(html, sha, branch_name)
    time.sleep(1)

    print("  → Creating GitHub issue...")
    issue_url = create_issue(spec)
    time.sleep(1)

    print("  → Opening pull request...")
    pr_url = create_pull_request(spec, branch_name)

    result = {
        "status": "done",
        "pr_url": pr_url,
        "issue_url": issue_url,
        "html_preview": html,
        "html_length": len(html)
    }

    send_message("engineer", "ceo", "result", result,
                 parent_message_id=task_message["message_id"])

    print("\n  🎉 Engineer Agent done!")
    return result