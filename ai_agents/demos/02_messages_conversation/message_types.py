from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

print("📝 Understanding Message Types")
print("=" * 50)

# 1. HumanMessage - Messages from the user
user_msg = HumanMessage(content="Hello, how are you?")
print("1. HumanMessage:")
print(f"   Content: {user_msg.content}")
print(f"   Type: {type(user_msg).__name__}")
print()

# 2. AIMessage - Responses from the AI
ai_msg = AIMessage(content="I'm doing well, thank you!")
print("2. AIMessage:")
print(f"   Content: {ai_msg.content}")
print(f"   Type: {type(ai_msg).__name__}")
print()

# 3. SystemMessage - Instructions for the AI
system_msg = SystemMessage(content="You are a helpful assistant.")
print("3. SystemMessage:")
print(f"   Content: {system_msg.content}")
print(f"   Type: {type(system_msg).__name__}")
print()

# 4. ToolMessage - Results from tool executions
tool_msg = ToolMessage(content="24", tool_call_id="123")
print("4. ToolMessage:")
print(f"   Content: {tool_msg.content}")
print(f"   Tool Call ID: {tool_msg.tool_call_id}")
print(f"   Type: {type(tool_msg).__name__}")
print()

# 5. Building a conversation
print("5. Building a Conversation:")
conversation = [
    HumanMessage(content="There are 600+ CRR related regulations"),
    AIMessage(content="Thanks for the information, that is great to know, would you like me to elaborate on any of these"),
    HumanMessage(content="Give me details of 1 regulation which applies to TechBank International")
]

for i, msg in enumerate(conversation, 1):
    print(f"   Message {i}: {type(msg).__name__} - {msg.content}")