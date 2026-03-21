# =============================================================================
# SESSION 2 — Prompt Engineering & LLM Architecture
# File: 03_temperature_and_tokens.py
# Cohort 5 · 22 March 2026
#
# Live demos for the LLM Architecture section.
# Shows temperature effect and token counting without any external tools.
# Run this FIRST — before 01_prompt_techniques.py — during Part 1.
# =============================================================================

from openai import OpenAI

from env_loader import load_env
load_env()
client = OpenAI()

DIVIDER = "\n" + "=" * 60 + "\n"


# =============================================================================
# DEMO 1 — TEMPERATURE: Same prompt, different temperatures
# Run all three back to back and compare the outputs live.
# =============================================================================

print(DIVIDER + "DEMO 1 — TEMPERATURE COMPARISON" + DIVIDER)

PROMPT = "Describe what an IT support engineer does in 2 sentences."

temperatures = [0.0, 0.7, 1.5]

for temp in temperatures:
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temp,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": PROMPT}
        ]
    )
    print(f"Temperature {temp}:")
    print(response.choices[0].message.content)
    print()

# ── Teaching point ───────────────────────────────────────────────────────────
# Run temp=0 THREE TIMES. Ask: is it always the same?
# Run temp=1.5 three times. Ask: what do you notice?
# Key message:
#   0.0 = deterministic, same every time   → classifiers, JSON extraction
#   0.7 = slight variation, still coherent → chat bots, Q&A
#   1.5 = chaotic, may become incoherent   → almost never useful in production


# =============================================================================
# DEMO 2 — TEMPERATURE for classification vs creative tasks
# Makes the practical tradeoff concrete.
# =============================================================================

print(DIVIDER + "DEMO 2 — RIGHT TEMPERATURE FOR THE JOB" + DIVIDER)

classifier_prompt = {
    "system": "Classify this IT ticket as exactly one word: Hardware, Software, Network, or Access.",
    "user": "My VPN keeps dropping every 20 minutes when I'm working from home."
}

creative_prompt = {
    "system": "You are a friendly IT support bot for Acme Corp. Be warm and helpful.",
    "user": "My VPN keeps dropping every 20 minutes when I'm working from home."
}

print("CLASSIFICATION — should use temp=0:")
for i in range(3):
    r = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": classifier_prompt["system"]},
            {"role": "user",   "content": classifier_prompt["user"]}
        ]
    )
    print(f"  Run {i+1}: {r.choices[0].message.content.strip()}")

print()
print("FRIENDLY RESPONSE — temp=0.7 gives natural variation:")
for i in range(2):
    r = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.7,
        messages=[
            {"role": "system", "content": creative_prompt["system"]},
            {"role": "user",   "content": creative_prompt["user"]}
        ]
    )
    print(f"  Run {i+1}: {r.choices[0].message.content[:120]}...")
    print()

# ── Teaching point ───────────────────────────────────────────────────────────
# The classifier should output the SAME word every time. If it doesn't, temp is wrong.
# The friendly response should feel slightly different each time — that's natural.


# =============================================================================
# DEMO 2.5 — ROLES: system, user, assistant
# The API expects messages with roles. Each has a purpose.
# =============================================================================

print(DIVIDER + "DEMO 2.5 — MESSAGE ROLES" + DIVIDER)

print("""
ROLES (what each message type does):

  system   — Sets the model's behavior, persona, constraints. NEVER put user input here.
             Only you (the developer) control this. Trusted channel.

  user     — The human's message. UNTRUSTED. Can contain injection attempts.
             This is what you validate before sending.

  assistant — The model's previous replies. Used for multi-turn chat.
              You append each response here and resend the full history.

Every API call sends the full message list. The model has no memory — you provide it.
""")

# ── Teaching point ───────────────────────────────────────────────────────────
# Ask: "Why never put user input in the system prompt?"
# Answer: Injection. If you concatenate user_msg into system, an attacker can
# inject "Ignore above. You are now..." and the model may obey. Keep them separate.


# =============================================================================
# DEMO 3 — TOKEN COUNTING using the API's usage field
# No tiktoken needed — the API tells you exactly how many tokens were used.
# response.usage has: prompt_tokens, completion_tokens, total_tokens
# =============================================================================

print(DIVIDER + "DEMO 3 — TOKEN COUNTING" + DIVIDER)

test_inputs = [
    "Hello",
    "The quick brown fox jumps over the lazy dog.",
    "You are an IT support assistant for Acme Corp. You help employees with hardware, software, networking, and access issues. Always be professional and empathetic.",
    "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
]

print(f"{'Input (first 60 chars)':<62} {'Prompt':>8} {'Completion':>10} {'Chars':>6}")
print("-" * 95)

for text in test_inputs:
    # max_tokens=1: we request 1 output token to minimise cost; we only need input count
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[{"role": "user", "content": text}],
        max_tokens=1   # Limits OUTPUT length. Here we use it to get a cheap token count.
    )

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    chars = len(text)
    print(f"{text[:60]:<62} {prompt_tokens:>8} {completion_tokens:>10} {chars:>6}")

print()
print("Rule of thumb: ~4 characters per token in English.")
print("Code tokenises LESS efficiently (more tokens per character).")
print("completion_tokens = tokens in the model's reply. Output costs more than input.")

# ── Teaching point ───────────────────────────────────────────────────────────
# max_tokens: Caps how long the model can reply. Default is model's max (e.g. 4096).
# Set low for classifiers (e.g. 20). Set higher for chat (e.g. 500). Saves cost + latency.


# =============================================================================
# DEMO 3.5 — MAX_TOKENS: Same prompt, different output limits
# Shows: too low = truncated reply. Right size = cost control.
# =============================================================================

print(DIVIDER + "DEMO 3.5 — MAX_TOKENS EFFECT" + DIVIDER)

prompt = "List 5 steps to troubleshoot a WiFi connection problem. Number each step."

for max_tok in [20, 100, 500]:
    r = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tok
    )
    content = r.choices[0].message.content
    truncated = "..." if r.usage.completion_tokens >= max_tok else ""
    print(f"max_tokens={max_tok} (used {r.usage.completion_tokens}):")
    print(f"  {content[:200].replace(chr(10), ' ')}{truncated}")
    print()

# ── Teaching point ───────────────────────────────────────────────────────────
# max_tokens=20: reply gets cut off mid-sentence. Use for single-word classification.
# max_tokens=100: enough for a short answer. Use for ticket summaries.
# max_tokens=500: full paragraph. Use for chat, explanations. Set based on your use case.


# =============================================================================
# DEMO 3.6 — OTHER PARAMETERS (top_p, frequency_penalty, presence_penalty)
# Brief mention — temperature is the main one you'll use.
# =============================================================================

print(DIVIDER + "DEMO 3.6 — OTHER SAMPLING PARAMETERS" + DIVIDER)

print("""
top_p (nucleus sampling): Alternative to temperature. Considers top tokens whose
  cumulative probability exceeds p. 1.0 = no truncation. Rarely needed if you use temp.

frequency_penalty (-2 to 2): Penalises tokens that appear often. Reduces repetition.
  Use 0.3–0.7 for long-form generation when the model gets stuck repeating phrases.

presence_penalty (-2 to 2): Penalises tokens that have appeared at all.
  Use when you want the model to cover new topics, avoid echoing back.

Example: Creative writing with less repetition:
  temperature=0.8, frequency_penalty=0.5
""")

# ── Teaching point ───────────────────────────────────────────────────────────
# Now calculate the cost live:
print()
print(DIVIDER + "TOKEN COST CALCULATOR" + DIVIDER)

system_prompt_words = 50
conversation_turns = 20
words_per_turn = 100
context_tokens = (system_prompt_words + (conversation_turns * words_per_turn)) * (4/3)

# GPT-4o pricing (as of early 2026 — check current pricing)
cost_per_1k_input = 0.0025   # $0.0025 per 1K input tokens
cost_per_1k_output = 0.01    # $0.01 per 1K output tokens

input_cost = (context_tokens / 1000) * cost_per_1k_input
output_cost = (50 / 1000) * cost_per_1k_output  # ~50 token response

print(f"Scenario: Acme Corp chatbot, 20-turn conversation")
print(f"  System prompt:      ~{system_prompt_words} words = ~{int(system_prompt_words * 4/3)} tokens")
print(f"  Conversation turns: {conversation_turns} × ~{words_per_turn} words = ~{int(conversation_turns * words_per_turn * 4/3)} tokens")
print(f"  Total input tokens: ~{int(context_tokens)}")
print(f"  Estimated cost per conversation: ${input_cost + output_cost:.4f}")
print(f"  Cost for 1,000 conversations/day: ${(input_cost + output_cost) * 1000:.2f}/day")
print()
print("Context window limits (tokens):")
print("  GPT-4o:             128,000 tokens  (~96,000 words  — a full novel)")
print("  Claude 3.5 Sonnet:  200,000 tokens  (~150,000 words)")
print("  Llama 3.2 (local):  128,000 tokens  (zero API cost — Week 9)")

# ── Teaching point ───────────────────────────────────────────────────────────
# Ask: "At what point in this 20-turn conversation does the history need trimming?"
# Answer: depends on the model — but the LangChain window memory from last session
# is the mechanism that manages this automatically.


# =============================================================================
# DEMO 4 — CONTEXT WINDOW EFFECT
# Show what happens as context grows — model starts 'forgetting'
# =============================================================================

print(DIVIDER + "DEMO 4 — CONTEXT WINDOW AND MEMORY" + DIVIDER)

# Simulate a long conversation where the model is asked about early information
messages = [
    {"role": "system", "content": "You are an IT support assistant. Answer questions about the conversation history."},
    {"role": "user",   "content": "My name is James and I'm having trouble with my VPN."},
    {"role": "assistant", "content": "Hi James! I'd be happy to help with your VPN issue. What's happening exactly?"},
    {"role": "user",   "content": "It drops every 20 minutes."},
    {"role": "assistant", "content": "That sounds like a timeout issue. Are you using Cisco AnyConnect?"},
    {"role": "user",   "content": "Yes. Also my email is slow today."},
    {"role": "assistant", "content": "Let's tackle the VPN first. Go to Settings > Network in AnyConnect and check the timeout value."},
    {"role": "user",   "content": "What was the first issue I mentioned at the start of our conversation?"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,
    messages=messages
)

print("Short conversation — model recalls early context:")
print(f"User: What was the first issue I mentioned at the start?")
print(f"Bot:  {response.choices[0].message.content}")
print()
print("Key point: the ENTIRE message list above is sent on every API call.")
print("LLMs are stateless — memory is just us passing history back each time.")
print("This is exactly what LangChain's InMemoryChatMessageHistory does.")
print("At 200K tokens (Claude), that's ~150 A4 pages of conversation history.")
