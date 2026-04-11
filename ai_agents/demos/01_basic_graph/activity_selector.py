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