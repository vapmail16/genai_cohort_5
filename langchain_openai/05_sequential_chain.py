"""
BONUS DEMO: Sequential Chain — LCEL Composition
=================================================
What students learn:
  - How to chain multiple LLM calls together
  - How the output of one step becomes the input of the next
  - A real use case: classify issue → generate response → suggest ticket title

This shows the POWER of LCEL beyond a single prompt → LLM call.
Great for building intuition before agents are introduced in Week 6.

Run:
    python 05_sequential_chain.py
"""

from env_loader import load_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_env()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()


# ── Step 1: Classify the issue ────────────────────────────────────────────────
classify_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT support classifier.
Given a user's IT issue, respond with ONLY one of these categories:
PASSWORD | NETWORK | SOFTWARE | HARDWARE | ACCESS | UNKNOWN

Respond with the single category word only. Nothing else."""),
    ("human", "Issue: {issue}")
])

classify_chain = classify_prompt | llm | parser


# ── Step 2: Generate a helpful response ──────────────────────────────────────
respond_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT support assistant for Acme Corp.
You have already classified this issue as: {category}

Give a helpful, concise response (max 100 words).
If you cannot resolve it remotely, say a ticket will be raised."""),
    ("human", "Issue: {issue}")
])

respond_chain = respond_prompt | llm | parser


# ── Step 3: Suggest a ticket title ───────────────────────────────────────────
ticket_prompt = ChatPromptTemplate.from_messages([
    ("system", "Generate a short, professional IT ticket title (max 8 words) for this issue."),
    ("human", "Issue: {issue}\nCategory: {category}")
])

ticket_chain = ticket_prompt | llm | parser


# ── Wire it all together ──────────────────────────────────────────────────────
# RunnablePassthrough passes the original input through alongside new keys
full_chain = (
    RunnablePassthrough.assign(category=classify_chain)
    | RunnablePassthrough.assign(response=respond_chain)
    | RunnablePassthrough.assign(ticket_title=ticket_chain)
)


# ── Run it ────────────────────────────────────────────────────────────────────
test_issues = [
    "I forgot my password and can't log in to my laptop.",
    "My laptop screen has a big crack and won't display anything.",
    "The VPN disconnects every time I try to access the internal drive.",
]

for issue in test_issues:
    print("\n" + "=" * 60)
    print(f"🧑 Issue: {issue}")
    print("=" * 60)

    result = full_chain.invoke({"issue": issue})

    print(f"📂 Category:     {result['category']}")
    print(f"🎫 Ticket Title: {result['ticket_title']}")
    print(f"🤖 Response:\n   {result['response']}")
