"""
DEMO 2: Memory — Making the Chatbot Remember
=============================================
What students learn:
  - Why LLMs are stateless (they don't remember anything by default)
  - How memory works: we manually pass conversation history back each time
  - Three memory types: Buffer, Window, Summary
  - How to use RunnableWithMessageHistory

Run:
    python 02_memory_conversations.py
"""

from env_loader import load_env
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_env()


# ─────────────────────────────────────────────────────────────────────────────
# PART A: Show the problem first — no memory
# ─────────────────────────────────────────────────────────────────────────────
def demo_no_memory():
    print("=" * 60)
    print("PART A: Without Memory (stateless)")
    print("The LLM forgets everything between calls.")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an IT support assistant for Acme Corp."),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()

    print("\n🧑 User: My name is James and my VPN keeps dropping.")
    r1 = chain.invoke({"question": "My name is James and my VPN keeps dropping."})
    print(f"🤖 Bot:  {r1}")

    print("\n🧑 User: What was my name again?")
    r2 = chain.invoke({"question": "What was my name again?"})
    print(f"🤖 Bot:  {r2}")
    print("\n⚠️  The bot forgot! It has no memory between calls.\n")


# ─────────────────────────────────────────────────────────────────────────────
# PART B: Buffer Memory — remembers everything
# ─────────────────────────────────────────────────────────────────────────────
def demo_buffer_memory():
    print("=" * 60)
    print("PART B: Buffer Memory (remembers full conversation)")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # MessagesPlaceholder is where conversation history gets injected
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an IT support assistant for Acme Corp."),
        MessagesPlaceholder(variable_name="chat_history"),  # ← history goes here
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    # Store session histories in a dict: session_id → InMemoryChatMessageHistory
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

    config = {"configurable": {"session_id": "acme-session-001"}}

    conversation = [
        "Hi, my name is James. My VPN keeps disconnecting every 20 minutes.",
        "I'm on Windows 11, using Cisco AnyConnect.",
        "What was the first issue I mentioned?",
        "And what's my name?",
    ]

    for message in conversation:
        print(f"\n🧑 User: {message}")
        response = chain_with_memory.invoke({"question": message}, config=config)
        print(f"🤖 Bot:  {response}")

    # ── TEACHING MOMENT: Show what's in memory ───────────────────────────────
    print("\n" + "=" * 60)
    print("WHAT'S STORED IN MEMORY (the full history):")
    print("=" * 60)
    history = store["acme-session-001"]
    for msg in history.messages:
        label = "🧑 Human" if msg.__class__.__name__ == "HumanMessage" else "🤖 AI"
        print(f"{label}: {msg.content[:80]}{'...' if len(msg.content) > 80 else ''}")


# ─────────────────────────────────────────────────────────────────────────────
# PART C: Window Memory — only remembers last N turns
# ─────────────────────────────────────────────────────────────────────────────
def demo_window_memory():
    print("\n" + "=" * 60)
    print("PART C: Window Memory (remembers last 2 turns only)")
    print("Good for production — limits token usage & cost.")
    print("=" * 60)

    from langchain_core.chat_history import InMemoryChatMessageHistory

    # Store window size by id (InMemoryChatMessageHistory is Pydantic - no extra attrs)
    _window_sizes: dict[int, int] = {}

    class WindowChatHistory(InMemoryChatMessageHistory):
        """Subclass that only keeps the last `window` message pairs."""

        def __init__(self, window: int = 2):
            super().__init__()
            _window_sizes[id(self)] = window

        def add_message(self, message):
            super().add_message(message)
            window = _window_sizes.get(id(self), 2)
            max_messages = window * 2
            if len(self.messages) > max_messages:
                self.messages = self.messages[-max_messages:]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an IT support assistant for Acme Corp."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()

    store = {}

    def get_window_history(session_id: str) -> WindowChatHistory:
        if session_id not in store:
            store[session_id] = WindowChatHistory(window=2)
        return store[session_id]

    chain_with_window = RunnableWithMessageHistory(
        chain,
        get_window_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    config = {"configurable": {"session_id": "window-session-001"}}

    questions = [
        "My name is Sarah. My laptop won't boot.",
        "I've already tried holding the power button.",
        "Should I try a hard reset?",
        "What was the very first thing I told you?",   # ← should forget 'Sarah'
    ]

    for q in questions:
        print(f"\n🧑 User: {q}")
        r = chain_with_window.invoke({"question": q}, config=config)
        print(f"🤖 Bot:  {r}")
        msgs_in_memory = len(store["window-session-001"].messages)
        print(f"   [Messages currently in memory: {msgs_in_memory}]")


# ─────────────────────────────────────────────────────────────────────────────
# Run all demos
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo_no_memory()
    demo_buffer_memory()
    demo_window_memory()
