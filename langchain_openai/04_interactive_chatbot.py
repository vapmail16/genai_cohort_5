"""
DEMO 4: Interactive Acme Corp IT Support Chatbot
=================================================
What students learn:
  - How to build an interactive chat loop in the terminal
  - How to wire everything together: prompt + LLM + memory + loop
  - How to handle a session with a real back-and-forth conversation

This is the student task demo — they should build something like this
for their capstone project.

Run:
    python 04_interactive_chatbot.py

Type 'quit' or 'exit' to end the session.
Type 'history' to see the full conversation so far.
Type 'clear' to start a new session.
"""

import uuid
from env_loader import load_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_env()

# ── Build the chain ───────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an IT support assistant for Acme Corp, a 500-person company.

Your role:
- Help employees resolve technical issues quickly and clearly
- If you can resolve the issue, provide step-by-step instructions
- If the issue needs escalation, say so and ask them to raise a ticket
- Always be professional, friendly, and concise

You can help with:
- WiFi and network connectivity
- VPN setup and errors
- Password resets
- Laptop and hardware issues
- Software installation
- Common Windows/Mac error codes

If you're unsure, say so honestly and ask a clarifying question."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# ── Memory store ─────────────────────────────────────────────────────────────
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)


# ── Helper: print conversation history ───────────────────────────────────────
def print_history(session_id: str):
    if session_id not in store or not store[session_id].messages:
        print("  (no history yet)")
        return
    print("\n── Conversation History ──────────────────────────────")
    for msg in store[session_id].messages:
        label = "🧑 You" if msg.__class__.__name__ == "HumanMessage" else "🤖 Bot"
        print(f"  {label}: {msg.content}")
    print("─────────────────────────────────────────────────────\n")


# ── Main chat loop ────────────────────────────────────────────────────────────
def main():
    session_id = str(uuid.uuid4())[:8]  # short random session ID

    print("\n" + "=" * 60)
    print("  🖥️  Acme Corp IT Support Chatbot")
    print("=" * 60)
    print(f"  Session ID: {session_id}")
    print("  Commands: 'history' | 'clear' | 'quit'")
    print("=" * 60 + "\n")

    config = {"configurable": {"session_id": session_id}}

    while True:
        try:
            user_input = input("🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("\nSession ended. Goodbye!")
            break

        if user_input.lower() == "history":
            print_history(session_id)
            continue

        if user_input.lower() == "clear":
            session_id = str(uuid.uuid4())[:8]
            config = {"configurable": {"session_id": session_id}}
            print(f"\n✅ New session started: {session_id}\n")
            continue

        # ── Send to LLM ──────────────────────────────────────────────────────
        print("🤖 Bot: ", end="", flush=True)
        try:
            response = chain_with_memory.invoke(
                {"question": user_input},
                config=config
            )
            print(response)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Check your OPENAI_API_KEY in .env\n")

        print()


if __name__ == "__main__":
    main()
