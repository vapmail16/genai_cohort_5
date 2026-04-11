# 🎓 LangGraph Complete Training Guide

---

## 📚 Table of Contents

1. [**Introduction & Setup**](#1-introduction--setup)
2. [**Core Concepts**](#2-core-concepts)

3. [**Building Your First Graph**](#3-building-your-first-graph)
4. message conversations
5. [**Tool Calling**](#5-tool-calling)
6. [**State Management**](#6-state-management)
7. [**Complete Agents**](#7-complete-agents)

8. [**ReACT Pattern**](#8-react-pattern)

9. [**Memory & Persistence**](#9-memory--persistence)

10. [**Real-World Project**](#10-real-world-project)
11. [**Advanced Topics**](#11-advanced-topics)

---

## 1. Introduction & Setup

### What is LangGraph? 🤔
**Simple Explanation:** Think of LangGraph as a recipe book for AI agents. Just like a recipe has steps (chop onions → heat oil → add ingredients), LangGraph lets you create AI workflows with clear steps that can make decisions and use tools.

**Technical Definition:** LangGraph is a framework for building stateful, multi-step applications with Large Language Models (LLMs).

### Why Use LangGraph? 🎯
- **Decision Making:** Your AI can choose different paths based on what it learns
- **Tool Usage:** Your AI can perform actions (calculations, API calls, etc.)
- **Memory:** Your AI remembers previous conversations
- **Complex Reasoning:** Handle multi-step problems that require thinking and acting

### Prerequisites ✅
- Basic Python knowledge
- OpenAI API key
- Understanding of AI/LLM concepts

### Environment Setup 🛠️


#### Step 1: Create Virtual Environment
```bash

# Create a folder for this lab (any path/name you like), then enter it
mkdir -p ~/langgraph_lab && cd ~/langgraph_lab

# Create virtual environment
python3 -m venv venv 

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Step 2: Install Dependencies

touch requirements.txt

langchain-core
langgraph
langgraph-checkpoint
langgraph-prebuilt
jupyter
ipykernel
langchain-openai
pandas
pydantic
pydantic_core
python-dotenv



Install packages:

pip3 install -r requirements.txt

#### Step 3: OpenAI Configuration

touch .env 

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

#### Step 4: Test Setup

touch test_setup.py

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Please make sure your .env file contains: OPENAI_API_KEY=your_actual_api_key_here")
    exit(1)

# Initialize model
model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Test connection
print("Testing OpenAI connection...")
msg = HumanMessage(content="Hi, how are you?")
response = model.invoke([msg])
print("Response:", response.content)
print("✅ Setup successful!")

```
python3 test_setup.py

**Expected Output:**
```
Testing OpenAI connection...
Response: Hello! I'm just a computer program, so I don't have feelings, but I'm here and ready to help you. How can I assist you today?
✅ Setup successful!

```

---

# Create subdirectories for different demos
mkdir -p demos/01_basic_graph
mkdir -p demos/02_messages_conversation
mkdir -p demos/03_tool_calling
mkdir -p demos/04_react_pattern
mkdir -p demos/05_memory_persistence
mkdir -p demos/06_real_world_project



## 2. Core Concepts

### Understanding Graphs 📊

**Simple Explanation:** A graph is like a flowchart where:
- **Boxes (Nodes)** = Functions that do something
- **Arrows (Edges)** = Show what happens next
- **Data (State)** = Information that flows through the boxes

**Visual Representation:**
```
Input Data → [Process A] → [Decision Point] → [Process B] or [Process C] → Output
```

### Key Components 🧩

#### 1. State
**What it is:** The data that flows through your workflow
**Simple Example:** Like a shopping cart that gets filled as you go through a store


#### 2. Nodes
**What they are:** Functions that process and modify the state
**Simple Example:** Like workers in a factory assembly line

#### 3. Edges
**What they are:** Connections that determine the flow between nodes
**Simple Example:** Like road signs that tell you which way to go

---

## 3. Building Your First Graph

### Project: Activity Selector 🎯

**Goal:** Build a simple AI that decides what activity someone will do based on a random "mood".


cd demos/01_basic_graph
touch activity_selector.py

****

import random
from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END

# Step 1: Define the State
class State(TypedDict):
    graph_state: str

# Step 2: Create the Nodes (functions that do work)
def node_1(state):
    print("Node 1 working...")
    return {"graph_state": state["graph_state"] + " will"}

def node_2(state):
    print("Node 2 working...")
    return {"graph_state": state["graph_state"] + " go surfing"}

def node_3(state):
    print("Node 3 working...")
    return {"graph_state": state["graph_state"] + " go rock climbing"}

# Step 3: Create Decision Logic
def decide_mood_node(state) -> Literal["node_2", "node_3"]:
    # Randomly choose between surfing or rock climbing
    if random.random() < 0.5:
        return "node_2"
        return "node_3"

# Step 4: Build the Graph
def create_activity_graph():
    # Create the graph builder
    builder = StateGraph(State)
    
    # Add nodes
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)
    
    # Add edges (connections)
    builder.add_edge(START, "node_1")  # Always start with node_1
    builder.add_conditional_edges("node_1", decide_mood_node)  # node_1 decides what's next
    builder.add_edge("node_2", END)    # node_2 goes to end
    builder.add_edge("node_3", END)    # node_3 goes to end
    
    # Compile the graph
    return builder.compile()


# Step 5: Test the Graph
if __name__ == "__main__":
    print("🎯 Building Activity Selector Graph...")
    
    # Create the graph
    graph = create_activity_graph()
    
    # Test it multiple times
    for i in range(3):
        print(f"\n--- Test {i+1} ---")
        result = graph.invoke({"graph_state": "Vikkas"})
        print(f"Result: {result['graph_state']}")
****

python3 activity_selector.py




touch visualize_graph.py

****

from activity_selector import create_activity_graph
from IPython.display import Image, display

# Create the graph
graph = create_activity_graph()

# Display the graph structure
print("📊 Graph Structure:")
print(graph.get_graph().draw_mermaid())

# If you want to see it as an image (requires additional setup)
# display(Image(graph.get_graph().draw_mermaid_png()))

****

python3 visualize_graph.py   

START → node_1 → [Decision] → node_2 OR node_3 → END


## 4. Messages & Conversations

### Understanding Messages 💬

**Simple Explanation:** Messages are like text messages between you and the AI. They keep track of the conversation history so the AI remembers what you talked about.

### Message Types 📝

#### 1. HumanMessage
Messages from the user

#### 2. AIMessage
Responses from the AI

#### 3. SystemMessage
Instructions for the AI

#### 4. ToolMessage
**What it is:** Results from tool executions


### Building Conversations 🔄

Understanding Different Types of Messages

What it does: This is like learning about different types of text messages in a chat app.

Simple explanation:
HumanMessage: Messages YOU send (like "Hello, how are you?")
AIMessage: Messages the AI sends back (like "I'm doing well, thank you!")
SystemMessage: Instructions for the AI (like "You are a helpful assistant")
ToolMessage: Results from when the AI uses tools (like "The answer is 24")

Real-world analogy: It's like understanding the difference between:
Your text messages
Your friend's replies
Instructions you give to someone
Results from a calculator


cd .. 
cd 02_messages_conversation
touch message_types.py


****

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

python3 message_types.py



****

Create the Conversation Demo

What it does: This shows how to have a back-and-forth conversation with the AI, like texting.

Simple explanation:
You send a message: "There are 600+ CRR related regulations"
AI replies: "Thanks for the information, that is great to know..."
You ask follow-up: "Give me details of 1 regulation..."
AI gives a detailed answer about banking regulations

Real-world analogy: It's like having a conversation with a banking expert where:
You mention something about regulations
They acknowledge it
You ask for specific details
They give you a detailed explanation





touch conversation_demo.py

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


python3 conversation_demo.py

Understanding Message Flow in LangGraph

What it does: This shows how LangGraph processes conversations step by step.

Simple explanation:
You send a message to the AI
LangGraph takes that message and processes it
The AI sees the full conversation history
The AI responds
LangGraph adds the response to the conversation

Real-world analogy: It's like having a smart assistant that:
Listens to everything you say
Remembers the whole conversation
Gives you thoughtful responses
Keeps track of what you've discussed



touch message_flow_demo.py


import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, add_messages

# Load environment variables
load_dotenv()

# Step 1: Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Step 2: Create the LLM Node
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

def llm_node(state: MessagesState):
    """This node processes messages and returns AI response"""
    print("🤖 LLM Node: Processing messages...")
    
    # Get the last message to understand what the user wants
    last_message = state["messages"][-1]
    print(f"   Last message: {last_message.content}")
    
    # Send all messages to the LLM (it sees the full conversation)
    response = model.invoke(state["messages"])
    print(f"   AI Response: {response.content}")
    
    # Return the AI response as a new message
    return {"messages": [response]}

# Step 3: Build the Graph
def create_conversation_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("llm", llm_node)
    builder.add_edge(START, "llm")
    builder.add_edge("llm", END)
    return builder.compile()

# Step 4: Test the Conversation Flow
if __name__ == "__main__":
    print("🔄 Message Flow in LangGraph")
    print("=" * 50)
    
    # Create the graph
    graph = create_conversation_graph()
    
    # Test 1: First message
    print("\n--- Test 1: First Message ---")
    messages = [HumanMessage(content="Hi, I'm Vikkas. What's your name?")]
    result = graph.invoke({"messages": messages})
    
    print(f"Messages in state: {len(result['messages'])}")
    for i, msg in enumerate(result['messages'], 1):
        print(f"{i}. {type(msg).__name__}: {msg.content}")
    
    # Test 2: Follow-up message (simulating a conversation)
    print("\n--- Test 2: Follow-up Message ---")
    messages = [
        HumanMessage(content="Hi, I'm Vikkas. What's your name?"),
        AIMessage(content="Hello Vikkas! I'm an AI assistant. How can I help you today?"),
        HumanMessage(content="Can you help me understand LangGraph?")
    ]
    
    result = graph.invoke({"messages": messages})
    
    print(f"Messages in state: {len(result['messages'])}")
    for i, msg in enumerate(result['messages'], 1):
        print(f"{i}. {type(msg).__name__}: {msg.content}")

python3 message_flow_demo.py


**********


Understanding the add_messages Reducer

What it does: This explains a technical problem and solution with message handling.

Simple explanation:
Problem: Without special handling, new messages would replace old ones
Solution: Use add_messages to combine old and new messages
Result: The AI can see the full conversation history

Real-world analogy: It's like:
Bad way: Every time you send a new text, it deletes all previous texts
Good way: New texts get added to the conversation, so you can see the full history

touch reducer_demo.py

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import add_messages

print("🧩 Understanding the add_messages Reducer")
print("=" * 50)

# Step 1: Show the problem without add_messages
print("❌ Problem: Without add_messages, messages get replaced")
print()

# Simulate what happens without add_messages
old_messages = [
    HumanMessage(content="Hi how are you"),
    AIMessage(content="I am good, thank you")
]

new_message = [HumanMessage(content="What is the role of PRA in banking")]

# This would REPLACE the old messages (BAD!)
print("Old messages:")
for i, msg in enumerate(old_messages, 1):
    print(f"  {i}. {msg.content}")

print(f"\nNew message: {new_message[0].content}")

# Step 2: Show the solution with add_messages
print("\n✅ Solution: With add_messages, messages accumulate")
print()

# This COMBINES the old and new messages (GOOD!)
combined = add_messages(old_messages, new_message)

print("Combined messages:")
for i, msg in enumerate(combined, 1):
    print(f"  {i}. {msg.content}")

print(f"\nTotal messages: {len(combined)}")
print("The AI can see the full conversation history!")


python3 reducer_demo.py


Complete Conversation Example

What it does: This simulates a complete conversation with multiple back-and-forth exchanges.

Simple explanation:
You introduce yourself: "Hi, I'm Vikkas. I work in banking."
You ask for help: "I need help understanding CRR regulations."
You ask for specifics: "Can you explain what CRR Article 92 means?"
You ask for application: "How does this apply to TechBank International?"

Real-world analogy: It's like having a consultation with a banking expert where:
You introduce yourself and your background
You explain what you need help with
You ask for specific information
You ask how it applies to your specific situation
The expert remembers everything and gives you relevant answers


touch complete_conversation.py

import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

def conversation_node(state: MessagesState):
    """Process conversation and return AI response"""
    print("💬 Processing conversation...")
    
    # The AI sees the full conversation history
    response = model.invoke(state["messages"])
    
    # Return the AI response
    return {"messages": [response]}

def create_conversation_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("conversation", conversation_node)
    builder.add_edge(START, "conversation")
    builder.add_edge("conversation", END)
    return builder.compile()

if __name__ == "__main__":
    print("🎯 Complete Conversation Demo")
    print("=" * 50)
    
    # Create the graph
    graph = create_conversation_graph()
    
    # Simulate a multi-turn conversation
    conversation_turns = [
        "Hi, I'm Vikkas. I work in banking.",
        "I need help understanding CRR regulations.",
        "Can you explain what CRR Article 92 means?",
        "How does this apply to TechBank International specifically?"
    ]
    
    # Start with system message
    messages = [SystemMessage(content="You are a helpful banking regulation expert.")]
    
    for i, user_input in enumerate(conversation_turns, 1):
        print(f"\n--- Turn {i} ---")
        print(f"User: {user_input}")
        
        # Add user message
        messages.append(HumanMessage(content=user_input))
        
        # Process with graph
        result = graph.invoke({"messages": messages})
        
        # Get the AI response
        ai_response = result["messages"][-1]
        print(f"AI: {ai_response.content}")
        
        # Update messages for next turn
        messages = result["messages"]
    
    print(f"\n📊 Final conversation has {len(messages)} messages")
    print("The AI remembered the entire conversation context!")


python3 complete_conversation.py


### Understanding Message Flow 🔄

**Visual Flow:**
```
User Message → Graph → LLM → AI Response → Add to State → Continue
```

**Key Point:** Messages accumulate in the state, so the AI always has the full conversation context.

---




## 5. Tool Calling

### What are Tools? 🛠️

**Simple Explanation:** Tools are like giving your AI superpowers. Instead of just talking, it can:
- Do calculations
- Look up information
- Call APIs
- Execute functions

### How Tool Calling Works 🔧

**Process:**
1. User asks a question
2. AI decides if it needs a tool
3. AI calls the tool with parameters
4. Tool executes and returns result
5. AI uses result to answer the user

### Creating Your First Tool 🎯

**What it does:** This shows how to create a simple calculator tool that the AI can use.

**Simple explanation:**
You create a function that does math
You tell the AI about this function
The AI can then use it to answer math questions
The AI decides when it needs to use the tool

**Real-world analogy:** It's like giving a calculator to a smart assistant so they can do math for you.

cd ..
cd 03_tool_calling
touch basic_tool_demo.py

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

print("🛠️ Basic Tool Calling Demo")
print("=" * 50)

# Step 1: Define the Tool Function
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers and returns an integer
    
    Args:
        a: first integer
        b: second integer
    """
    return a * b

print("1. Tool Function Created:")
print(f"   Function: multiply(a: int, b: int) -> int")
print(f"   Docstring: {multiply.__doc__.strip()}")
print()

# Step 2: Bind Tools to Model
model_with_tools = model.bind_tools([multiply])
print("2. Model with Tools Created:")
print("   Model now knows about the multiply function")
print()

# Step 3: Test Tool Calling
print("3. Testing Tool Calling:")
print("   Question: What is 4 times 6?")
print()

result = model_with_tools.invoke([HumanMessage(content="What is 4 times 6?")])

print("AI Response:", result.content)
print("Tool Calls:", result.tool_calls)
print()

# Step 4: Inspect Tool Call Details
if result.tool_calls:
    tool_call = result.tool_calls[0]
    print("4. Tool Call Details:")
    print(f"   Function name: {tool_call['name']}")
    print(f"   Arguments: {tool_call['args']}")
    print(f"   Call ID: {tool_call['id']}")
    print()
    
    # Step 5: Execute the Tool
    print("5. Executing the Tool:")
    args = tool_call['args']
    result_value = multiply(args['a'], args['b'])
    print(f"   multiply({args['a']}, {args['b']}) = {result_value}")
else:
    print("4. No tool calls made")
```

python3 basic_tool_demo.py

**Expected Output:**
```
🛠️ Basic Tool Calling Demo
==================================================
1. Tool Function Created:
   Function: multiply(a: int, b: int) -> int
   Docstring: Multiply two numbers and returns an integer

2. Model with Tools Created:
   Model now knows about the multiply function

3. Testing Tool Calling:
   Question: What is 4 times 6?

AI Response: I'll calculate 4 times 6 for you.
Tool Calls: [{'name': 'multiply', 'args': {'a': 4, 'b': 6}, 'id': 'call_123'}]

4. Tool Call Details:
   Function name: multiply
   Arguments: {'a': 4, 'b': 6}
   Call ID: call_123

5. Executing the Tool:
   multiply(4, 6) = 24
```

### Understanding Tool Call Structure 📊

**What it does:** This shows the detailed structure of how tool calls work.

**Simple explanation:**
The AI creates a special message when it wants to use a tool
This message contains the function name, arguments, and a unique ID
You can inspect these details to understand what the AI wants to do

**Real-world analogy:** It's like the AI writing a note saying "Please use the calculator to multiply 4 and 6" with all the details.

touch tool_structure_demo.py

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

print("📊 Understanding Tool Call Structure")
print("=" * 50)

# Define multiple tools
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# Bind all tools to model
tools = [add, subtract, multiply]
model_with_tools = model.bind_tools(tools)

print("Available Tools:")
for i, tool in enumerate(tools, 1):
    print(f"  {i}. {tool.__name__}: {tool.__doc__}")
print()

# Test with different questions
test_questions = [
    "What is 10 plus 5?",
    "Calculate 20 minus 8",
    "What is 6 times 7?"
]

for i, question in enumerate(test_questions, 1):
    print(f"--- Test {i} ---")
    print(f"Question: {question}")
    
    result = model_with_tools.invoke([HumanMessage(content=question)])
    
    print(f"AI Response: {result.content}")
    
    if result.tool_calls:
        for j, tool_call in enumerate(result.tool_calls, 1):
            print(f"Tool Call {j}:")
            print(f"  Name: {tool_call['name']}")
            print(f"  Arguments: {tool_call['args']}")
            print(f"  ID: {tool_call['id']}")
            
            # Execute the tool
            func_name = tool_call['name']
            args = tool_call['args']
            
            if func_name == 'add':
                result_value = add(args['a'], args['b'])
            elif func_name == 'subtract':
                result_value = subtract(args['a'], args['b'])
            elif func_name == 'multiply':
                result_value = multiply(args['a'], args['b'])
            
            print(f"  Result: {result_value}")
    else:
        print("No tool calls made")
    
    print()
```

python3 tool_structure_demo.py

### Building a Complete Tool Agent 🤖

**What it does:** This creates a complete agent that can use tools and provide final answers.

**Simple explanation:**
You create an agent that can receive questions
The agent decides which tools to use
The agent executes the tools
The agent gives you the final answer

**Real-world analogy:** It's like having a smart assistant that can use calculators, look things up, and give you complete answers.

touch complete_tool_agent.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define tools
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Create model with tools
tools = [add, subtract, multiply, divide]
model_with_tools = model.bind_tools(tools)

def tool_calling_llm(state: MessagesState):
    """LLM node that can call tools"""
    return {"messages": model_with_tools.invoke(state["messages"])}

def create_tool_agent():
    """Create a complete tool-calling agent"""
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", END)
    
    return builder.compile()

if __name__ == "__main__":
    print("🤖 Complete Tool Agent Demo")
    print("=" * 50)
    
    # Create the agent
    agent = create_tool_agent()
    
    # Test questions
    test_questions = [
        "What is 15 plus 25?",
        "Calculate 100 minus 37",
        "What is 8 times 9?",
        "What is 50 divided by 5?",
        "Calculate 2 plus 3, then multiply by 4"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test {i} ---")
        print(f"Question: {question}")
        print()
        
        # Process with agent
        messages = [HumanMessage(content=question)]
        result = agent.invoke({"messages": messages})
        
        # Display the conversation
        for msg in result["messages"]:
            if isinstance(msg, HumanMessage):
                print(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                print(f"AI: {msg.content}")
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        print(f"  Tool Call: {tool_call['name']}({tool_call['args']})")
            elif isinstance(msg, ToolMessage):
                print(f"Tool Result: {msg.content}")
        print()
```

python3 complete_tool_agent.py

**Expected Output:**
```
🤖 Complete Tool Agent Demo
==================================================

--- Test 1 ---
Question: What is 15 plus 25?

Human: What is 15 plus 25?
AI: I'll calculate 15 plus 25 for you.
  Tool Call: add({'a': 15, 'b': 25})
Tool Result: 40
AI: The result of 15 + 25 is 40.

--- Test 2 ---
Question: Calculate 100 minus 37

Human: Calculate 100 minus 37
AI: I'll calculate 100 minus 37 for you.
  Tool Call: subtract({'a': 100, 'b': 37})
Tool Result: 63
AI: The result of 100 - 37 is 63.

--- Test 3 ---
Question: What is 8 times 9?

Human: What is 8 times 9?
AI: I'll calculate 8 times 9 for you.
  Tool Call: multiply({'a': 8, 'b': 9})
Tool Result: 72
AI: The result of 8 × 9 is 72.

--- Test 4 ---
Question: What is 50 divided by 5?

Human: What is 50 divided by 5?
AI: I'll calculate 50 divided by 5 for you.
  Tool Call: divide({'a': 50, 'b': 5})
Tool Result: 10.0
AI: The result of 50 ÷ 5 is 10.0.

--- Test 5 ---
Question: Calculate 2 plus 3, then multiply by 4

Human: Calculate 2 plus 3, then multiply by 4
AI: I'll help you calculate this step by step. First, I'll add 2 and 3, then multiply the result by 4.
  Tool Call: add({'a': 2, 'b': 3})
Tool Result: 5
AI: Now I'll multiply 5 by 4.
  Tool Call: multiply({'a': 5, 'b': 4})
Tool Result: 20
AI: The final result is 20. Here's the breakdown:
2 + 3 = 5
5 × 4 = 20
```

### Understanding the Tool Agent Flow 🔄

**What it does:** This explains how the tool agent processes requests step by step.

**Simple explanation:**
1. User asks a question
2. Agent decides if it needs tools
3. Agent calls the appropriate tool
4. Tool executes and returns result
5. Agent provides the final answer

**Real-world analogy:** It's like having a smart assistant that can use different tools (calculator, dictionary, etc.) to help you get complete answers.

touch tool_flow_explanation.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define a simple tool
def get_weather(city: str) -> str:
    """Get weather information for a city"""
    # Simulate weather data
    weather_data = {
        "london": "Sunny, 22°C",
        "paris": "Cloudy, 18°C",
        "tokyo": "Rainy, 15°C",
        "new york": "Windy, 12°C"
    }
    return weather_data.get(city.lower(), "Weather data not available")

# Create model with tools
tools = [get_weather]
model_with_tools = model.bind_tools(tools)

def tool_calling_llm(state: MessagesState):
    """LLM node that can call tools"""
    print("🤖 LLM Processing: Analyzing user request...")
    return {"messages": model_with_tools.invoke(state["messages"])}

def create_flow_demo_agent():
    """Create agent to demonstrate the flow"""
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", END)
    
    return builder.compile()

if __name__ == "__main__":
    print("🔄 Tool Agent Flow Explanation")
    print("=" * 50)
    
    # Create the agent
    agent = create_flow_demo_agent()
    
    print("Flow Steps:")
    print("1. User asks a question")
    print("2. Agent analyzes the question")
    print("3. Agent decides if tools are needed")
    print("4. If yes: Agent calls the tool")
    print("5. Tool executes and returns result")
    print("6. Agent provides final answer")
    print()
    
    # Test with a question that needs a tool
    print("--- Example: Weather Question ---")
    messages = [HumanMessage(content="What's the weather like in London?")]
    result = agent.invoke({"messages": messages})
    
    print("\nConversation Flow:")
    for i, msg in enumerate(result["messages"], 1):
        if isinstance(msg, HumanMessage):
            print(f"{i}. Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"{i}. AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   → Tool Call: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})")
        else:
            print(f"{i}. Tool Result: {msg.content}")
    
    print("\n--- Example: Non-Tool Question ---")
    messages = [HumanMessage(content="Hello, how are you?")]
    result = agent.invoke({"messages": messages})
    
    print("\nConversation Flow:")
    for i, msg in enumerate(result["messages"], 1):
        if isinstance(msg, HumanMessage):
            print(f"{i}. Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"{i}. AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"   → Tool Call: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})")
        else:
            print(f"{i}. Tool Result: {msg.content}")
```

python3 tool_flow_explanation.py

---

## 6. State Management

Covered above 

## 7. Complete Agents

Covered above

## 8. ReACT Pattern

### What is ReACT? 🔄

**Simple Explanation:** ReACT (Reason + Act) is like having a smart assistant that:
1. **Reasons** about what to do
2. **Acts** by calling a tool
3. **Observes** the result
4. **Repeats** until the task is complete

**Key Difference:** Unlike basic tool calling, ReACT creates a loop where the assistant can see tool results and decide to call more tools.

**Real-world analogy:** It's like having a smart assistant that doesn't just use a calculator once, but can see the result, think about what to do next, and keep using tools until the problem is fully solved.

### ReACT Flow Diagram 📊

```
User Query → Assistant LLM Reasoning
   │
   ▼
Need Tools?
   │
  Yes ──► Execute Tools ──► Observe Result ──► Loop ──► Final Answer
   │
   └──► No ──► Final Answer
```

### Building a ReACT Agent 🛠️

**What it does:** This creates an agent that can reason, act, observe, and repeat until a problem is solved.

**Simple explanation:**
You create an agent with multiple tools
The agent looks at a complex problem
The agent reasons about what to do first
The agent uses a tool and sees the result
The agent repeats until the problem is solved

**Real-world analogy:** It's like a smart assistant that can break down complex math problems into steps and solve them one by one.

cd ..
cd 04_react_pattern
touch react_agent_demo.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

print("🔄 Building ReACT Agent Demo")
print("=" * 50)

# Define multiple arithmetic tools
def addition(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

def subtraction(a: int, b: int) -> int:
    """Subtracts two numbers"""
    return a - b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def division(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

# Create model with all tools
tools = [addition, subtraction, multiplication, division]
model_with_tools = model.bind_tools(tools)

# System message for the assistant
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state: MessagesState):
    """Assistant node that reasons and acts"""
    return {"messages": model_with_tools.invoke([sys_msg] + state["messages"])}

def create_react_agent():
    """Create a ReACT agent with looping capability"""
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges with LOOP back to assistant (key difference!)
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")  # Loop back (key difference!)
    
    return builder.compile()

if __name__ == "__main__":
    print("Creating ReACT agent...")
    react_graph = create_react_agent()
    
    print("\nReACT Agent Structure:")
    print("- START → assistant")
    print("- assistant → tools_condition")
    print("- tools_condition: YES → tools")
    print("- tools_condition: NO → END")
    print("- tools → assistant (LOOP!)")
    print()
    
    # Test with a complex multi-step problem
    print("=" * 50)
    print("Test: Complex multi-step calculation")
    print("=" * 50)
    
    messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]
    result = react_graph.invoke({"messages": messages})
    
    print("\nConversation Flow:")
    for i, msg in enumerate(result["messages"], 1):
        if isinstance(msg, HumanMessage):
            print(f"\n{i}. Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"\n{i}. AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    print(f"   Tool Call: {tool_call['name']}({tool_call['args']})")
        else:
            print(f"\n{i}. Tool Result: {msg.content}")
    
    print("\n" + "=" * 50)
    print("Key Point: The agent looped back multiple times!")
    print("Unlike basic tool calling, ReACT creates a reasoning loop.")
    print("=" * 50)
```

**Explanation:**

**Lines 1-8:** Import the required packages.
- `StateGraph` for the graph structure.
- `ToolNode`, `tools_condition` for tool handling.
- `MessagesState` for message state.
- `ChatOpenAI` for the model.
- Message types (`HumanMessage`, `AIMessage`, `SystemMessage`).

**Lines 11-12:** Load environment variables from `.env`.

**Lines 14-16:** Define the agent’s state with `add_messages`.

**Lines 18-23:** Configure the model (gpt-4o, temperature 0.1, max 512 tokens).

**Lines 28-37:** Define arithmetic tools (addition, subtraction, multiplication, division) with docstrings for LLM selection.

**Lines 39-40:** Bind the tools to the model.

**Lines 42-43:** Set a `SystemMessage` to guide behavior.

**Lines 45-47:** The assistant node calls the model and returns messages.

**Lines 49-62:** Build the graph:
- Add `assistant` and `tools` nodes.
- `START` → `assistant`.
- `assistant` → conditional → `tools` or `END`.
- `tools` → `assistant` loop.
- Compile and return.

**Lines 64-89:** Create the agent, print structure, run a multi-step query, and display the flow.

**ReACT difference:** `builder.add_edge("tools", "assistant")` creates the reasoning loop.

python3 react_agent_demo.py

**Expected Output:**
```
🔄 Building ReACT Agent Demo
==================================================
Creating ReACT agent...

ReACT Agent Structure:
- START → assistant
- assistant → tools_condition
- tools_condition: YES → tools
- tools_condition: NO → END
- tools → assistant (LOOP!)

==================================================
Test: Complex multi-step calculation
==================================================

Conversation Flow:

1. Human: Add 3 and 4. Multiply the output by 2. Divide the output by 5

2. AI: I'll help you perform these arithmetic operations step by step.
   Tool Call: addition({'a': 3, 'b': 4})

3. Tool Result: 7

4. AI: Now I'll multiply 7 by 2.
   Tool Call: multiplication({'a': 7, 'b': 2})

5. Tool Result: 14

6. AI: Finally, I'll divide 14 by 5.
   Tool Call: division({'a': 14, 'b': 5})

7. Tool Result: 2.8

8. AI: The final result is 2.8. Here's the breakdown:
3 + 4 = 7
7 × 2 = 14
14 ÷ 5 = 2.8

==================================================
Key Point: The agent looped back multiple times!
Unlike basic tool calling, ReACT creates a reasoning loop.
==================================================
```

### Understanding ReACT Loop 🎯

**What it does:** This demonstrates the key difference between basic tool calling and ReACT.

**Simple explanation:**
Basic tool calling: Use tool once, done
ReACT: Use tool, see result, think, use another tool, repeat until solved

**Real-world analogy:** 
- Basic: "What's 2+2?" → Calculator → "4" → Done
- ReACT: "Solve this multi-step problem" → Calculator → Think → Calculator → Think → Answer

touch react_loop_explanation.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define tools
def addition(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

tools = [addition, multiplication]
model_with_tools = model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful arithmetic assistant.")

def assistant(state: MessagesState):
    return {"messages": model_with_tools.invoke([sys_msg] + state["messages"])}

def create_react_agent():
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")  # Loop back!
    return builder.compile()

if __name__ == "__main__":
    print("🔄 Understanding ReACT Loop")
    print("=" * 50)
    
    react_graph = create_react_agent()
    
    print("\nWhat Happened:")
    print("1. AI reasoned it needed to add 3 and 4")
    print("2. Called addition tool, got result 7")
    print("3. AI reasoned it needed to multiply 7 by 2")
    print("4. Called multiplication tool, got result 14")
    print("5. AI reasoned it needed to divide 14 by 5")
    print("6. Called division tool, got result 2.8")
    print("7. AI provided final answer with summary")
    print()
    
    messages = [HumanMessage(content="I need to calculate something complex: Add 10 and 15, then multiply by 3, then add 100.")]
    result = react_graph.invoke({"messages": messages})
    
    print("\nDetailed Conversation Flow:")
    step_count = 0
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                step_count += 1
                print(f"\n--- Loop {step_count} ---")
    
    print(f"\nTotal reasoning loops: {step_count}")
    print("\nThis is ReACT: Reasoning and acting in a loop until complete!")
```

**Explanation:**

**Lines 1-7:** Import the required packages.

**Lines 10-11:** Load environment variables.

**Lines 13-15:** Define the message state.

**Lines 17-22:** Initialize the model.

**Lines 24-30:** Define two tools: addition and multiplication.

**Lines 32-33:** Bind tools to the model.

**Lines 35-36:** Create the system message.

**Lines 38-40:** Define the assistant node.

**Lines 42-48:** Build the ReACT graph:
- Add nodes.
- Set edges, including the loop back from tools to assistant.

**Lines 50-72:** Main execution:
- Create the agent.
- Print expected steps.
- Process a complex query.
- Count reasoning loops.

**Loop counting:** Increments on each tool call to show the iterations.

This demonstrates ReACT’s iterative reasoning.

python3 react_loop_explanation.py

---

## 9. Memory & Persistence

### Why Memory Matters 🧠

**Problem:** By default, agents start fresh with each query
**Solution:** Memory allows agents to remember previous interactions and maintain context

### How Memory Works in LangGraph 💾

**Simple Explanation:** LangGraph uses "checkpointers" to save state after each step, tied to a conversation session (thread_id).

**Real-world analogy:** It's like having a notebook where the agent writes down everything you've discussed, so it remembers the context in future conversations.

### Adding Memory to Your Agent

**What it does:** This shows how to add memory to an agent so it can remember previous conversations.

**Simple explanation:**
Without memory: Each query starts fresh, no context
With memory: Agent remembers the conversation history
Thread ID: Like having different notebooks for different conversations

**Real-world analogy:** 
- Without memory: Talking to someone who forgets everything you said
- With memory: Talking to someone who remembers your whole conversation

cd ..
cd 05_memory_persistence
touch memory_demo.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define tools
def addition(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

def division(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

tools = [addition, multiplication, division]
model_with_tools = model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful arithmetic assistant.")

def assistant(state: MessagesState):
    return {"messages": model_with_tools.invoke([sys_msg] + state["messages"])}

def create_memory_agent():
    """Create agent with memory capability"""
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    # Add memory checkpointing
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("🧠 Memory & Persistence Demo")
    print("=" * 50)
    
    # Create agent with memory
    agent = create_memory_agent()
    
    # Use thread_id to maintain conversation context
    config = {"configurable": {"thread_id": "demo_session_1"}}
    
    print("\n--- Turn 1: First calculation ---")
    print("User: Add 3 and 4")
    messages = [HumanMessage(content="Add 3 and 4")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Turn 2: Using context ---")
    print("User: Multiply that by 2")
    messages = [HumanMessage(content="Multiply that by 2.")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Turn 3: More context ---")
    print("User: Now divide that by 3")
    messages = [HumanMessage(content="Now divide that by 3")]
    result = agent.invoke({"messages": messages}, config)
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n" + "=" * 50)
    print("Key Point: The agent remembered 'that' and 'that'!")
    print("Memory allows natural, contextual conversations.")
    print("=" * 50)
```

**Explanation:**

**Lines 1-8:** Imports include `MemorySaver` for persistence.

**Lines 11-12:** Load environment variables.

**Lines 14-16:** Define the message state.

**Lines 18-23:** Initialize the model.

**Lines 25-35:** Define arithmetic tools.

**Lines 37-38:** Bind tools to the model.

**Lines 40-41:** Create the system message.

**Lines 43-45:** Define the assistant node.

**Lines 47-57:** Build the agent with memory:
- Create the graph.
- Add `assistant` and `tools` nodes.
- Add a loop from `tools` to `assistant`.
- **Line 55:** Create `MemorySaver`.
- **Line 56:** Compile with `checkpointer=memory`.

**Lines 59-89:** Execute a multi-turn conversation:
- Create the agent.
- **Line 67:** Set a thread ID for context.
- **Lines 69-79:** Execute three turns; context is preserved.

**Notable points:**
- `MemorySaver()` persists state between calls.
- A thread ID groups messages.
- `config` is passed to `invoke` to preserve context.
- Same `config` = same thread; separate `config` = separate threads.

python3 memory_demo.py

**Expected Output:**
```
🧠 Memory & Persistence Demo
==================================================

--- Turn 1: First calculation ---
User: Add 3 and 4
AI: The result of 3 + 4 is 7

--- Turn 2: Using context ---
User: Multiply that by 2
AI: I'll multiply 7 by 2. The result is 14

--- Turn 3: More context ---
User: Now divide that by 3
AI: I'll divide 14 by 3. The result is approximately 4.67

==================================================
Key Point: The agent remembered 'that' and 'that'!
Memory allows natural, contextual conversations.
==================================================
```

### Understanding Memory Threads 🎯

**What it does:** This demonstrates how different thread IDs maintain separate conversation contexts.

**Simple explanation:**
Thread ID is like a notebook name
Different thread IDs = different notebooks
Each conversation thread is independent
Memory is isolated per thread

**Real-world analogy:** Having separate chat rooms - each room remembers only its own conversation history.

touch memory_threads_demo.py

```python
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Define State with Messages
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Define tools
def addition(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

tools = [addition, multiplication]
model_with_tools = model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful arithmetic assistant.")

def assistant(state: MessagesState):
    return {"messages": model_with_tools.invoke([sys_msg] + state["messages"])}

def create_memory_agent():
    """Create agent with memory capability"""
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    # Add memory checkpointing
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

if __name__ == "__main__":
    print("🧠 Understanding Memory Threads")
    print("=" * 50)
    
    # Create agent with memory
    agent = create_memory_agent()
    
    print("\n--- Thread 1: User Alice ---")
    config_alice = {"configurable": {"thread_id": "alice_session"}}
    
    messages = [HumanMessage(content="My favorite number is 10")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: My favorite number is 10")
    print(f"AI: {result['messages'][-1].content}")
    
    messages = [HumanMessage(content="Add 5 to my favorite number")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: Add 5 to my favorite number")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Thread 2: User Bob ---")
    config_bob = {"configurable": {"thread_id": "bob_session"}}
    
    messages = [HumanMessage(content="My favorite number is 20")]
    result = agent.invoke({"messages": messages}, config_bob)
    print(f"User Bob: My favorite number is 20")
    print(f"AI: {result['messages'][-1].content}")
    
    messages = [HumanMessage(content="Add 5 to my favorite number")]
    result = agent.invoke({"messages": messages}, config_bob)
    print(f"User Bob: Add 5 to my favorite number")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n--- Thread 1: User Alice Continues ---")
    messages = [HumanMessage(content="What's my favorite number?")]
    result = agent.invoke({"messages": messages}, config_alice)
    print(f"User Alice: What's my favorite number?")
    print(f"AI: {result['messages'][-1].content}")
    
    print("\n" + "=" * 50)
    print("Key Point: Each thread maintains its own context!")
    print("Alice's favorite number is still 10, Bob's is 20.")
    print("=" * 50)
```

**Explanation:**

**Lines 1-8:** Import the required packages, including `MemorySaver`.

**Lines 11-12:** Load environment variables.

**Lines 14-16:** Define the message state.

**Lines 18-23:** Initialize the model.

**Lines 25-31:** Define tools: addition and multiplication.

**Lines 33-34:** Bind tools to the model.

**Lines 36-37:** Create the system message.

**Lines 39-41:** Define the assistant node.

**Lines 43-53:** Build the memory agent:
- Create the graph.
- Add nodes; set edges, including the loop back from `tools` to `assistant`.
- **Line 52:** Create `MemorySaver`.
- **Line 53:** Compile with `checkpointer=memory`.

**Lines 55-101:** Use separate threads:
- Create the agent.
- **Lines 61, 67:** Set different thread IDs.
- **Lines 63-76:** Alice’s session.
- **Lines 78-89:** Bob’s session.
- **Lines 91-98:** Resume Alice’s session.

**Threading:** Separate contexts allow independent conversations using different config IDs.

python3 memory_threads_demo.py

**Expected Output:**
```
🧠 Understanding Memory Threads
==================================================

--- Thread 1: User Alice ---
User Alice: My favorite number is 10
AI: Thank you for sharing! Your favorite number is 10.

User Alice: Add 5 to my favorite number
AI: Adding 5 to your favorite number 10 gives us 15.

--- Thread 2: User Bob ---
User Bob: My favorite number is 20
AI: Thank you for sharing! Your favorite number is 20.

User Bob: Add 5 to my favorite number
AI: Adding 5 to your favorite number 20 gives us 25.

--- Thread 1: User Alice Continues ---
User Alice: What's my favorite number?
AI: Your favorite number is 10.

==================================================
Key Point: Each thread maintains its own context!
Alice's favorite number is still 10, Bob's is 20.
==================================================
```

### Understanding Memory Benefits 🎯

**What Memory Enables:**
- **Context Awareness:** "Multiply that by 2" works because it remembers the previous result
- **Natural Conversations:** No need to restate everything
- **Stateful Interactions:** Each conversation thread maintains its own state
- **Multi-User Support:** Different threads for different users/conversations

---

## 10. Real-World Project

### Project: Bank Emissions Assessment Agent 🏦

**Goal:** Build a complete agent that helps a bank track and analyze their operational carbon footprint.

### Business Context 📊

**Scenario:** TechBank International's ESG team needs to track operational emissions across all facilities to achieve net-zero goals.

**Emissions Sources:**
- Real estate (offices, branches)
- Fleet vehicles
- Waste management
- Supply chain vendors

### Step 1: Create Emission Calculation Tools

#### Real Estate Emissions
```python
def calculate_real_estate_emissions(
    square_meters: float,
    energy_intensity: float = 0.05
) -> float:
    """
    Calculate CO2 emissions from real estate operations (offices, branches, data centers).

    Args:
        square_meters: Total square meters of real estate
        energy_intensity: Energy intensity factor (kgCO2 per sqm per year), default 0.05

    Returns:
        Annual CO2 emissions in kg
    """
    emissions = square_meters * energy_intensity * 365
    return round(emissions, 2)
```

#### Fleet Emissions
```python
def calculate_fleet_emissions(km_driven: float, fuel_type: str = "diesel") -> float:
    """
    Calculate CO2 emissions from company fleet vehicles.

    Args:
        km_driven: Total kilometers driven
        fuel_type: Type of fuel used - "diesel", "petrol", or "electric"

    Returns:
        CO2 emissions in kg
    """
    # Emission factors in kg CO2 per km
    emission_factors = {
        "diesel": 0.27,
        "petrol": 0.24,
        "electric": 0.05
    }

    factor = emission_factors.get(fuel_type.lower(), 0.27)
    emissions = km_driven * factor
    return round(emissions, 2)
```

#### Waste Emissions
```python
def calculate_waste_emissions(waste_kg: float, recycling_rate: float = 0.3) -> float:
    """
    Calculate CO2 emissions from waste management.

    Args:
        waste_kg: Total waste in kilograms
        recycling_rate: Percentage of waste recycled (0.0 to 1.0), default 0.3

    Returns:
        CO2 emissions in kg
    """
    # Non-recycled waste has higher emission factor
    non_recycled = waste_kg * (1 - recycling_rate)
    recycled = waste_kg * recycling_rate

    emissions = (non_recycled * 0.5) + (recycled * 0.1)
    return round(emissions, 2)
```

#### Supply Chain Emissions
```python
def calculate_supply_chain_emissions(spend_amount: float, category: str = "services") -> float:
    """
    Calculate estimated CO2 emissions from supply chain spending.

    Args:
        spend_amount: Amount spent with vendors in USD
        category: Category of spending - "services", "goods", or "technology"

    Returns:
        Estimated CO2 emissions in kg
    """
    # Emission factors in kg CO2 per USD spent
    emission_factors = {
        "services": 0.2,
        "goods": 0.5,
        "technology": 0.3
    }

    factor = emission_factors.get(category.lower(), 0.3)
    emissions = spend_amount * factor
    return round(emissions, 2)
```

### Step 2: Test the Tools
```python
# Test all tools
print("🏢 Real Estate Emissions")
print(f"10,000 sqm office: {calculate_real_estate_emissions(10000)} kg CO2/year")

print("\n🚗 Fleet Emissions")
print(f"50,000 km diesel: {calculate_fleet_emissions(50000, 'diesel')} kg CO2")
print(f"50,000 km electric: {calculate_fleet_emissions(50000, 'electric')} kg CO2")

print("\n♻️ Waste Emissions")
print(f"5,000 kg waste (30% recycled): {calculate_waste_emissions(5000, 0.3)} kg CO2")

print("\n📦 Supply Chain Emissions")
print(f"$100,000 spent on services: {calculate_supply_chain_emissions(100000, 'services')} kg CO2")
```

**Expected Output:**
```
🏢 Real Estate Emissions
10,000 sqm office: 182500.0 kg CO2/year

🚗 Fleet Emissions
50,000 km diesel: 13500.0 kg CO2
50,000 km electric: 2500.0 kg CO2

♻️ Waste Emissions
5,000 kg waste (30% recycled): 1900.0 kg CO2

📦 Supply Chain Emissions
$100,000 spent on services: 20000.0 kg CO2
```

### Step 3: Build the Emissions Agent

#### Create Specialized Model
```python
# Create a specialized model for emissions assessment
emissions_model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o",
    max_tokens=1024,
    temperature=0.1,
)

# Bind all emissions tools
emissions_tools = [
    calculate_real_estate_emissions,
    calculate_fleet_emissions,
    calculate_waste_emissions,
    calculate_supply_chain_emissions
]
emissions_model_with_tools = emissions_model.bind_tools(emissions_tools)

# System message for the emissions agent
emissions_sys_msg = SystemMessage(content="""
You are an ESG (Environmental, Social, Governance) analyst helping a bank achieve net-zero operational emissions.
1. Calculate emissions from various sources (real estate, fleet, waste, supply chain)
2. Break down complex queries into specific calculations
3. Provide the total emissions in kg CO2
4. Offer recommendations for emissions reduction when appropriate
""")
```

#### Define the Assistant Node
```python
def emissions_assistant(state: MessagesState):
    return {"messages": emissions_model_with_tools.invoke([emissions_sys_msg] + state["messages"])}
```

#### Build the Agent Graph
```python
# Build the emissions agent graph
emissions_agent_builder = StateGraph(MessagesState)
emissions_agent_builder.add_node("emissions_assistant", emissions_assistant)
emissions_agent_builder.add_node("tools", ToolNode(emissions_tools))

# Add edges with ReACT loop
emissions_agent_builder.add_edge(START, "emissions_assistant")
emissions_agent_builder.add_conditional_edges("emissions_assistant", tools_condition)
emissions_agent_builder.add_edge("tools", "emissions_assistant")  # ReACT loop

# Compile
emissions_agent = emissions_agent_builder.compile()
```

### Step 4: Test the Agent

#### Test 1: Single Calculation
```python
messages = [HumanMessage(content="Calculate emissions from our London headquarters which is 15,000 square meters")]
result = emissions_agent.invoke({"messages": messages})

for m in result['messages']:
    m.pretty_print()
```

**Expected Output:**
```
Human Message
Calculate emissions from our London headquarters which is 15,000 square meters

AI Message
"I'll calculate the CO2 emissions from your London headquarters using the real estate emissions calculator."

Tool Call:
calculate_real_estate_emissions(square_meters=15000)

Tool Message:
273750.0

AI Message
Real Estate Emissions — London Headquarters:
- Building size: 15,000 sqm
- Annual CO2 emissions: 273,750 kg CO2 (273.75 tonnes CO2)
- Energy intensity factor: 0.05 kgCO2 per sqm per year (default)

Recommendations:
- LED lighting upgrades
- HVAC optimization
- Renewable energy sourcing
- Green certifications (LEED, BREEAM)
```

#### Test 2: Multi-step Calculation
```python
messages = [HumanMessage(content="""
Calculate our total operational emissions from:
- Our fleet that drove 120,000 km on diesel
- Our office waste of 8,000 kg with 40% recycling rate
- Our technology vendor spending of $250,000
""")]
result = emissions_agent.invoke({"messages": messages})

for m in result['messages']:
    m.pretty_print()
```

**Expected Output:**
```
Human Message
Calculate our total operational emissions from:
- Our fleet that drove 120,000 km on diesel
- Our office waste of 8,000 kg with 40% recycling rate
- Our technology vendor spending of $250,000

AI Message
"I'll calculate the total operational emissions by breaking this down into individual calculations for each source."

Tool Call:
calculate_fleet_emissions(120000, diesel)

Tool Message:
32400.0

Tool Call:
calculate_waste_emissions(8000, 0.4)

Tool Message:
2720.0

Tool Call:
calculate_supply_chain_emissions(250000, technology)

Tool Message:
75000.0

AI Message
## Total Operational Emissions Summary

- Fleet (Diesel vehicles): 32,400 kg CO2
- Waste Management: 2,720 kg CO2
- Supply Chain (Technology vendors): 75,000 kg CO2

TOTAL: 110,120 kg CO2 (110.12 tonnes)

Key Observations:
- Supply chain emissions = 68%
- Fleet emissions = 29%
- Waste management = 2.5%

Recommendations:
- Transition fleet to EVs or hybrids
- Evaluate vendor sustainability
- Increase recycling rate above 40%
```

### Step 5: Add Memory for Multi-Turn Conversations

#### Set Up Memory
```python
from langgraph.checkpoint.memory import MemorySaver

# Add memory to the emissions agent
emissions_memory = MemorySaver()
emissions_agent_with_memory = emissions_agent_builder.compile(checkpointer=emissions_memory)
```

#### Test Multi-Turn Conversation
```python
# Turn 1: Initial Assessment
config = {"configurable": {"thread_id": "esg_analyst_001"}}

print("=" * 70)
print("TURN 1: Calculate baseline emissions")
print("=" * 70)

messages = [HumanMessage(content="Calculate emissions from our Manchester branch: 8,500 square meters")]
result = emissions_agent_with_memory.invoke({"messages": messages}, config)

for m in result['messages']:
    m.pretty_print()
```

**Expected Output:**
```
Human Message:
Calculate emissions from our Manchester branch: 8,500 square meters

AI Message:
"I'll calculate the CO2 emissions from your Manchester branch real estate operations."

Tool Call:
calculate_real_estate_emissions(square_meters=8500)

Tool Message:
155125.0

AI Message:
Real Estate Emissions — Manchester Branch:
- Total emissions: 155,125 kg CO2/year
- Source: 8,500 sqm office space
- Energy intensity factor: 0.05 kgCO2/sqm/year

Recommendations:
- LED lighting upgrades
- HVAC automation
- Renewable energy procurement
- Insulation & energy efficiency
- Temperature controls and sensors
```

#### Turn 2: Adding Fleet Emissions (Contextual)
```python
print("=" * 70)
print("TURN 2: Follow-up adding fleet emissions")
print("=" * 70)

messages = [HumanMessage(content="That branch also has a fleet that drove 45,000 km on diesel. Add that to the total.")]
result = emissions_agent_with_memory.invoke({"messages": messages}, config)

# Print only new messages
for m in result['messages'][-3:]:
    m.pretty_print()
```

**Expected Output:**
```
Tool Call:
calculate_fleet_emissions(45000, diesel)

Tool Message: 12150.0

AI Message:
Manchester Branch — Total Emissions Summary:
- Real Estate: 155,125 kg CO2
- Fleet (Diesel): 12,150 kg CO2
TOTAL: 167,275 kg CO2/year (167.3 tonnes)
Breakdown:
- Real Estate: 92.7%
- Fleet: 7.3%

Fleet Recommendations:
- Transition to electric/hybrid
- Carpooling, teleconferencing, maintenance optimization
```

**Key Point:** The agent remembered "that branch" referred to the Manchester branch from Turn 1!

#### Turn 3: Scenario Comparison
```python
print("=" * 70)
print("TURN 3: Scenario comparison using conversation context")
print("=" * 70)

messages = [HumanMessage(content="If we switched that fleet to electric vehicles, how much would our total emissions decrease?")]
result = emissions_agent_with_memory.invoke({"messages": messages}, config)

for m in result['messages'][-4:]:
    m.pretty_print()
```

**Expected Output:**
```
Tool Call:
calculate_fleet_emissions(45000, electric)

Tool Message:
2250.0

AI Message:
Manchester Branch — Electric Fleet Comparison:

Current (Diesel):
- Real estate: 155,125 kg CO2
- Fleet: 12,150 kg CO2
TOTAL: 167,275 kg CO2

With Electric:
- Real estate: 155,125 kg CO2
- Fleet: 2,250 kg CO2
TOTAL: 157,375 kg CO2

Reduction: 9,900 kg CO2 (9.9 tonnes)
Fleet reduction: 81.5%

This switch significantly reduces fleet emissions by over 80%. Even though fleet is a smaller source than buildings, this is still meaningful progress.
```

### Understanding the Power of Memory 🧠

**What Just Happened:**
1. **Turn 1:** Agent calculated Manchester branch real estate emissions
2. **Turn 2:** Agent understood "that branch" and added fleet emissions
3. **Turn 3:** Agent used stored context to compare diesel vs electric scenarios

**This is the power of memory in LangGraph** — enabling dynamic, stateful conversations and tool use!

---

## 11. Advanced Topics

### Real-World Applications 🌍

The same patterns can be applied to:

#### Customer Service Agents 💬
- **Use Case:** Handle customer inquiries, access databases, resolve issues
- **Tools:** CRM lookup, ticket creation, knowledge base search
- **Memory:** Remember customer history and preferences

#### Financial Analysis Agents 📊
- **Use Case:** Generate reports, analyze metrics, provide recommendations
- **Tools:** Data analysis, chart generation, risk calculations
- **Memory:** Track analysis history and trends

#### IT Support Agents 🧰
- **Use Case:** Diagnose issues, query systems, execute fixes
- **Tools:** System monitoring, log analysis, automated repairs
- **Memory:** Track incident history and solutions

#### Legal Research Agents ⚖️
- **Use Case:** Search documents, analyze cases, provide legal insights
- **Tools:** Document search, case law lookup, precedent analysis
- **Memory:** Track research history and findings

#### Healthcare Agents 🏥
- **Use Case:** Review patient data, coordinate treatment, provide insights
- **Tools:** Medical database access, symptom analysis, treatment recommendations
- **Memory:** Track patient history and treatment plans

### Next Steps 🚀

#### 1. Explore Advanced Features
- **Sub-graphs:** Break complex workflows into smaller, manageable pieces
- **Dynamic Nodes:** Create nodes that can be added or removed at runtime
- **Streaming:** Get real-time updates as the agent processes

#### 2. Production Deployment
- **Error Handling:** Add robust error handling and recovery
- **Monitoring:** Implement logging and performance monitoring
- **Scaling:** Deploy with proper infrastructure and load balancing

#### 3. Security & Access Control
- **Authentication:** Implement user authentication and authorization
- **API Security:** Secure your agent endpoints
- **Data Privacy:** Ensure compliance with data protection regulations

#### 4. Advanced Patterns
- **Multi-Agent Systems:** Create agents that work together
- **Hierarchical Agents:** Build agents that manage other agents
- **Adaptive Agents:** Create agents that learn and improve over time

---

## 🎉 Congratulations!

You've completed the LangGraph Complete Training Guide! You now understand:

✅ **State Management** — defining and managing state in graphs
✅ **Nodes & Edges** — building LangGraph workflows  
✅ **Conditional Routing** — making dynamic decisions
✅ **Tool Calling** — giving agents abilities to perform actions
✅ **Reducers** — accumulating state properly
✅ **ReACT Pattern** — building agents that reason and act iteratively
✅ **Memory** — maintaining context across conversations
✅ **Real-World Applications** — building production-ready agents

### Your Learning Journey Continues! 🚀

You now have the foundation to build sophisticated AI agents that can:
- Make intelligent decisions
- Use tools effectively
- Remember context
- Handle complex multi-step problems
- Provide real business value

**Happy coding and agent building!** 🤖✨

---

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Python TypedDict Documentation](https://docs.python.org/3/library/typing.html#typing.TypedDict)

---

*This training guide was created to help you master LangGraph and build amazing AI agents. Keep experimenting, keep learning, and keep building!* 🎯
