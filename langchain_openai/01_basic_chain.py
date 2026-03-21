"""
DEMO 1: Your First LangChain Chain
===================================
What students learn:
  - What LCEL (LangChain Expression Language) is and why the pipe | syntax exists
  - How a chain is: Prompt → LLM → Output Parser
  - How to wire in a system prompt
  - The difference between .invoke() and just calling the API directly

Run:
    python 01_basic_chain.py
"""

from env_loader import load_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Load environment variables from monorepo .env ──────────────────────────────
load_env()

# ── Step 1: Define the LLM ────────────────────────────────────────────────────
# temperature=0 → deterministic, good for support bots
# temperature=1 → creative, good for creative writing
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# ── Step 2: Define the Prompt Template ───────────────────────────────────────
# The system message shapes HOW the model behaves
# The human message is the user's input (filled in at runtime)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT support assistant for Acme Corp.
You help employees with technical issues clearly and concisely.
Always ask for one clarifying detail if you need it.
Keep responses under 150 words."""),
    ("human", "{question}")
])

# ── Step 3: Build the Chain with LCEL ─────────────────────────────────────────
# The | pipe operator chains components left to right:
#   prompt takes the dict → formats it into messages
#   llm takes the messages → returns an AIMessage object
#   StrOutputParser takes the AIMessage → returns a plain string
chain = prompt | llm | StrOutputParser()

# ── TEACHING MOMENT: What does the prompt look like before it hits the LLM? ──
print("=" * 60)
print("WHAT THE PROMPT LOOKS LIKE (before LLM sees it):")
print("=" * 60)
formatted = prompt.format_messages(question="My laptop won't connect to WiFi")
for msg in formatted:
    print(f"[{msg.__class__.__name__}] {msg.content}")
print()

# ── Step 4: Run the chain ─────────────────────────────────────────────────────
print("=" * 60)
print("RESPONSE FROM THE CHAIN:")
print("=" * 60)

questions = [
    "My laptop won't connect to the office WiFi.",
    "I keep getting error 422 when connecting to the VPN.",
    "How do I reset my password?",
]

for q in questions:
    print(f"\n🧑 User: {q}")
    response = chain.invoke({"question": q})
    print(f"🤖 Bot:  {response}")
    print("-" * 60)
