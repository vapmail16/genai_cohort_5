# =============================================================================
# SESSION 2 — Prompt Engineering & LLM Architecture
# File: 01_prompt_techniques.py
# Cohort 5 · 22 March 2026
#
# Run each section one at a time during the session.
# All techniques use the Acme Corp IT Support scenario.
# =============================================================================

import json
import os
from openai import OpenAI

from env_loader import load_env
load_env()
client = OpenAI()

DIVIDER = "\n" + "=" * 60 + "\n"


# =============================================================================
# TECHNIQUE 1 — ZERO-SHOT
# No examples. Just a clear instruction.
# The model decides the format entirely on its own.
# =============================================================================

print(DIVIDER + "TECHNIQUE 1 — ZERO-SHOT" + DIVIDER)

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.7,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful IT support assistant for Acme Corp."
        },
        {
            "role": "user",
            "content": "A user says their laptop won't connect to the office Wi-Fi. What should I tell them?"
        }
    ]
)

print(response.choices[0].message.content)

# ── Teaching point ───────────────────────────────────────────────────────────
# Notice: the response is helpful but the FORMAT is entirely up to the model.
# No priority. No category. No consistent structure.
# This is fine for simple tasks. It breaks down for production systems.
# Ask students: "What if you need to store this output in a database?"


# =============================================================================
# TECHNIQUE 2 — FEW-SHOT
# Show 2–5 examples of the exact input → output pattern you want.
# The model learns your format from the examples.
# Note: temperature=0 for consistent classification output.
# =============================================================================

print(DIVIDER + "TECHNIQUE 2 — FEW-SHOT" + DIVIDER)

few_shot_system = """You are a ticket classifier for Acme Corp IT support.

Examples:
Input: 'My email isn't loading'
Output: Category: Email & Communication | Priority: P3 - Medium

Input: 'Can't log into Salesforce since the update'
Output: Category: Software Access | Priority: P2 - High

Input: 'My keyboard stopped working'
Output: Category: Hardware | Priority: P3 - Medium

Input: 'The server room is on fire'
Output: Category: Infrastructure | Priority: P1 - Critical"""

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,          # Low temp = consistent classification every time
    messages=[
        {
            "role": "system",
            "content": few_shot_system
        },
        {
            "role": "user",
            "content": "Input: 'The whole London office internet is down'"
        }
    ]
)

print(response.choices[0].message.content)

# ── Teaching point ───────────────────────────────────────────────────────────
# TRY THIS LIVE:
#   1. Remove the P1 example from few_shot_system and re-run.
#      Ask: will it ever output P1 now?
#   2. Change temperature to 0.9 and run the classifier 3 times.
#      Show students why temp=0 is essential for classification.
# Key lesson: your examples define the space of possible outputs.


# =============================================================================
# TECHNIQUE 3 — CHAIN OF THOUGHT (CoT)
# Tell the model to show its reasoning before giving the final answer.
# Best for complex decisions — triage, prioritisation, diagnosis.
# The XML tags let us parse <thinking> and <answer> separately in code.
# =============================================================================

print(DIVIDER + "TECHNIQUE 3 — CHAIN OF THOUGHT" + DIVIDER)

cot_system = """You are an IT triage specialist at Acme Corp.

Before giving your response, reason through these steps:
1. Scope: How many people are affected?
2. Business impact: What happens if this is unresolved in 30 minutes?
3. Root cause options: What could be causing this?
4. Fastest resolution path?

Format your response EXACTLY as:
<thinking>
[Your step-by-step reasoning here]
</thinking>
<answer>
[Your final triage decision and recommended action]
</answer>"""

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.3,
    messages=[
        {
            "role": "system",
            "content": cot_system
        },
        {
            "role": "user",
            "content": (
                "Three engineers just reported their deployments are failing "
                "with 403 errors since 2pm. The CTO has a demo at 4pm."
            )
        }
    ]
)

print(response.choices[0].message.content)

# ── Teaching point ───────────────────────────────────────────────────────────
# TRY THIS LIVE:
#   Run the SAME scenario without the CoT instruction — just ask for a response.
#   Compare the quality and depth of the priority decision.
# Key lesson: CoT costs more tokens (= more time + cost) but dramatically
# improves accuracy on complex reasoning. Worth it for high-stakes decisions.
# The XML tags are not cosmetic — in Week 6 we will PARSE these tags
# to route a LangGraph agent's next action.


# =============================================================================
# TECHNIQUE 4 — TAG FRAMEWORK (Task · Actions · Guidelines)
# Structured system prompt that separates WHAT, HOW, and RULES.
# Makes prompts maintainable, testable, and easy to hand off.
# =============================================================================

print(DIVIDER + "TECHNIQUE 4 — TAG FRAMEWORK" + DIVIDER)

tag_system = """TASK:
Classify incoming IT support tickets and draft a first response.

ACTIONS:
1. Identify the ticket category:
   Hardware | Software | Network | Access | Other
2. Assign a priority level:
   P1 = Critical  (more than 5 users affected OR revenue blocked)
   P2 = High      (single user, time-sensitive)
   P3 = Medium    (inconvenient but a workaround exists)
   P4 = Low       (cosmetic or non-urgent)
3. Draft a 2-sentence empathetic first response.
   Use the user's name if provided.

GUIDELINES:
- Never promise a resolution time without engineering sign-off.
- Escalate all P1 tickets to the on-call engineer immediately.
- If the issue is unclear, ask exactly ONE clarifying question.
- Do not suggest rebooting as the first step for network issues."""

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.4,
    messages=[
        {
            "role": "system",
            "content": tag_system
        },
        {
            "role": "user",
            "content": (
                "User: Sarah\n"
                "Issue: I've been locked out of my account for 3 hours "
                "and I have a client presentation in 30 minutes."
            )
        }
    ]
)

print(response.choices[0].message.content)

# ── Teaching point ───────────────────────────────────────────────────────────
# Ask students: "What would you add to GUIDELINES to handle out-of-hours requests?"
# Key lesson: TAG makes your prompt testable.
# You can write code that checks: does output contain a category? a priority?
# Is the priority correct for this severity? That's what RAGAS does in Week 10.


# =============================================================================
# TECHNIQUE 5 — PIC FRAMEWORK (Persona · Instructions · Context)
# Better for customer-facing bots where personality matters.
# Context grounding reduces hallucination — model can't recommend
# tools/OS/software that Acme Corp doesn't use.
# =============================================================================

print(DIVIDER + "TECHNIQUE 5 — PIC FRAMEWORK" + DIVIDER)

pic_system = """PERSONA:
You are Alex, a senior IT support engineer at Acme Corp with 10 years
of experience. You are calm under pressure, use plain English (never
jargon), and always make users feel heard before jumping to solutions.

INSTRUCTIONS:
1. Acknowledge the user's frustration briefly (one sentence).
2. Diagnose the issue described.
3. If you need more information, ask exactly ONE clarifying question.
4. Provide the top 3 troubleshooting steps in numbered plain English.

CONTEXT:
Acme Corp standard environment:
- Operating system: Windows 11
- Email: Microsoft Outlook / Microsoft 365
- Networking: Cisco Meraki (802.1x authentication)
- VPN: Cisco AnyConnect
- Users are non-technical — assume no command-line knowledge."""

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5,
    messages=[
        {
            "role": "system",
            "content": pic_system
        },
        {
            "role": "user",
            "content": (
                "I keep getting a blue screen that says MEMORY_MANAGEMENT. "
                "It happens twice a day, usually when I'm on a video call."
            )
        }
    ]
)

print(response.choices[0].message.content)

# ── Teaching point ───────────────────────────────────────────────────────────
# Ask: "What happens if I remove the CONTEXT section?"
# Run it without CONTEXT — the model may suggest Linux commands or
# non-Microsoft tools. Context grounding prevents hallucinated advice.
# This is also why RAG exists — we'll extend this with real documents in Week 4.


# =============================================================================
# TECHNIQUE 6 — STRUCTURED JSON OUTPUT (response_format)
# Answers "What if you need to store this in a database?" from Technique 1.
# Use response_format={"type": "json_object"} so the model returns valid JSON.
# Then parse it and optionally store in PostgreSQL.
# =============================================================================

print(DIVIDER + "TECHNIQUE 6 — STRUCTURED JSON OUTPUT" + DIVIDER)

json_system = """You are a ticket classifier for Acme Corp IT support.

Return a JSON object with exactly these keys:
- "category": one of Hardware, Software, Network, Access, Other
- "priority": one of P1, P2, P3, P4
- "summary": one sentence describing the issue
- "first_response": 2-sentence empathetic reply to the user

Example:
{"category": "Network", "priority": "P2", "summary": "VPN drops every 20 minutes.", "first_response": "I'm sorry to hear that. Let's try a few steps..."}"""

json_user = "User: Mike. Issue: My laptop won't connect to the office Wi-Fi since this morning."

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,
    messages=[
        {"role": "system", "content": json_system},
        {"role": "user",   "content": json_user}
    ],
    response_format={"type": "json_object"},  # Forces valid JSON output
    max_tokens=200   # Classification output is short — cap it to save cost
)

raw_content = response.choices[0].message.content
print("Raw API response (JSON string):")
print(raw_content)

# Parse the JSON so we can use it in code
parsed = json.loads(raw_content)
print("\nParsed (Python dict):")
print(f"  category:      {parsed.get('category')}")
print(f"  priority:      {parsed.get('priority')}")
print(f"  summary:       {parsed.get('summary')}")
print(f"  first_response: {parsed.get('first_response', '')[:60]}...")

# ── Teaching point ───────────────────────────────────────────────────────────
# response_format={"type": "json_object"} guarantees parseable JSON.
# Without it, the model might return "Here is the JSON: {...}" with extra text.
# Now we can validate (check category in allowed list) and store in a database.


# =============================================================================
# OPTIONAL — Store in PostgreSQL (only if DATABASE_URL is set)
# Creates a simple tickets table and inserts the classified ticket.
# Run: createdb prompt_demo  (then set DATABASE_URL in .env)
# =============================================================================

# Only use PostgreSQL — SQLite URLs (from capstone) would fail with psycopg2
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.strip().lower().startswith("postgresql"):
    try:
        import psycopg2
        from psycopg2 import sql

        # Parse the connection URL (postgresql://user:pass@host:port/dbname)
        conn = psycopg2.connect(database_url)

        # Create table if not exists (idempotent)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    user_name TEXT,
                    raw_input TEXT,
                    category TEXT,
                    priority TEXT,
                    summary TEXT,
                    first_response TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            conn.commit()

        # Insert the classified ticket
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tickets (user_name, raw_input, category, priority, summary, first_response)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                "Mike",
                json_user,
                parsed.get("category"),
                parsed.get("priority"),
                parsed.get("summary"),
                parsed.get("first_response")
            ))
            inserted_id = cur.fetchone()[0]
            conn.commit()

        print(f"\n✓ Stored in PostgreSQL (ticket id={inserted_id})")
        conn.close()

    except ImportError:
        print("\n(psycopg2 not installed — run: pip install psycopg2-binary)")
    except Exception as e:
        print(f"\n(PostgreSQL optional — skipped: {e})")
else:
    if not database_url:
        print("\n(Set DATABASE_URL=postgresql://... in .env to store tickets. Skipping DB write.)")
    else:
        print("\n(DATABASE_URL must be PostgreSQL. Skipping DB write.)")

# ── Teaching point ───────────────────────────────────────────────────────────
# In production: validate parsed values (category in allowed list, priority valid)
# before inserting. Output validation (Layer 3 in 02_prompt_injection.py) checks
# the response before trusting it. JSON + schema validation = robust pipeline.
