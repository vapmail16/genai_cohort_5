"""
DEMO 3: The One-Line Model Switch
===================================
What students learn:
  - LangChain's key selling point: provider-agnostic code
  - Same chain, three different models: OpenAI, Anthropic, Ollama (local)
  - How to switch without rewriting your application logic

Run:
    python 03_model_switch.py

Requirements:
  - OpenAI:    OPENAI_API_KEY in .env
  - Anthropic: ANTHROPIC_API_KEY in .env   (optional)
  - Ollama:    Run `ollama pull llama3.2` then `ollama serve`  (optional)
"""

import os
from env_loader import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_env()

# ── The SAME prompt used for every model ──────────────────────────────────────
SYSTEM_PROMPT = "You are an IT support assistant for Acme Corp. Be concise."
TEST_QUESTION  = "An employee says: my laptop won't connect to the VPN and I'm getting error 422. What should I do?"

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

output_parser = StrOutputParser()


def run_with_model(label: str, llm):
    """Build the chain and run the same question through any LLM."""
    print(f"\n{'=' * 60}")
    print(f"  MODEL: {label}")
    print(f"{'=' * 60}")

    # ── This is the key teaching moment ──────────────────────────────────────
    # The CHAIN is identical no matter which LLM you plug in.
    # Swap the llm object → everything else stays the same.
    chain = prompt | llm | output_parser

    response = chain.invoke({"question": TEST_QUESTION})
    print(f"🤖 {response}")


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 1: OpenAI GPT-4o
# ─────────────────────────────────────────────────────────────────────────────
if os.getenv("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI
    run_with_model(
        label="OpenAI GPT-4o  (cloud, paid)",
        llm=ChatOpenAI(model="gpt-4o", temperature=0)
    )
else:
    print("\n⚠️  OPENAI_API_KEY not set — skipping OpenAI demo")


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 2: Anthropic Claude
# ─────────────────────────────────────────────────────────────────────────────
if os.getenv("ANTHROPIC_API_KEY"):
    from langchain_anthropic import ChatAnthropic
    run_with_model(
        label="Anthropic Claude Sonnet  (cloud, paid)",
        llm=ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
    )
else:
    print("\n⚠️  ANTHROPIC_API_KEY not set — skipping Anthropic demo")


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 3: Ollama — fully local, no API key, no cost (offline_model_setup)
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")  # matches offline_model_setup
try:
    from langchain_ollama import ChatOllama
    run_with_model(
        label="Ollama Llama 3.2  (LOCAL — free, private)",
        llm=ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0,
        )
    )
except Exception as e:
    print(f"\n⚠️  Ollama not available ({e})")
    print("   To enable: run `offline_model_setup/setup.sh` or `ollama pull llama3.2:3b` then `ollama serve`")


# ─────────────────────────────────────────────────────────────────────────────
# TEACHING MOMENT: Print the summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("KEY TAKEAWAY:")
print("=" * 60)
print("""
The chain code is IDENTICAL for all three models:

    chain = prompt | llm | output_parser

The ONLY thing that changed was this one line:

    llm = ChatOpenAI(...)          ← cloud, costs money
    llm = ChatAnthropic(...)       ← cloud, costs money
    llm = ChatOllama(...)          ← local, FREE, private

This is why we use LangChain throughout this course.
Your architecture is never locked to one provider.
""")
