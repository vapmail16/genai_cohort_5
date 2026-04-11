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
