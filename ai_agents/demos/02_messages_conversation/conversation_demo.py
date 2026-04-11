import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

print("💬 Building Conversations with LLM")
print("=" * 50)

# Step 1: Create a conversation
messages = [
    HumanMessage(content="There are 600+ CRR related regulations"),
    AIMessage(content="Thanks for the information, that is great to know, would you like me to elaborate on any of these"),
    HumanMessage(content="Give me details of 1 regulation which applies to TechBank International")
]

print("📋 Conversation History:")
for i, msg in enumerate(messages, 1):
    print(f"{i}. {type(msg).__name__}: {msg.content}")
print()

# Step 2: Send the conversation to the model
print("🤖 AI Response:")
result = model.invoke(messages)
print(result.content)
print()

# Step 3: Add the AI response to the conversation
messages.append(result)
print("📋 Updated Conversation History:")
for i, msg in enumerate(messages, 1):
    print(f"{i}. {type(msg).__name__}: {msg.content}")
