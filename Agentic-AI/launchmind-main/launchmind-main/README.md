># 🚀 LaunchMind
### *5 autonomous AI agents that think, build, market, and ship a startup — from a single idea*

> **"You give it one sentence. It gives you a GitHub PR, a live website, a Slack announcement, and a real email — fully automated."**

## 💡 The Startup Idea

**TutorConnect** — A mobile app that connects students with local tutors for personalized one-on-one learning experiences.

| | |
|---|---|
| 🎯 **Target User** | Students struggling with subjects + tutors looking for students |
| 💰 **Why pay for it** | Saves hours of searching, instant booking, secure payments |
| 🏆 **Core value** | Right tutor, right subject, right time |

---
## 🏗️ Agent Architecture

```
Startup Idea (text input)
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                    CEO AGENT                            │
│  Orchestrator: decomposes idea, reviews outputs,        │
│  sends revision requests, posts final Slack summary     │
└─────────────────────────┬───────────────────────────────┘
                          │
                      send tasks
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   PRODUCT     │  │   ENGINEER    │  │   MARKETING   │    Sends email via SendGrid
│    AGENT      │  │    AGENT      │  │    AGENT      │    Posts to Slack #launches
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        │ spec             │ builts HTML      │ 
        │                  │ commits to GitHub│
        |                  | opens PR         |
        └──────────────────┼──────────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │       QA AGENT        │
                │  reviews HTML + copy, │
                │  posts PR comments    │
                └───────────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ PASS / FAIL │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        If FAIL:                   If PASS:
        CEO sends                  CEO posts
        revision to                final summary
        Engineer                   to Slack 

💬 All communication = structured JSON messages via message_bus.py
🔄 CEO uses LLM twice – once to decompose, once to review (feedback loop)
```

---

## 🤖 What Each Agent Does

### 👔 CEO Agent — `agents/ceo_agent.py`
- Receives startup idea as plain text input
- Uses LLM to decompose idea into tasks, and to review each agent's output
- Sends `revision_request` if output is not good enough — **feedback loop**
- Posts final mission-complete summary to Slack

### 📋 Product Agent — `agents/product_agent.py`
- Receives task from CEO
- Generates full product spec: value proposition, 2 personas, 5 features, user stories
- Sends spec to both Engineer and Marketing agents

### 💻 Engineer Agent — `agents/engineer_agent.py`
- Receives product spec
- Generates HTML landing page using AI
- Creates GitHub branch → commits `index.html` → opens Issue → opens Pull Request
- Returns PR URL and Issue URL to CEO

### 📢 Marketing Agent — `agents/marketing_agent.py`
- Receives product spec
- Generates tagline, description, cold outreach email, social media posts
- Sends **real email** via SendGrid
- Posts **real Slack message** to `#launches` using Block Kit

### 🔍 QA Agent — `agents/qa_agent.py`
- Receives HTML + marketing copy from CEO
- Reviews both using LLM — checks headline, features, CTA, tone
- Posts **review comments directly on GitHub PR**
- Returns pass/fail verdict — if fail, CEO triggers revision

---

## 📨 Message Schema

Every agent-to-agent message follows this structure:

```json
{
  "message_id": "unique-id",
  "from_agent": "ceo",
  "to_agent": "product",
  "message_type": "task | result | revision_request | confirmation",
  "payload": {},
  "timestamp": "2026-04-10T00:00:00Z",
  "parent_message_id": "optional-parent-id"
}
```
---

## Platform Integrations

| Platform | What agents do |
|----------|---------------|
| **GitHub** | Engineer creates branch, commits `index.html`, opens PR, creates issue |
| **Slack** | Marketing posts launch message to `#launches`, CEO posts final summary |
| **SendGrid** | Marketing sends cold outreach email to test inbox |
| **Gorq API** | All agents use `llama-3.3-70b-versatile` (free tier, cloud-based) |
---

## 🔗 Live Proof — Real Actions Taken

| What | Link | Who did it |
|------|------|------------|
| GitHub Pull Request | [PR #34 — Initial landing page](https://github.com/HaiderRasoolQadri/launchmind/pull/34) | Engineer Agent |
| GitHub Issue | [Issue #33](https://github.com/HaiderRasoolQadri/launchmind/issues/33) | Engineer Agent |
| HTML Landing Page | [`index.html` on agent-landing-page branch](https://github.com/HaiderRasoolQadri/launchmind/blob/agent-landing-page-1775900586/index.html) | Engineer Agent |
| QA PR Comments | [View on PR #34](https://github.com/HaiderRasoolQadri/launchmind/pull/34) | QA Agent |

![alt text](image.png)
---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/HaiderRasoolQadri/launchmind.git
cd launchmind
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
copy .env.example .env
```
```
GITHUB_TOKEN=your_github_pat_here
GITHUB_REPO=HaiderRasoolQadri/launchmind
GITHUB_EMAIL=agent@launchmind.ai
SLACK_BOT_TOKEN=xoxb-your-token
SENDGRID_API_KEY=SG.your-key
SENDGRID_FROM_EMAIL=your@email.com
SENDGRID_TO_EMAIL=your@email.com
GROQ_API_KEY=gsk_your_groq_key_here
```

### 4. Run the system
```bash
python main.py
```

---
## 🔄 Feedback Loops Demonstrated

This run showed **3 real feedback loops**:

| Loop | From | To | Reason |
|------|------|----|--------|
| 1 | CEO | Product Agent | Output incomplete — missing user stories |
| 2 | CEO | Product Agent | Output lacking market analysis and revenue model |
| 3 | CEO → QA → Engineer | Engineer Agent | QA failed — HTML issues found |

> This is the dynamic decision-making — CEO used LLM reasoning to evaluate each output before deciding next action.
---

## 👥 Group Members

| Name | Agent | Responsibility |
|------|-------|---------------|
| Haider Rasool Qadri | CEO Agent + Engineer Agent | Orchestration, GitHub integration, HTML generation |
| Talha Aslam | Product Agent + Marketing Agent | Product spec, email, Slack, social copy |
| Muhammad Ahmer | QA Agent | HTML + copy review, PR comments, pass/fail verdict |

---

## Tech Stack
- **LLM:** Groq API + `llama-3.3-70b-versatile` (cloud, free tier)
- **Language:** Python 3.12.3
- **Message Bus:** Shared Python dictionary
- **GitHub API:** Direct HTTP calls via `requests`
- **Slack API:** Block Kit via `chat.postMessage`
- **Email:** SendGrid free tier

---

## ⚡ Key Highlights

- ✅ **Free LLM** — runs on Groq free tier (`llama-3.3-70b-versatile`)
- ✅ **Real GitHub PR** opened by agent — not simulated
- ✅ **Real email** delivered to inbox via SendGrid
- ✅ **Real Slack messages** posted using Block Kit
- ✅ **Multiple feedback loops** — CEO sent 2 revision requests to Product Agent, and 1 revision request to Engineer Agent via QA verdict
- ✅ **Structured JSON messages** — every agent communication is traceable
- ✅ **Full message log** — complete conversation history printed at runtime

> *"Built entirely by autonomous AI agents. No human did any of the startup work manually."*