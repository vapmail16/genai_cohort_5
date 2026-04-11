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