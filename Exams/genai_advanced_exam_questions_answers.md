# GenAI Advanced Exam - Questions and Detailed Answers

## 📝 Exam Information

**Total Points**: 200  
**Time Allowed**: 3 hours  
**Topics Covered**: AI Agents, Model Context Protocol (MCP), LangGraph, Offline Models & Fine-Tuning

---

## Question 1: AI Agents Fundamentals & Architecture (20 points)

**Scenario**: You're building an AI agent system for a customer support application that needs to handle complex, multi-step customer inquiries.

### Part A (10 points)
Explain the core components of an AI agent (Perception, Reasoning, Action, Learning) and how they work together in the agent loop. Describe how this differs from a simple LLM chatbot.

### Part B (10 points)
Compare and contrast three agent architectures: Reactive Agents, Deliberative Agents, and Hybrid Agents. For your customer support use case, which architecture would you choose and why? Include a brief code structure showing how you would implement it.

---

### **ANSWER TO QUESTION 1**

#### **Part A: Core Components of AI Agents**

**The Agent Loop: Perceive → Reason → Act → Learn**

**1. Perception (Observation)**
- **What it does**: Extracts relevant information from the environment
- **How it works**: Uses sensors/data inputs to capture current state
- **Example**: Reading user messages, accessing databases, monitoring system status

```python
class AgentPerception:
    def observe(self, environment):
        """Extract relevant information from environment"""
        observations = []
        # Read user input
        observations.append(environment.get_user_message())
        # Check system state
        observations.append(environment.get_system_status())
        # Access knowledge base
        observations.append(environment.search_knowledge_base())
        return observations
```

**2. Reasoning (Decision Making)**
- **What it does**: Processes observations and decides on actions
- **How it works**: Uses LLM to analyze context and generate action plans
- **Example**: Understanding customer intent, determining next steps

```python
class AgentReasoning:
    def think(self, observations, goal):
        """Process observations and decide on action"""
        prompt = f"""
        Observations: {observations}
        Goal: {goal}
        What action should I take?
        """
        reasoning = self.llm.generate(prompt)
        return self.parse_reasoning(reasoning)
```

**3. Action (Tool Execution)**
- **What it does**: Executes the decided actions through tools/functions
- **How it works**: Calls tools, APIs, or functions to interact with environment
- **Example**: Creating tickets, querying databases, sending emails

```python
class AgentAction:
    def execute(self, action_plan):
        """Execute the decided action"""
        results = []
        for action in action_plan:
            tool = self.tools[action.tool_name]
            result = tool.execute(action.parameters)
            results.append(result)
        return results
```

**4. Learning (Memory & Adaptation)**
- **What it does**: Learns from experiences and improves over time
- **How it works**: Stores experiences, extracts patterns, updates behavior
- **Example**: Remembering successful solutions, avoiding past mistakes

```python
class AgentLearning:
    def learn(self, experience):
        """Learn from experience and update behavior"""
        self.memory.append(experience)
        patterns = self.extract_patterns(experience)
        self.update_behavior(patterns)
```

**Complete Agent Loop:**
```
User Query → Perceive (read message, check context)
    ↓
Reason (understand intent, plan response)
    ↓
Act (call tools, query databases, generate response)
    ↓
Learn (store interaction, update patterns)
    ↓
Feedback Loop → Perceive again
```

**Difference from Simple LLM Chatbot:**

| Aspect | Simple LLM Chatbot | AI Agent |
|--------|-------------------|----------|
| **Capabilities** | Text generation only | Can use tools, access systems |
| **Memory** | Limited context window | Persistent memory across sessions |
| **Actions** | Can only respond | Can perform actions (create tickets, etc.) |
| **Reasoning** | Single-step | Multi-step reasoning with tool use |
| **Learning** | No learning | Can learn from experiences |
| **Autonomy** | Reactive only | Can plan and execute complex tasks |

**Key Difference**: A chatbot is a **reactive text generator**, while an AI agent is an **autonomous system** that can perceive, reason, act, and learn to achieve goals.

#### **Part B: Agent Architectures Comparison**

**1. Reactive Agents**
- **How it works**: Responds to current state only, no memory of past states
- **Advantages**: Fast, simple, predictable
- **Disadvantages**: No planning, limited context, can't handle complex tasks

```python
class ReactiveAgent:
    def __init__(self, rules):
        self.rules = rules  # Pre-defined if-then rules
    
    def act(self, current_state):
        for condition, action in self.rules:
            if condition(current_state):
                return action(current_state)
        return "no_action"
```

**2. Deliberative Agents**
- **How it works**: Plans before acting, uses internal models, considers future consequences
- **Advantages**: Can handle complex tasks, makes informed decisions
- **Disadvantages**: Slower, more complex, requires planning capability

```python
class DeliberativeAgent:
    def __init__(self, planner, world_model):
        self.planner = planner
        self.world_model = world_model
    
    def act(self, goal):
        # Create a plan
        plan = self.planner.create_plan(goal, self.world_model)
        # Execute plan step by step
        return self.execute_plan(plan)
```

**3. Hybrid Agents**
- **How it works**: Combines reactive and deliberative approaches
- **Advantages**: Fast for simple tasks, thoughtful for complex ones
- **Disadvantages**: More complex implementation

```python
class HybridAgent:
    def __init__(self, reactive_layer, deliberative_layer):
        self.reactive = reactive_layer
        self.deliberative = deliberative_layer
    
    def act(self, state, goal):
        # Try reactive first (fast path)
        action = self.reactive.act(state)
        if action == "no_action":
            # Fall back to deliberative (complex path)
            action = self.deliberative.act(goal)
        return action
```

**Recommendation for Customer Support:**

**Choose Hybrid Agent** because:

1. **Simple queries** (e.g., "What are your hours?") → Reactive layer handles quickly
2. **Complex queries** (e.g., "I was charged twice for an order I never received") → Deliberative layer plans multi-step resolution
3. **Best of both worlds**: Fast responses for common questions, thoughtful handling for complex issues

**Implementation Structure:**

```python
class CustomerSupportAgent:
    def __init__(self):
        # Reactive layer for common queries
        self.reactive = ReactiveAgent({
            "hours": lambda s: "We're open 9am-5pm EST",
            "contact": lambda s: "Email us at support@company.com",
            # ... more common responses
        })
        
        # Deliberative layer for complex issues
        self.deliberative = DeliberativeAgent(
            planner=MultiStepPlanner(),
            world_model=CustomerSupportWorldModel()
        )
        
        self.tools = {
            "create_ticket": create_support_ticket,
            "check_order": check_order_status,
            "refund": process_refund,
            "escalate": escalate_to_human
        }
    
    def handle_query(self, user_message, context):
        # Try reactive first
        quick_response = self.reactive.act({"message": user_message})
        if quick_response != "no_action":
            return quick_response
        
        # Complex query - use deliberative planning
        goal = self.understand_goal(user_message)
        plan = self.deliberative.plan(goal, context)
        
        # Execute plan with tools
        results = []
        for step in plan:
            if step.requires_tool:
                tool_result = self.tools[step.tool_name](step.parameters)
                results.append(tool_result)
        
        return self.synthesize_response(results)
```

**Why Hybrid Works Best:**
- **Efficiency**: 80% of queries are simple (reactive handles instantly)
- **Capability**: 20% are complex (deliberative handles thoughtfully)
- **User Experience**: Fast for common questions, thorough for complex issues
- **Scalability**: Can handle both high-volume simple queries and low-volume complex ones

---

## Question 2: ReACT Pattern & Tool Integration (20 points)

**Scenario**: You need to build an agent that can solve complex multi-step problems requiring multiple tool calls.

### Part A (10 points)
Explain the ReACT (Reasoning + Acting) pattern. How does it differ from basic tool calling? Describe the execution flow with a diagram showing the reasoning loop.

### Part B (10 points)
Design a ReACT agent using LangGraph that can:
- Perform arithmetic calculations (add, subtract, multiply, divide)
- Handle multi-step problems like "Add 5 and 3, then multiply by 2, then subtract 4"
- Provide a final answer with explanation

Show the complete graph structure, node definitions, and how the loop back mechanism works.

---

### **ANSWER TO QUESTION 2**

#### **Part A: ReACT Pattern Explanation**

**What is ReACT?**

ReACT stands for **Reasoning + Acting**. It's a pattern where an agent:
1. **Reasons** about what to do
2. **Acts** by calling a tool
3. **Observes** the result
4. **Repeats** until the task is complete

**Key Difference from Basic Tool Calling:**

| Aspect | Basic Tool Calling | ReACT Pattern |
|--------|-------------------|---------------|
| **Execution** | Single tool call, done | Multiple tool calls in a loop |
| **Reasoning** | One-time decision | Iterative reasoning after each tool result |
| **Context** | Doesn't see tool results | Sees tool results and reasons about next steps |
| **Complexity** | Simple, linear | Complex, iterative |

**Basic Tool Calling Flow:**
```
User: "What is 4 times 6?"
    ↓
AI: Decides to use multiply tool
    ↓
Tool: multiply(4, 6) = 24
    ↓
AI: "The answer is 24"
    ↓
END (no loop)
```

**ReACT Pattern Flow:**
```
User: "Add 3 and 4, then multiply by 2, then subtract 5"
    ↓
AI: Reasons → "I need to add 3 and 4 first"
    ↓
Tool: add(3, 4) = 7
    ↓
AI: Observes result (7), Reasons → "Now I need to multiply 7 by 2"
    ↓
Tool: multiply(7, 2) = 14
    ↓
AI: Observes result (14), Reasons → "Now I need to subtract 5 from 14"
    ↓
Tool: subtract(14, 5) = 9
    ↓
AI: Observes result (9), Reasons → "Task complete, provide final answer"
    ↓
AI: "The answer is 9. Here's the breakdown: 3+4=7, 7×2=14, 14-5=9"
    ↓
END
```

**Visual Execution Flow Diagram:**

```
┌─────────────────────────────────────────────────────────┐
│                    USER QUERY                            │
│     "Add 3 and 4, multiply by 2, subtract 5"           │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              ASSISTANT NODE (Reasoning)                  │
│  - Analyzes query                                        │
│  - Decides: "I need to add 3 and 4 first"               │
│  - Generates tool call: add(3, 4)                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              CONDITIONAL ROUTING                         │
│  Question: Does AI message have tool_calls?             │
│  Answer: YES → Route to "tools"                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  TOOLS NODE                              │
│  - Executes: add(3, 4)                                   │
│  - Returns: ToolMessage(content="7")                     │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              LOOP BACK TO ASSISTANT                      │
│  (This is the key difference - creates reasoning loop)   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         ASSISTANT NODE (Reasoning Again)                │
│  - Sees previous result: 7                              │
│  - Reasons: "Now I need to multiply 7 by 2"             │
│  - Generates tool call: multiply(7, 2)                  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
              (Loop continues...)
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│         ASSISTANT NODE (Final Reasoning)                 │
│  - Sees all results                                      │
│  - Reasons: "Task complete, provide answer"              │
│  - No tool calls → Route to END                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    FINAL ANSWER                          │
│  "The answer is 9. Breakdown: 3+4=7, 7×2=14, 14-5=9"   │
└─────────────────────────────────────────────────────────┘
```

**Key Insight**: The loop back from "tools" to "assistant" enables iterative reasoning. The agent can see tool results and decide what to do next, creating a reasoning loop.

#### **Part B: Complete ReACT Agent Implementation**

**Complete LangGraph Implementation:**

```python
import os
from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Step 1: Define State
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Step 2: Initialize Model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Step 3: Define Arithmetic Tools
def add(a: int, b: int) -> int:
    """Adds two numbers together"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtracts second number from first number"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiplies two numbers together"""
    return a * b

def divide(a: int, b: int) -> float:
    """Divides first number by second number"""
    if b == 0:
        raise ValueError("Division by zero not allowed")
    return a / b

# Step 4: Bind Tools to Model
tools = [add, subtract, multiply, divide]
model_with_tools = model.bind_tools(tools)

# Step 5: System Message for Reasoning
system_message = SystemMessage(content="""
You are a helpful arithmetic assistant that solves multi-step math problems.

When given a problem:
1. Break it down into steps
2. Use tools to perform calculations
3. After each tool result, decide what to do next
4. Continue until the problem is solved
5. Provide a clear final answer with explanation

Example:
User: "Add 3 and 4, then multiply by 2"
- Step 1: Use add tool → 3 + 4 = 7
- Step 2: Use multiply tool → 7 × 2 = 14
- Final: "The answer is 14. Here's how: 3+4=7, then 7×2=14"
""")

# Step 6: Define Assistant Node
def assistant_node(state: MessagesState):
    """Assistant node that reasons and decides on actions"""
    # Include system message for context
    messages_with_system = [system_message] + state["messages"]
    
    # Get AI response (may include tool calls)
    response = model_with_tools.invoke(messages_with_system)
    
    return {"messages": [response]}

# Step 7: Build the Graph
def create_react_agent():
    """Create a ReACT agent with looping capability"""
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "assistant")  # Start with assistant
    
    # Conditional routing: Does assistant want to use tools?
    builder.add_conditional_edges(
        "assistant",
        tools_condition,  # Built-in: checks for tool_calls
        {
            "tools": "tools",  # If tool_calls exist → go to tools
            "__end__": END     # If no tool_calls → end
        }
    )
    
    # KEY: Loop back from tools to assistant (enables ReACT pattern)
    builder.add_edge("tools", "assistant")
    
    return builder.compile()

# Step 8: Usage Example
if __name__ == "__main__":
    # Create the agent
    agent = create_react_agent()
    
    # Test with multi-step problem
    query = "Add 5 and 3, then multiply by 2, then subtract 4"
    messages = [HumanMessage(content=query)]
    
    result = agent.invoke({"messages": messages})
    
    # Display conversation
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"AI: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    print(f"  → Tool: {tool_call['name']}({tool_call['args']})")
        else:
            print(f"Tool Result: {msg.content}")
```

**Graph Structure Visualization:**

```
START
  │
  ▼
┌─────────────────┐
│   assistant     │  ← Reasoning node
│  (Reasoning)     │
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ tools_condition │  ← Decision point
│  Has tool_calls?│
└─────────────────┘
  │
  ├─ YES ────────────┐
  │                   ▼
  │            ┌──────────────┐
  │            │    tools     │  ← Tool execution
  │            │  (Execute)   │
  │            └──────────────┘
  │                   │
  │                   │ LOOP BACK (key to ReACT!)
  │                   │
  └───────────────────┘
  │
  ├─ NO ────────────────┐
  │                      ▼
  │                 ┌────────┐
  │                 │  END   │
  │                 └────────┘
```

**How the Loop Back Works:**

1. **First Iteration:**
   - Assistant receives: "Add 5 and 3, then multiply by 2, then subtract 4"
   - Assistant reasons: "I need to add 5 and 3 first"
   - Assistant generates: `tool_calls=[add(5, 3)]`
   - Routes to "tools" node
   - Tools execute: `add(5, 3) = 8`
   - **Loop back to assistant** (this is the key!)

2. **Second Iteration:**
   - Assistant sees: Previous query + tool result (8)
   - Assistant reasons: "Now I need to multiply 8 by 2"
   - Assistant generates: `tool_calls=[multiply(8, 2)]`
   - Routes to "tools" node
   - Tools execute: `multiply(8, 2) = 16`
   - **Loop back to assistant** again

3. **Third Iteration:**
   - Assistant sees: Previous query + tool results (8, 16)
   - Assistant reasons: "Now I need to subtract 4 from 16"
   - Assistant generates: `tool_calls=[subtract(16, 4)]`
   - Routes to "tools" node
   - Tools execute: `subtract(16, 4) = 12`
   - **Loop back to assistant**

4. **Final Iteration:**
   - Assistant sees: All tool results (8, 16, 12)
   - Assistant reasons: "Task complete, provide final answer"
   - Assistant generates: Final answer with explanation
   - **No tool calls** → Routes to END

**Expected Output:**

```
Human: Add 5 and 3, then multiply by 2, then subtract 4

AI: I'll solve this step by step.
  → Tool: add({'a': 5, 'b': 3})
Tool Result: 8

AI: Now I'll multiply 8 by 2.
  → Tool: multiply({'a': 8, 'b': 2})
Tool Result: 16

AI: Finally, I'll subtract 4 from 16.
  → Tool: subtract({'a': 16, 'b': 4})
Tool Result: 12

AI: The final answer is 12. Here's the breakdown:
    Step 1: 5 + 3 = 8
    Step 2: 8 × 2 = 16
    Step 3: 16 - 4 = 12
```

**Key Implementation Details:**

1. **`tools_condition`**: Built-in function that checks if last AIMessage has `tool_calls`
2. **Loop back edge**: `builder.add_edge("tools", "assistant")` creates the reasoning loop
3. **State accumulation**: `add_messages` reducer accumulates all messages, so assistant sees full context
4. **System message**: Provides instructions for multi-step reasoning

This implementation enables the agent to reason iteratively, seeing tool results and deciding next steps, which is the core of the ReACT pattern.

---

## Question 3: Model Context Protocol (MCP) Architecture (25 points)

**Scenario**: You're building an MCP server to expose billing operations to AI systems.

### Part A (10 points)
Explain the key differences between traditional REST APIs and MCP. Why is MCP better suited for AI-to-system communication? Include examples of tool discovery, schema validation, and standardized communication.

### Part B (10 points)
Design an MCP server with the following tools:
- `billing.create_invoice(amount, currency, customer_email, idempotency_key)`
- `billing.get_invoice(invoice_id)`
- `billing.update_invoice_status(invoice_id, status)`

Show the complete server implementation including tool registration, input schema validation using Zod, and idempotency handling.

### Part C (5 points)
Explain the three transport methods in MCP (stdio, HTTP, WebSocket). When would you use each one? Provide a brief code example for stdio transport.

---

### **ANSWER TO QUESTION 3**

#### **Part A: REST APIs vs MCP**

**Key Differences:**

| Feature | Traditional REST APIs | MCP (Model Context Protocol) |
|---------|---------------------|------------------------------|
| **Purpose** | General application communication | AI-to-system communication |
| **Discovery** | Manual (read documentation) | Automatic (`tools/list` method) |
| **Schema** | Optional (OpenAPI, etc.) | Built-in (JSON Schema with Zod) |
| **AI Understanding** | Requires custom integration | Native understanding |
| **Standardization** | Varies by implementation | Standardized protocol |
| **Tool Concept** | Not built-in | Built-in tool system |
| **Transport** | Usually HTTP only | stdio, HTTP, WebSocket |

**1. Tool Discovery**

**REST API Approach:**
```javascript
// Problem: You must already know the endpoint exists
// No automatic way to discover available endpoints

// Documentation says: "Use POST /api/invoices to create invoice"
// But there's no programmatic way to discover this

fetch('/api/invoices', { 
  method: 'POST',  // You must know this endpoint accepts POST
  body: JSON.stringify({ amount: 100, currency: 'USD' })
})
// No automatic discovery mechanism
```

**MCP Approach:**
```javascript
// Automatic tool discovery - AI can query at runtime
const tools = await client.request({ 
  method: "tools/list"  // Standard MCP method
});

// Returns: [
//   { 
//     name: "billing.create_invoice", 
//     description: "Create a new invoice",
//     inputSchema: { 
//       type: "object",
//       properties: {
//         amount: { type: "number", minimum: 0 },
//         currency: { type: "string", length: 3 }
//       }
//     }
//   },
//   // ... all available tools with schemas
// ]

// Benefits:
// - No documentation needed
// - Self-documenting with schemas
// - AI can understand capabilities automatically
```

**2. Schema Validation**

**REST API Approach:**
```javascript
// Manual validation required
if (!amount || amount < 0) {
  throw new Error("Invalid amount");
}
if (!currency || currency.length !== 3) {
  throw new Error("Invalid currency");
}
// Validation logic scattered, inconsistent
```

**MCP Approach:**
```typescript
// Built-in schema validation
server.registerTool("billing.create_invoice", {
  inputSchema: {
    amount: z.number().min(0).describe("Invoice amount"),
    currency: z.string().length(3).describe("Currency code")
  }
}, async ({ amount, currency }) => {
  // Validation happens automatically before this function runs
  // You can trust that amount is a number >= 0
  // You can trust that currency is a 3-character string
});
```

**3. Standardized Communication**

**REST API Approach:**
```javascript
// Different APIs use different structures
// Each API requires custom code

// API 1
fetch('https://api1.com/v1/invoices', { method: 'POST', ... })

// API 2  
fetch('https://api2.com/api/billing/invoice', { method: 'POST', ... })

// API 3
fetch('https://api3.com/invoices/create', { method: 'POST', ... })
// Different URL patterns, different structures
```

**MCP Approach:**
```javascript
// Standardized format - same for all MCP servers
const result = await client.request({
  method: "tools/call",  // Always the same method
  params: {
    name: "billing.create_invoice",  // Tool name format
    arguments: { amount: 100, currency: "USD" }  // Standard structure
  }
});
// Same structure works for any MCP server
```

**Why MCP is Better for AI:**

1. **Auto-Discovery**: AI can automatically find available tools without documentation
2. **Self-Describing**: Schemas tell AI exactly what parameters are needed
3. **Standardized**: Same pattern works across all MCP servers
4. **Type-Safe**: Built-in validation ensures correct data types
5. **AI-Optimized**: Designed specifically for AI understanding, not human readability

#### **Part B: Complete MCP Server Implementation**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// In-memory invoice store (in production, use a database)
const invoices = new Map<string, {
  id: string;
  amount: number;
  currency: string;
  customer_email: string;
  status: "draft" | "sent" | "paid" | "cancelled";
  created_at: string;
}>();

// Create MCP Server
const server = new McpServer({
  name: "billing-mcp-server",
  version: "0.1.0"
});

// Tool 1: Create Invoice
server.registerTool(
  "billing.create_invoice",
  {
    description: "Create a new invoice and return its ID. Supports idempotency to prevent duplicate invoices.",
    inputSchema: {
      amount: z.number()
        .min(0, "Amount must be non-negative")
        .describe("Invoice amount in the specified currency"),
      
      currency: z.string()
        .length(3, "Currency must be exactly 3 characters (e.g., USD, EUR)")
        .describe("Currency code (ISO 4217 format)"),
      
      customer_email: z.string()
        .email("Invalid email format")
        .describe("Customer email address"),
      
      idempotency_key: z.string()
        .min(1, "Idempotency key is required")
        .describe("Unique key for idempotency. If invoice with this key exists, returns existing invoice.")
    }
  },
  async ({ amount, currency, customer_email, idempotency_key }) => {
    // Idempotency check - if invoice with this key exists, return it
    if (invoices.has(idempotency_key)) {
      const existing = invoices.get(idempotency_key)!;
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              invoice_id: existing.id,
              reused: true,
              message: "Invoice already exists with this idempotency key",
              invoice: existing
            })
          }
        ]
      };
    }
    
    // Create new invoice
    const invoice = {
      id: idempotency_key,  // Use idempotency_key as invoice ID
      amount,
      currency: currency.toUpperCase(),
      customer_email,
      status: "draft" as const,
      created_at: new Date().toISOString()
    };
    
    // Store invoice
    invoices.set(idempotency_key, invoice);
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            invoice_id: invoice.id,
            reused: false,
            message: "Invoice created successfully",
            invoice
          })
        }
      ]
    };
  }
);

// Tool 2: Get Invoice
server.registerTool(
  "billing.get_invoice",
  {
    description: "Retrieve an invoice by its ID",
    inputSchema: {
      invoice_id: z.string()
        .min(1, "Invoice ID is required")
        .describe("Invoice ID to retrieve")
    }
  },
  async ({ invoice_id }) => {
    const invoice = invoices.get(invoice_id);
    
    if (!invoice) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ 
              error: "NOT_FOUND", 
              message: `Invoice with ID ${invoice_id} not found` 
            })
          }
        ],
        isError: true
      };
    }
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ invoice })
        }
      ]
    };
  }
);

// Tool 3: Update Invoice Status
server.registerTool(
  "billing.update_invoice_status",
  {
    description: "Update the status of an invoice (draft, sent, paid, cancelled)",
    inputSchema: {
      invoice_id: z.string()
        .min(1, "Invoice ID is required")
        .describe("Invoice ID to update"),
      
      status: z.enum(["draft", "sent", "paid", "cancelled"], {
        errorMap: () => ({ message: "Status must be one of: draft, sent, paid, cancelled" })
      })
        .describe("New status for the invoice")
    }
  },
  async ({ invoice_id, status }) => {
    const invoice = invoices.get(invoice_id);
    
    if (!invoice) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ 
              error: "NOT_FOUND",
              message: `Invoice with ID ${invoice_id} not found` 
            })
          }
        ],
        isError: true
      };
    }
    
    // Update status
    invoice.status = status;
    invoices.set(invoice_id, invoice);
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ 
            message: "Invoice status updated successfully",
            invoice 
          })
        }
      ]
    };
  }
);

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Billing MCP server is running on stdio...");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

**Key Implementation Details:**

1. **Tool Registration**: Each tool is registered with `server.registerTool(name, config, handler)`
2. **Schema Validation**: Zod schemas automatically validate inputs before handler runs
3. **Idempotency**: Uses `idempotency_key` to prevent duplicate invoices
4. **Error Handling**: Returns `isError: true` for error cases
5. **Response Format**: Always returns `{ content: [{ type: "text", text: JSON.stringify(...) }] }`

#### **Part C: Transport Methods**

**1. stdio (Standard Input/Output)**
- **What it is**: Communication through standard input/output streams
- **Best for**: Local development, server-to-server communication, process-to-process
- **Pros**: Simple, no network setup, fast for local
- **Cons**: Only works locally, not for web apps

```typescript
// Server side
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const transport = new StdioServerTransport();
await server.connect(transport);
// Server communicates via stdin/stdout

// Client side
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["dist/index.js"],
  cwd: "./servers/billing"
});
await client.connect(transport);
// Client spawns server process and communicates via stdio
```

**2. HTTP (Server-Sent Events)**
- **What it is**: Communication over HTTP protocol
- **Best for**: Web applications, remote servers, REST-like APIs
- **Pros**: Works over network, standard HTTP, good for web
- **Cons**: Stateless, requires HTTP server setup

```typescript
// Server side
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();
const transport = new SSEServerTransport("/mcp", app);

app.listen(3000, async () => {
  await server.connect(transport);
  console.log("MCP server running on http://localhost:3000/mcp");
});
```

**3. WebSocket**
- **What it is**: Bidirectional real-time communication
- **Best for**: Real-time applications, live updates, bidirectional needs
- **Pros**: Real-time, bidirectional, persistent connection
- **Cons**: More complex, requires WebSocket server

**When to Use Each:**

- **stdio**: Development, local services, backend-to-backend
- **HTTP**: Web apps, remote access, standard deployments
- **WebSocket**: Real-time apps, live data, interactive systems

**Example: stdio Transport (Complete)**

```typescript
// servers/billing/src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "billing-server",
  version: "0.1.0"
});

// Register tools...
server.registerTool(/* ... */);

async function main() {
  // Create stdio transport
  const transport = new StdioServerTransport();
  
  // Connect server to transport
  await server.connect(transport);
  
  // Server now listens on stdin and writes to stdout
  console.error("Server running on stdio...");
}

main();
```

**How stdio Works:**
- Server reads requests from `stdin`
- Server writes responses to `stdout`
- Client spawns server as child process
- Communication happens through process pipes
- No network required - direct process communication

---

## Question 4: LangGraph State Management & Architecture (20 points)

**Scenario**: You're building a LangGraph application that needs to maintain conversation context across multiple interactions.

### Part A (10 points)
Explain LangGraph's state management architecture. What is a TypedDict state? What are reducers (specifically `add_messages`)? Why is state immutability important for checkpointing?

### Part B (10 points)
Design a state schema for a customer service agent that needs to track:
- Conversation messages (with full history)
- Current customer information
- Active ticket ID
- Conversation metadata (start time, agent name, priority)

Show the complete TypedDict definition with proper annotations and explain how each field would be used in nodes.

---

### **ANSWER TO QUESTION 4**

#### **Part A: LangGraph State Management Architecture**

**1. TypedDict State**

**What it is:**
- A Python `TypedDict` that defines the structure of data flowing through the graph
- Provides type safety and IDE autocomplete
- Acts as a contract for what data the graph expects and produces

**Example:**
```python
from typing_extensions import TypedDict
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    counter: int
    user_name: str
```

**Benefits:**
- **Type Safety**: IDE and type checkers can validate state access
- **Documentation**: Clear contract of what data is available
- **Autocomplete**: IDE suggests available fields
- **Error Prevention**: Catches typos and missing fields at development time

**2. Reducers**

**What they are:**
- Functions that define how new state merges with existing state
- Specified using `Annotated` type hints
- Control how state updates accumulate

**`add_messages` Reducer:**

```python
from langgraph.graph import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

**How it works:**
```python
# Initial state
state = {"messages": [msg1, msg2]}

# Node returns new messages
new_state = {"messages": [msg3]}

# add_messages reducer combines them
# Result: {"messages": [msg1, msg2, msg3]}
# Old messages are preserved, new messages are appended
```

**Without `add_messages` (BAD):**
```python
class MessagesState(TypedDict):
    messages: list[AnyMessage]  # No reducer

# Problem: New messages would REPLACE old messages
# state = {"messages": [msg1, msg2]}
# new_state = {"messages": [msg3]}
# Result: {"messages": [msg3]}  # msg1 and msg2 are lost!
```

**With `add_messages` (GOOD):**
```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]  # With reducer

# Solution: New messages are APPENDED to old messages
# state = {"messages": [msg1, msg2]}
# new_state = {"messages": [msg3]}
# Result: {"messages": [msg1, msg2, msg3]}  # All messages preserved!
```

**Custom Reducers:**

```python
def add_to_list(old_list: list, new_list: list) -> list:
    """Custom reducer that accumulates lists"""
    return old_list + new_list

class MyState(TypedDict):
    items: Annotated[list[str], add_to_list]

# Usage:
# state = {"items": ["a", "b"]}
# new_state = {"items": ["c"]}
# Result: {"items": ["a", "b", "c"]}
```

**3. State Immutability**

**Principle:**
- State should never be mutated directly
- Nodes return new state, don't modify existing state
- Enables checkpointing, rollback, and parallel execution

**Why Immutability Matters for Checkpointing:**

**1. Checkpointing:**
```python
# With immutability, you can save state at any point
checkpoint_1 = state.copy()  # Save current state
# ... execute node ...
checkpoint_2 = state.copy()  # Save new state
# Can restore to checkpoint_1 or checkpoint_2
```

**2. Rollback:**
```python
# If something goes wrong, restore previous state
if error_occurred:
    state = checkpoint_1  # Restore to previous checkpoint
```

**3. Debugging:**
```python
# Inspect state at each step without affecting execution
checkpoint = get_checkpoint(step=5)
print(checkpoint["messages"])  # See messages at step 5
```

**4. Parallel Execution:**
```python
# Multiple nodes can read state without conflicts
# No race conditions because state isn't mutated
```

**Correct Pattern (Immutable):**
```python
def my_node(state: MyState):
    # Read from state
    current_value = state["counter"]
    
    # Create new value (don't mutate)
    new_value = current_value + 1
    
    # Return new state
    return {"counter": new_value}  # ✅ GOOD: Returns new state
```

**Incorrect Pattern (Mutable):**
```python
def my_node(state: MyState):
    # Mutate existing state (BAD!)
    state["counter"] += 1  # ❌ BAD: Mutates existing state
    return {}  # Returns empty dict
```

**Why This Breaks Checkpointing:**
- If state is mutated, you can't restore previous checkpoints
- Checkpointing relies on being able to save and restore state snapshots
- Mutations make it impossible to go back in time

#### **Part B: Customer Service Agent State Schema**

**Complete TypedDict Definition:**

```python
from typing_extensions import TypedDict
from typing import Annotated, Optional
from datetime import datetime
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class CustomerServiceState(TypedDict):
    # Conversation messages with full history
    messages: Annotated[list[AnyMessage], add_messages]
    
    # Current customer information
    customer_info: Optional[dict]  # {
    #     "customer_id": str,
    #     "name": str,
    #     "email": str,
    #     "account_type": str,
    #     "previous_tickets": list
    # }
    
    # Active ticket tracking
    active_ticket_id: Optional[str]
    
    # Conversation metadata
    metadata: dict  # {
    #     "start_time": str,  # ISO format timestamp
    #     "agent_name": str,
    #     "priority": str,  # "low", "medium", "high", "urgent"
    #     "session_id": str,
    #     "language": str,
    #     "channel": str  # "chat", "email", "phone"
    # }
```

**Detailed Field Explanations:**

**1. `messages: Annotated[list[AnyMessage], add_messages]`**

**Purpose**: Stores complete conversation history

**How it's used:**
```python
def conversation_node(state: CustomerServiceState):
    # Access all messages for context
    all_messages = state["messages"]
    
    # Get last user message
    last_user_msg = [m for m in all_messages if isinstance(m, HumanMessage)][-1]
    
    # LLM sees full conversation history
    response = llm.invoke(all_messages)
    
    # Return new message (reducer appends it)
    return {"messages": [response]}
```

**Why `add_messages`**: Preserves full conversation history across nodes

**2. `customer_info: Optional[dict]`**

**Purpose**: Stores current customer's information

**How it's used:**
```python
def lookup_customer_node(state: CustomerServiceState):
    # Extract customer email from messages
    user_email = extract_email_from_messages(state["messages"])
    
    # Lookup customer in database
    customer = database.get_customer(user_email)
    
    # Update state with customer info
    return {
        "customer_info": {
            "customer_id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "account_type": customer.account_type,
            "previous_tickets": customer.ticket_history
        }
    }

def personalize_response_node(state: CustomerServiceState):
    # Use customer info to personalize response
    customer = state.get("customer_info")
    if customer:
        response = f"Hello {customer['name']}, I see you're a {customer['account_type']} customer..."
    else:
        response = "Hello, how can I help you?"
    
    return {"messages": [AIMessage(content=response)]}
```

**Why Optional**: Customer info may not be available at start of conversation

**3. `active_ticket_id: Optional[str]`**

**Purpose**: Tracks the current support ticket being handled

**How it's used:**
```python
def create_ticket_node(state: CustomerServiceState):
    # Create new support ticket
    ticket = support_system.create_ticket(
        customer_id=state["customer_info"]["customer_id"],
        issue=extract_issue(state["messages"]),
        priority=state["metadata"]["priority"]
    )
    
    # Update state with ticket ID
    return {"active_ticket_id": ticket.id}

def update_ticket_node(state: CustomerServiceState):
    # Update existing ticket with new information
    ticket_id = state["active_ticket_id"]
    if ticket_id:
        support_system.add_note(ticket_id, state["messages"][-1].content)
    
    return {}  # No state changes needed
```

**Why Optional**: Ticket may not exist at conversation start

**4. `metadata: dict`**

**Purpose**: Stores conversation context and configuration

**How it's used:**
```python
def initialize_conversation_node(state: CustomerServiceState):
    # Set up conversation metadata
    return {
        "metadata": {
            "start_time": datetime.now().isoformat(),
            "agent_name": "AI Assistant",
            "priority": "medium",  # Default, can be updated
            "session_id": generate_session_id(),
            "language": "en",
            "channel": "chat"
        }
    }

def prioritize_conversation_node(state: CustomerServiceState):
    # Analyze messages to determine priority
    messages = state["messages"]
    urgency_keywords = ["urgent", "critical", "down", "broken"]
    
    priority = "low"
    for msg in messages:
        if any(keyword in msg.content.lower() for keyword in urgency_keywords):
            priority = "high"
            break
    
    # Update metadata
    metadata = state["metadata"].copy()
    metadata["priority"] = priority
    
    return {"metadata": metadata}
```

**Complete Example Usage:**

```python
# Initial state
initial_state = {
    "messages": [HumanMessage(content="I need help with my account")],
    "customer_info": None,
    "active_ticket_id": None,
    "metadata": {
        "start_time": "2024-01-15T10:00:00",
        "agent_name": "AI Assistant",
        "priority": "medium",
        "session_id": "session_123",
        "language": "en",
        "channel": "chat"
    }
}

# After customer lookup node
state_after_lookup = {
    "messages": [HumanMessage(...), AIMessage(...)],
    "customer_info": {
        "customer_id": "cust_456",
        "name": "John Doe",
        "email": "john@example.com",
        "account_type": "premium",
        "previous_tickets": ["ticket_1", "ticket_2"]
    },
    "active_ticket_id": None,
    "metadata": {...}
}

# After ticket creation node
state_after_ticket = {
    "messages": [...],
    "customer_info": {...},
    "active_ticket_id": "ticket_789",  # Now has active ticket
    "metadata": {...}
}
```

**State Access Patterns:**

```python
def example_node(state: CustomerServiceState):
    # Access messages
    messages = state["messages"]
    last_message = messages[-1]
    
    # Access customer info (with None check)
    customer = state.get("customer_info")
    if customer:
        customer_name = customer["name"]
    
    # Access ticket ID
    ticket_id = state.get("active_ticket_id")
    
    # Access metadata
    priority = state["metadata"]["priority"]
    session_id = state["metadata"]["session_id"]
    
    # Return partial state update
    return {
        "metadata": {
            **state["metadata"],  # Preserve existing metadata
            "priority": "high"     # Update priority
        }
    }
```

This state schema enables the agent to maintain full context across the conversation, track customer information, manage tickets, and store metadata for proper conversation handling.

---

*End of Part 1 (Questions 1-4). Continue with Part 2 for Questions 5-7...*

# GenAI Advanced Exam - Questions and Detailed Answers (Part 2: Q5-Q7)

---

## Question 5: LangGraph Nodes, Edges & Conditional Routing (15 points)

**Scenario**: You need to build a graph that makes decisions based on conversation state.

### Part A (8 points)
Explain the difference between simple edges and conditional edges in LangGraph. When would you use each? Show code examples of both.

### Part B (7 points)
Design a conditional routing function that:
- Routes to "tools" node if the last AI message contains tool calls
- Routes to "human" node if human input is required
- Routes to "end" if the conversation is complete

Show the complete routing function with proper type hints and edge configuration.

---

### **ANSWER TO QUESTION 5**

#### **Part A: Simple Edges vs Conditional Edges**

**Simple Edges:**

**What they are:**
- Direct, unconditional connections between nodes
- Always follow the same path
- No decision-making involved

**When to use:**
- Sequential processing (A → B → C)
- Fixed execution flow
- No branching logic needed

**Code Example:**
```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(MyState)

# Add nodes
builder.add_node("node_1", node_1_function)
builder.add_node("node_2", node_2_function)
builder.add_node("node_3", node_3_function)

# Simple edges - always follow this path
builder.add_edge(START, "node_1")      # Always start with node_1
builder.add_edge("node_1", "node_2")  # node_1 always goes to node_2
builder.add_edge("node_2", "node_3")   # node_2 always goes to node_3
builder.add_edge("node_3", END)        # node_3 always ends

# Execution flow: START → node_1 → node_2 → node_3 → END
# This path is ALWAYS the same, no decisions made
```

**Visual Representation:**
```
START → node_1 → node_2 → node_3 → END
```
(Linear, predictable path)

**Conditional Edges:**

**What they are:**
- Dynamic routing based on state
- Decision-making at runtime
- Can branch to different paths

**When to use:**
- Need to make decisions based on state
- Different paths for different conditions
- Dynamic execution flow

**Code Example:**
```python
from typing import Literal

def route_decision(state: MyState) -> Literal["path_a", "path_b"]:
    """Routing function that decides which path to take"""
    if state["condition"] == "option_1":
        return "path_a"
    else:
        return "path_b"

builder = StateGraph(MyState)

builder.add_node("start_node", start_function)
builder.add_node("path_a_node", path_a_function)
builder.add_node("path_b_node", path_b_function)

# Conditional edge - makes decision at runtime
builder.add_edge(START, "start_node")
builder.add_conditional_edges(
    "start_node",
    route_decision,  # Function that decides the path
    {
        "path_a": "path_a_node",  # If route_decision returns "path_a"
        "path_b": "path_b_node"   # If route_decision returns "path_b"
    }
)
builder.add_edge("path_a_node", END)
builder.add_edge("path_b_node", END)

# Execution flow depends on state["condition"]:
# If condition == "option_1": START → start_node → path_a_node → END
# Otherwise: START → start_node → path_b_node → END
```

**Visual Representation:**
```
        START
          │
          ▼
    ┌──────────┐
    │start_node│
    └──────────┘
          │
          ▼
    ┌─────────────┐
    │route_decision│
    └─────────────┘
      │         │
   YES│         │NO
      │         │
      ▼         ▼
  path_a    path_b
      │         │
      └────┬────┘
           ▼
          END
```
(Dynamic, decision-based routing)

**Comparison Table:**

| Aspect | Simple Edges | Conditional Edges |
|--------|-------------|-------------------|
| **Decision Making** | None | Runtime decision based on state |
| **Flexibility** | Fixed path | Dynamic path |
| **Use Case** | Sequential processing | Branching logic |
| **Complexity** | Simple | More complex |
| **Performance** | Faster (no evaluation) | Slightly slower (evaluation needed) |

**When to Use Each:**

**Use Simple Edges when:**
- ✅ Processing pipeline (A → B → C)
- ✅ Fixed workflow
- ✅ No decisions needed
- ✅ Sequential steps

**Use Conditional Edges when:**
- ✅ Need to branch based on state
- ✅ Different paths for different conditions
- ✅ Dynamic routing
- ✅ Decision-making required

#### **Part B: Advanced Conditional Routing Function**

**Complete Implementation:**

```python
from typing_extensions import TypedDict
from typing import Annotated, Literal
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    requires_human_input: bool
    conversation_complete: bool

def advanced_routing_function(
    state: MessagesState
) -> Literal["tools", "human", "end"]:
    """
    Advanced routing function that decides next step based on multiple conditions.
    
    Routing Logic:
    1. If last AI message has tool_calls → route to "tools"
    2. If human input is required → route to "human"
    3. If conversation is complete → route to "end"
    4. Default → route to "end"
    """
    messages = state["messages"]
    
    # Check 1: Does last AI message have tool calls?
    if messages:
        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                # AI wants to use tools
                return "tools"
    
    # Check 2: Is human input required?
    if state.get("requires_human_input", False):
        # Flag set indicating human intervention needed
        return "human"
    
    # Check 3: Is conversation complete?
    if state.get("conversation_complete", False):
        # Conversation has reached natural end
        return "end"
    
    # Check 4: Last message is from human and no further action needed
    if messages:
        last_message = messages[-1]
        if isinstance(last_message, HumanMessage):
            # Human sent message, but no tool calls or special flags
            # Default to end (or could route to assistant node)
            return "end"
    
    # Default: end conversation
    return "end"

# Graph setup with conditional routing
def create_advanced_graph():
    from langgraph.graph import StateGraph, START, END
    
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", tools_node)
    builder.add_node("human", human_input_node)
    
    # Add edges
    builder.add_edge(START, "assistant")
    
    # Conditional routing from assistant
    builder.add_conditional_edges(
        "assistant",
        advanced_routing_function,  # Routing function
        {
            "tools": "tools",      # Route to tools node
            "human": "human",     # Route to human input node
            "end": END            # End conversation
        }
    )
    
    # After tools, loop back to assistant
    builder.add_edge("tools", "assistant")
    
    # After human input, continue to assistant
    builder.add_edge("human", "assistant")
    
    return builder.compile()
```

**Alternative: Using Built-in `tools_condition` with Custom Logic:**

```python
from langgraph.prebuilt import tools_condition
from typing import Literal

def custom_routing_function(
    state: MessagesState
) -> Literal["tools", "human", "end"]:
    """
    Enhanced routing that combines tools_condition with custom logic.
    """
    # First check: Use built-in tools_condition logic
    tools_result = tools_condition(state)
    
    if tools_result == "tools":
        # AI wants to use tools
        return "tools"
    
    # Second check: Human input required?
    if state.get("requires_human_input", False):
        return "human"
    
    # Third check: Conversation complete?
    if state.get("conversation_complete", False):
        return "end"
    
    # Default: end
    return "end"

# Graph with enhanced routing
def create_enhanced_graph():
    builder = StateGraph(MessagesState)
    
    builder.add_node("assistant", assistant_node)
    builder.add_node("tools", tools_node)
    builder.add_node("human", human_input_node)
    
    builder.add_edge(START, "assistant")
    
    # Use custom routing function
    builder.add_conditional_edges(
        "assistant",
        custom_routing_function,
        {
            "tools": "tools",
            "human": "human",
            "end": END
        }
    )
    
    builder.add_edge("tools", "assistant")
    builder.add_edge("human", "assistant")
    
    return builder.compile()
```

**Complete Example with Node Implementations:**

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

# Initialize model and tools
model = ChatOpenAI(model="gpt-4o")
tools = [add, subtract, multiply, divide]
model_with_tools = model.bind_tools(tools)

def assistant_node(state: MessagesState):
    """Assistant node that processes messages and may call tools"""
    response = model_with_tools.invoke(state["messages"])
    
    # Check if response indicates conversation is complete
    conversation_complete = "goodbye" in response.content.lower() or \
                           "thank you" in response.content.lower()
    
    return {
        "messages": [response],
        "conversation_complete": conversation_complete
    }

def tools_node(state: MessagesState):
    """Tools node that executes tool calls"""
    tool_node = ToolNode(tools)
    result = tool_node.invoke(state)
    return result

def human_input_node(state: MessagesState):
    """Human input node - in production, this would wait for user input"""
    # In a real system, this would:
    # 1. Pause execution
    # 2. Wait for human input
    # 3. Resume with human message
    
    # For this example, we'll simulate it
    human_message = HumanMessage(content="[Waiting for human input...]")
    
    return {
        "messages": [human_message],
        "requires_human_input": False  # Reset flag after handling
    }

# Routing function
def route_decision(state: MessagesState) -> Literal["tools", "human", "end"]:
    """Decides routing based on state"""
    
    # Check for tool calls
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage):
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
    
    # Check for human input requirement
    if state.get("requires_human_input", False):
        return "human"
    
    # Check for conversation completion
    if state.get("conversation_complete", False):
        return "end"
    
    # Default to end
    return "end"
```

**Graph Visualization:**

```
                    START
                      │
                      ▼
              ┌──────────────┐
              │  assistant   │
              │  (Reasoning) │
              └──────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │ route_decision   │
            └─────────────────┘
              │      │      │
         tools│      │human │end
              │      │      │
              ▼      ▼      ▼
         ┌────┴──┐ ┌─┴──┐  END
         │ tools │ │human│
         └────┬──┘ └─┬──┘
              │      │
              └──┬───┘
                 │
                 ▼
            assistant
         (loop back)
```

**Key Points:**

1. **Type Hints**: Function returns `Literal["tools", "human", "end"]` for type safety
2. **State Inspection**: Checks multiple conditions in priority order
3. **Edge Mapping**: Maps return values to node names
4. **Loop Back**: Tools and human nodes loop back to assistant for continued processing
5. **Default Case**: Always has a default path (end) to prevent infinite loops

This routing function enables sophisticated decision-making in the graph, allowing it to dynamically choose the next step based on conversation state.

---

## Question 6: LangGraph Checkpointing & Memory (15 points)

**Scenario**: Your agent needs to remember conversations across multiple sessions for different users.

### Part A (8 points)
Compare MemorySaver and SQLiteSaver checkpointers. What are the trade-offs? When would you use each in production?

### Part B (7 points)
Explain how thread IDs work in LangGraph. Show how to:
- Create a new conversation thread
- Resume an existing thread
- Maintain separate contexts for multiple users

Include code examples demonstrating thread isolation.

---

### **ANSWER TO QUESTION 6**

#### **Part A: MemorySaver vs SQLiteSaver**

**MemorySaver (In-Memory Checkpointer)**

**What it is:**
- Stores checkpoints in memory (Python dictionary)
- Fast, simple, no external dependencies
- Lost when process restarts

**Implementation:**
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
```

**Characteristics:**

| Aspect | Details |
|--------|---------|
| **Storage** | In-memory (RAM) |
| **Persistence** | Lost on restart |
| **Speed** | Very fast (no I/O) |
| **Scalability** | Limited by RAM |
| **Sharing** | Single process only |
| **Setup** | No setup required |
| **Best For** | Development, testing, short sessions |

**Pros:**
- ✅ Fastest performance (no disk I/O)
- ✅ Simple setup (no configuration)
- ✅ Good for development
- ✅ No external dependencies

**Cons:**
- ❌ Not persistent (lost on restart)
- ❌ Not shared across processes
- ❌ Limited by available RAM
- ❌ Not suitable for production

**SQLiteSaver (Database Checkpointer)**

**What it is:**
- Stores checkpoints in SQLite database
- Persistent across restarts
- Can be shared across processes

**Implementation:**
```python
from langgraph.checkpoint.sqlite import SqliteSaver

db = SqliteSaver.from_conn_string("checkpoints.db")
graph = builder.compile(checkpointer=db)
```

**Characteristics:**

| Aspect | Details |
|--------|---------|
| **Storage** | SQLite database file |
| **Persistence** | Persistent across restarts |
| **Speed** | Slower (disk I/O) |
| **Scalability** | Limited by disk space |
| **Sharing** | Can share across processes |
| **Setup** | Requires database file |
| **Best For** | Production, long-term persistence |

**Pros:**
- ✅ Persistent (survives restarts)
- ✅ Can share across processes
- ✅ Suitable for production
- ✅ Can handle large amounts of data
- ✅ Transactional (ACID properties)

**Cons:**
- ❌ Slower than MemorySaver (disk I/O)
- ❌ Requires database file management
- ❌ More complex setup
- ❌ Disk space considerations

**Performance Comparison:**

```python
# MemorySaver: ~0.1ms per checkpoint
memory = MemorySaver()
# Very fast, but lost on restart

# SQLiteSaver: ~5-10ms per checkpoint
db = SqliteSaver.from_conn_string("checkpoints.db")
# Slower, but persistent
```

**When to Use Each:**

**Use MemorySaver when:**
- ✅ Development and testing
- ✅ Short-lived sessions
- ✅ Single process application
- ✅ Prototyping
- ✅ Performance testing

**Example:**
```python
# Development/testing
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Fast iteration, no persistence needed
```

**Use SQLiteSaver when:**
- ✅ Production applications
- ✅ Long-term persistence needed
- ✅ Multi-process deployments
- ✅ User sessions that span days/weeks
- ✅ Need to recover from crashes

**Example:**
```python
# Production
db = SqliteSaver.from_conn_string("production_checkpoints.db")
graph = builder.compile(checkpointer=db)

# Persistent, shared, production-ready
```

**Hybrid Approach:**

```python
import os

# Use MemorySaver in development, SQLiteSaver in production
if os.getenv("ENVIRONMENT") == "production":
    checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
else:
    checkpointer = MemorySaver()

graph = builder.compile(checkpointer=checkpointer)
```

#### **Part B: Thread IDs and Context Isolation**

**What are Thread IDs?**

Thread IDs are unique identifiers that group related checkpoints together. Each conversation session has its own thread ID, enabling:
- Separate conversation contexts
- Multi-user support
- Session isolation
- Conversation history per user

**1. Create a New Conversation Thread**

```python
import uuid
from langgraph.checkpoint.memory import MemorySaver

# Create checkpointer
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Create new thread ID for new conversation
def create_new_thread():
    """Create a new conversation thread"""
    thread_id = f"thread_{uuid.uuid4()}"
    config = {"configurable": {"thread_id": thread_id}}
    return config

# Usage
config = create_new_thread()
# config = {"configurable": {"thread_id": "thread_abc123"}}

# Start conversation with new thread
result = graph.invoke(
    {"messages": [HumanMessage("Hello!")]},
    config
)
```

**2. Resume an Existing Thread**

```python
def resume_thread(thread_id: str):
    """Resume an existing conversation thread"""
    config = {"configurable": {"thread_id": thread_id}}
    return config

# Usage: Resume previous conversation
existing_thread_id = "thread_abc123"
config = resume_thread(existing_thread_id)

# Continue conversation - state is automatically loaded!
result = graph.invoke(
    {"messages": [HumanMessage("What was my previous question?")]},
    config
)
# The agent remembers the previous conversation!
```

**3. Maintain Separate Contexts for Multiple Users**

```python
class ConversationManager:
    """Manages multiple user conversations"""
    
    def __init__(self):
        self.memory = MemorySaver()
        self.graph = builder.compile(checkpointer=self.memory)
        self.user_threads = {}  # Map user_id to thread_id
    
    def get_or_create_thread(self, user_id: str):
        """Get existing thread or create new one for user"""
        if user_id not in self.user_threads:
            # Create new thread for new user
            thread_id = f"user_{user_id}_{uuid.uuid4()}"
            self.user_threads[user_id] = thread_id
        return self.user_threads[user_id]
    
    def handle_user_message(self, user_id: str, message: str):
        """Handle message from specific user"""
        # Get or create thread for this user
        thread_id = self.get_or_create_thread(user_id)
        config = {"configurable": {"thread_id": thread_id}}
        
        # Process message in user's conversation context
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config
        )
        
        return result
    
    def get_user_conversation_history(self, user_id: str):
        """Get conversation history for a user"""
        if user_id not in self.user_threads:
            return []
        
        thread_id = self.user_threads[user_id]
        config = {"configurable": {"thread_id": thread_id}}
        
        # Get latest checkpoint (contains all messages)
        checkpoint = self.memory.get(config)
        if checkpoint:
            return checkpoint["channel_values"]["messages"]
        return []

# Usage Example
manager = ConversationManager()

# User Alice sends messages
alice_result_1 = manager.handle_user_message("alice", "My name is Alice")
alice_result_2 = manager.handle_user_message("alice", "What's my name?")
# Agent remembers: "Your name is Alice"

# User Bob sends messages (separate context)
bob_result_1 = manager.handle_user_message("bob", "My name is Bob")
bob_result_2 = manager.handle_user_message("bob", "What's my name?")
# Agent remembers: "Your name is Bob"

# Alice's context is separate from Bob's
alice_history = manager.get_user_conversation_history("alice")
# Contains only Alice's conversation

bob_history = manager.get_user_conversation_history("bob")
# Contains only Bob's conversation
```

**Complete Multi-User Example:**

```python
from typing_extensions import TypedDict
from typing import Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
import uuid

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Create graph with checkpointer
memory = MemorySaver()
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile(checkpointer=memory)

# User session management
user_sessions = {}

def get_user_config(user_id: str):
    """Get or create config for user"""
    if user_id not in user_sessions:
        user_sessions[user_id] = f"user_{user_id}_{uuid.uuid4()}"
    
    thread_id = user_sessions[user_id]
    return {"configurable": {"thread_id": thread_id}}

# Simulate multiple users
users = ["alice", "bob", "charlie"]

# Each user has separate conversation
for user_id in users:
    config = get_user_config(user_id)
    
    # User introduces themselves
    result1 = graph.invoke(
        {"messages": [HumanMessage(f"My name is {user_id.capitalize()}")]},
        config
    )
    
    # User asks for their name (agent remembers!)
    result2 = graph.invoke(
        {"messages": [HumanMessage("What's my name?")]},
        config
    )
    
    print(f"{user_id}: {result2['messages'][-1].content}")
    # Each user gets their own name back - contexts are isolated!

# Output:
# alice: Your name is Alice
# bob: Your name is Bob
# charlie: Your name is Charlie
```

**Thread Isolation Demonstration:**

```python
# Thread 1: Alice's conversation
alice_config = {"configurable": {"thread_id": "thread_alice_123"}}

result1 = graph.invoke(
    {"messages": [HumanMessage("I like pizza")]},
    alice_config
)

result2 = graph.invoke(
    {"messages": [HumanMessage("What do I like?")]},
    alice_config
)
# Result: "You like pizza" (remembers from thread 1)

# Thread 2: Bob's conversation (separate context)
bob_config = {"configurable": {"thread_id": "thread_bob_456"}}

result3 = graph.invoke(
    {"messages": [HumanMessage("What do I like?")]},
    bob_config
)
# Result: "I don't have that information" (different thread, no context)

# Thread 1 again: Alice's conversation continues
result4 = graph.invoke(
    {"messages": [HumanMessage("I also like ice cream")]},
    alice_config
)
# Alice's context continues - remembers pizza AND ice cream
```

**Key Points:**

1. **Thread ID = Conversation ID**: Each thread maintains its own state
2. **Isolation**: Different threads don't see each other's state
3. **Persistence**: Thread state persists across invocations (with checkpointer)
4. **Multi-User**: One thread per user = separate conversations
5. **Resume**: Can resume any thread by using its thread ID

This enables true multi-user support where each user has their own isolated conversation context that persists across sessions.

---

## Question 7: Multi-Agent Systems & Coordination (15 points)

**Scenario**: You need to build a system where multiple specialized agents collaborate to solve complex problems.

### Part A (8 points)
Explain two multi-agent coordination patterns: Master-Worker and Peer-to-Peer. What are the advantages and disadvantages of each?

### Part B (7 points)
Design a multi-agent system for a research assistant where:
- A "researcher" agent searches for information
- An "analyzer" agent processes the results
- A "summarizer" agent creates the final report

Show how these agents would communicate and coordinate. Include a high-level architecture diagram.

---

### **ANSWER TO QUESTION 7**

#### **Part A: Multi-Agent Coordination Patterns**

**1. Master-Worker Pattern**

**How it works:**
- One master agent coordinates the work
- Multiple worker agents perform specific tasks
- Master decomposes problem, assigns to workers, aggregates results

**Architecture:**
```
                    Master Agent
                    (Coordinator)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Worker 1          Worker 2          Worker 3
   (Task A)          (Task B)          (Task C)
        │                │                │
        └────────────────┼────────────────┘
                         │
                    Results
                         │
                    Master Agent
                    (Aggregates)
```

**Implementation:**
```python
class MasterWorkerPattern:
    def __init__(self, master_agent, worker_agents):
        self.master = master_agent
        self.workers = worker_agents
    
    def execute_task(self, task):
        # Master decomposes task
        subtasks = self.master.decompose(task)
        
        # Distribute to workers
        for i, subtask in enumerate(subtasks):
            worker = self.workers[i % len(self.workers)]
            worker.assign_task(subtask)
        
        # Collect results
        results = []
        for worker in self.workers:
            results.extend(worker.get_results())
        
        # Master aggregates
        return self.master.aggregate(results)
```

**Advantages:**
- ✅ Centralized control (easy to manage)
- ✅ Clear hierarchy (master coordinates)
- ✅ Efficient task distribution
- ✅ Easy to scale (add more workers)
- ✅ Simple to implement

**Disadvantages:**
- ❌ Single point of failure (master)
- ❌ Master can become bottleneck
- ❌ Less flexible (workers are specialized)
- ❌ Master needs to understand all tasks

**Use Cases:**
- Parallel processing (divide and conquer)
- Specialized workers (each does one thing well)
- Controlled coordination needed

**2. Peer-to-Peer Pattern**

**How it works:**
- All agents are equal (no master)
- Agents communicate directly with each other
- Consensus mechanism for decisions
- Distributed coordination

**Architecture:**
```
        Agent 1 ───────┐
                        │
        Agent 2 ───────┼─── Communication Network
                        │
        Agent 3 ───────┘
        
    All agents communicate directly
    No central coordinator
```

**Implementation:**
```python
class PeerToPeerPattern:
    def __init__(self, agents):
        self.agents = agents
        self.consensus_mechanism = ConsensusMechanism()
        self.message_bus = MessageBus()
        
        # Each agent can communicate with others
        for agent in self.agents:
            agent.set_message_bus(self.message_bus)
    
    def collaborate(self, task):
        # Each agent proposes solution
        proposals = []
        for agent in self.agents:
            proposal = agent.propose_solution(task)
            proposals.append(proposal)
        
        # Reach consensus
        consensus = self.consensus_mechanism.reach_consensus(proposals)
        
        return consensus
```

**Advantages:**
- ✅ No single point of failure
- ✅ Highly flexible (agents can adapt)
- ✅ Distributed (no bottleneck)
- ✅ Resilient (if one agent fails, others continue)
- ✅ Scalable (easy to add agents)

**Disadvantages:**
- ❌ More complex coordination
- ❌ Consensus can be slow
- ❌ Potential for conflicts
- ❌ Harder to debug
- ❌ Requires communication protocol

**Use Cases:**
- Distributed systems
- Collaborative problem solving
- When resilience is critical
- When no single agent should have control

**Comparison Table:**

| Aspect | Master-Worker | Peer-to-Peer |
|--------|--------------|--------------|
| **Control** | Centralized (master) | Distributed (all agents) |
| **Coordination** | Master coordinates | Agents coordinate themselves |
| **Failure** | Master = single point of failure | No single point of failure |
| **Complexity** | Simpler | More complex |
| **Flexibility** | Less flexible | More flexible |
| **Scalability** | Easy to scale workers | Easy to add peers |
| **Best For** | Parallel tasks, specialization | Collaborative, distributed |

#### **Part B: Research Assistant Multi-Agent System**

**System Design:**

```python
from typing_extensions import TypedDict
from typing import Annotated, List, Dict, Any
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, add_messages

class ResearchState(TypedDict):
    # Original query
    query: str
    
    # Messages for communication between agents
    messages: Annotated[list[AnyMessage], add_messages]
    
    # Research results from researcher agent
    research_results: List[Dict[str, Any]]
    
    # Analysis from analyzer agent
    analysis: Dict[str, Any]
    
    # Final summary from summarizer agent
    final_summary: str
    
    # Metadata
    status: str  # "researching", "analyzing", "summarizing", "complete"

# Agent 1: Researcher Agent
def researcher_agent(state: ResearchState):
    """Searches for information related to the query"""
    query = state["query"]
    
    # Simulate research (in production, would search databases, web, etc.)
    research_results = [
        {"source": "Paper 1", "content": "Relevant information about query"},
        {"source": "Paper 2", "content": "More relevant information"},
        {"source": "Database", "content": "Additional findings"}
    ]
    
    return {
        "research_results": research_results,
        "status": "analyzing",
        "messages": [AIMessage(content=f"Found {len(research_results)} relevant sources")]
    }

# Agent 2: Analyzer Agent
def analyzer_agent(state: ResearchState):
    """Analyzes research results and extracts key insights"""
    research_results = state["research_results"]
    
    # Analyze results (in production, would use LLM to analyze)
    analysis = {
        "key_findings": [
            "Finding 1 from research",
            "Finding 2 from research",
            "Finding 3 from research"
        ],
        "confidence_scores": [0.9, 0.85, 0.8],
        "sources_count": len(research_results),
        "topics_covered": ["topic1", "topic2", "topic3"]
    }
    
    return {
        "analysis": analysis,
        "status": "summarizing",
        "messages": [AIMessage(content="Analysis complete. Key findings extracted.")]
    }

# Agent 3: Summarizer Agent
def summarizer_agent(state: ResearchState):
    """Creates final summary report"""
    query = state["query"]
    analysis = state["analysis"]
    
    # Create summary (in production, would use LLM)
    final_summary = f"""
    Research Summary for: {query}
    
    Key Findings:
    {chr(10).join(f"- {finding}" for finding in analysis['key_findings'])}
    
    Topics Covered: {', '.join(analysis['topics_covered'])}
    Sources Analyzed: {analysis['sources_count']}
    
    This research provides comprehensive coverage of the topic with high confidence scores.
    """
    
    return {
        "final_summary": final_summary,
        "status": "complete",
        "messages": [AIMessage(content=final_summary)]
    }

# Coordination function
def route_to_next_agent(state: ResearchState) -> str:
    """Routes to next agent based on status"""
    status = state.get("status", "researching")
    
    if status == "researching" or not state.get("research_results"):
        return "researcher"
    elif status == "analyzing" or not state.get("analysis"):
        return "analyzer"
    elif status == "summarizing" or not state.get("final_summary"):
        return "summarizer"
    else:
        return "end"

# Build the multi-agent graph
def create_research_assistant():
    builder = StateGraph(ResearchState)
    
    # Add agent nodes
    builder.add_node("researcher", researcher_agent)
    builder.add_node("analyzer", analyzer_agent)
    builder.add_node("summarizer", summarizer_agent)
    
    # Add edges with conditional routing
    builder.add_edge(START, "researcher")
    
    builder.add_conditional_edges(
        "researcher",
        route_to_next_agent,
        {
            "analyzer": "analyzer",
            "end": END
        }
    )
    
    builder.add_conditional_edges(
        "analyzer",
        route_to_next_agent,
        {
            "summarizer": "summarizer",
            "end": END
        }
    )
    
    builder.add_conditional_edges(
        "summarizer",
        route_to_next_agent,
        {
            "end": END
        }
    )
    
    return builder.compile()

# Usage
if __name__ == "__main__":
    assistant = create_research_assistant()
    
    result = assistant.invoke({
        "query": "What are the latest developments in AI?",
        "messages": [],
        "research_results": [],
        "analysis": {},
        "final_summary": "",
        "status": "researching"
    })
    
    print(result["final_summary"])
```

**High-Level Architecture Diagram:**

```
                    User Query
                    "Research AI developments"
                         │
                         ▼
              ┌──────────────────────┐
              │   Research State     │
              │  (Shared Context)    │
              └──────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │     Conditional Router         │
        └────────────────────────────────┘
              │        │        │
              ▼        ▼        ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │Researcher│ │ Analyzer │ │Summarizer│
    │  Agent   │ │  Agent   │ │  Agent   │
    └──────────┘ └──────────┘ └──────────┘
         │            │            │
         │            │            │
         ▼            ▼            ▼
    Research      Analysis      Summary
    Results       Results       Report
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ Final Report │
              └──────────────┘
```

**Communication Flow:**

```
1. User Query → Research State
   ↓
2. Router → Researcher Agent
   - Searches for information
   - Updates state with research_results
   - Sets status = "analyzing"
   ↓
3. Router → Analyzer Agent
   - Analyzes research_results
   - Updates state with analysis
   - Sets status = "summarizing"
   ↓
4. Router → Summarizer Agent
   - Creates summary from analysis
   - Updates state with final_summary
   - Sets status = "complete"
   ↓
5. Router → END
   - Returns final_summary to user
```

**Enhanced Version with Message Passing:**

```python
class EnhancedResearchState(TypedDict):
    query: str
    messages: Annotated[list[AnyMessage], add_messages]
    research_results: List[Dict]
    analysis: Dict
    final_summary: str
    status: str

def researcher_with_messaging(state: EnhancedResearchState):
    """Researcher that communicates via messages"""
    query = state["query"]
    
    # Do research
    results = perform_research(query)
    
    # Send message to next agent
    message = AIMessage(
        content=f"Research complete. Found {len(results)} sources. "
                f"Key topics: {extract_topics(results)}"
    )
    
    return {
        "research_results": results,
        "status": "analyzing",
        "messages": [message]
    }

def analyzer_with_messaging(state: EnhancedResearchState):
    """Analyzer that reads researcher's message and responds"""
    # Read researcher's message
    researcher_msg = [m for m in state["messages"] 
                     if "Research complete" in m.content][0]
    
    # Analyze based on message and results
    analysis = analyze_results(state["research_results"])
    
    # Send message to summarizer
    message = AIMessage(
        content=f"Analysis complete. {len(analysis['key_findings'])} key findings identified. "
                f"Ready for summarization."
    )
    
    return {
        "analysis": analysis,
        "status": "summarizing",
        "messages": [message]
    }
```

**Key Design Principles:**

1. **Shared State**: All agents read/write to same state
2. **Sequential Processing**: Agents execute in order (research → analyze → summarize)
3. **Status-Based Routing**: Router checks status to determine next agent
4. **Message Passing**: Agents communicate via messages in state
5. **Isolation**: Each agent has specific responsibility

This design enables specialized agents to collaborate effectively, with clear separation of concerns and coordinated execution.

---

*End of Part 2 (Questions 5-7). Continue with Part 3 for Questions 8-10...*

# GenAI Advanced Exam - Questions and Detailed Answers (Part 3: Q8-Q10)

---

## Question 8: Offline Models & Fine-Tuning Fundamentals (20 points)

**Scenario**: You want to fine-tune a model for your specific domain without sending data to external APIs.

### Part A (10 points)
Compare fine-tuning with OpenAI vs fine-tuning with Ollama (local). Include cost analysis, privacy considerations, iteration speed, and customization capabilities. Show a cost comparison table for training 10M tokens.

### Part B (10 points)
Explain LoRA (Low-Rank Adaptation) fine-tuning. Why is it preferred over full fine-tuning? What are the key parameters (lora_r, lora_alpha, learning_rate, num_epochs) and how do you choose appropriate values?

---

### **ANSWER TO QUESTION 8**

#### **Part A: OpenAI vs Ollama Fine-Tuning Comparison**

**Comprehensive Comparison:**

| Aspect | OpenAI Fine-Tuning | Ollama Fine-Tuning |
|--------|-------------------|-------------------|
| **Cost (Training)** | $8-12 per 1M tokens | $0 (electricity only, ~$0.10-0.50 per run) |
| **Cost (Usage)** | Pay per API call | $0 after training |
| **Privacy** | Data sent to OpenAI servers | 100% local, private |
| **Iteration Speed** | Hours to days | Minutes to hours |
| **Customization** | Limited to OpenAI's process | Full control |
| **Model Access** | Via API only | Full model ownership |
| **Experimentation** | Expensive per attempt | Free to experiment |
| **Hardware** | No hardware needed | Requires local GPU/CPU |
| **Setup Complexity** | Simple (API calls) | Moderate (local setup) |
| **Scalability** | Handled by OpenAI | Limited by your hardware |

**Cost Analysis for 10M Tokens:**

**OpenAI Fine-Tuning:**
```
Training Cost:
- 10M tokens × $10 per 1M tokens = $100
- Plus: API usage costs after training
- Example: 1M API calls/month × $0.002 = $2,000/month
- Annual usage: $24,000/year
- Total Year 1: $100 + $24,000 = $24,100
```

**Ollama Fine-Tuning:**
```
Training Cost:
- Electricity: ~$0.50 per training run
- Hardware: One-time (if you don't have GPU)
  - GPU: $500-2000 (one-time)
  - Or use cloud GPU: $0.50-2.00/hour during training
- Usage: $0 after training
- Total Year 1: $0.50 + (hardware if needed)
```

**Cost Comparison Table (10M Tokens Training):**

| Cost Component | OpenAI | Ollama |
|---------------|--------|--------|
| **Training (10M tokens)** | $100 | $0.50 |
| **Hardware (one-time)** | $0 | $500-2000 (optional) |
| **Usage (1M calls/month)** | $24,000/year | $0 |
| **Total Year 1** | $24,100 | $500-2000 (one-time) |
| **Total Year 2** | $24,000 | $0 |
| **5-Year Total** | $120,100 | $500-2000 |

**Break-Even Analysis:**
- If you make < 500 API calls/month: OpenAI is cheaper
- If you make > 500 API calls/month: Ollama pays for itself in 1-4 months

**Privacy Considerations:**

**OpenAI:**
- ❌ Training data sent to OpenAI servers
- ❌ Model hosted on OpenAI infrastructure
- ❌ Data subject to OpenAI's privacy policy
- ❌ May not meet compliance requirements (HIPAA, GDPR for sensitive data)

**Ollama:**
- ✅ All data stays local
- ✅ Complete data privacy
- ✅ Meets compliance requirements
- ✅ No data leaves your infrastructure

**Iteration Speed:**

**OpenAI:**
- Training: 2-24 hours (queue dependent)
- Iteration: Must wait for training to complete
- Experimentation: Expensive (each attempt costs money)

**Ollama:**
- Training: 30 minutes - 2 hours (depending on hardware)
- Iteration: Can start immediately after previous run
- Experimentation: Free (only electricity cost)

**Customization Capabilities:**

**OpenAI:**
- Limited to OpenAI's fine-tuning process
- Can't modify training algorithm
- Can't adjust hyperparameters extensively
- Must use OpenAI's infrastructure

**Ollama:**
- Full control over training process
- Can modify any hyperparameter
- Can use different base models
- Can experiment with different techniques
- Can combine multiple adapters

**When to Choose Each:**

**Choose OpenAI when:**
- ✅ No hardware available
- ✅ Low usage volume (< 500 calls/month)
- ✅ Need quick setup
- ✅ Privacy not critical
- ✅ Don't want to manage infrastructure

**Choose Ollama when:**
- ✅ High usage volume (> 500 calls/month)
- ✅ Privacy is critical
- ✅ Want full control
- ✅ Have hardware available
- ✅ Need to experiment frequently
- ✅ Compliance requirements

#### **Part B: LoRA (Low-Rank Adaptation) Explained**

**What is LoRA?**

LoRA (Low-Rank Adaptation) is an efficient fine-tuning technique that:
- Trains only a small subset of model parameters
- Uses low-rank matrices to approximate weight updates
- Reduces memory and computational requirements
- Maintains most of the performance of full fine-tuning

**How LoRA Works:**

**Traditional Full Fine-Tuning:**
```
Original Weights: W (7B parameters)
Updated Weights: W' (7B parameters)
Memory: 14B parameters during training
Time: Hours to days
```

**LoRA Fine-Tuning:**
```
Original Weights: W (7B parameters) - FROZEN
LoRA Adapter: A × B (small matrices)
  - A: rank × hidden_size
  - B: hidden_size × rank
  - rank (r) = 8-32 (much smaller)
  
Updated Weights: W + (A × B)
Memory: 7B + (r × hidden_size × 2) parameters
Time: 30 minutes - 2 hours
```

**Mathematical Representation:**

```
W' = W + ΔW
where ΔW = A × B

A: [rank × hidden_size] matrix
B: [hidden_size × rank] matrix

Example:
- Original: 7B parameters
- LoRA rank (r) = 16
- Hidden size = 4096
- LoRA parameters = 16 × 4096 × 2 = 131,072 parameters
- Reduction: 7B → 131K (99.998% reduction!)
```

**Why LoRA is Preferred:**

| Aspect | Full Fine-Tuning | LoRA |
|--------|-----------------|------|
| **Parameters Trained** | All (7B) | Small subset (131K) |
| **Memory Required** | 14-28GB VRAM | 8-16GB VRAM |
| **Training Time** | Hours to days | 30 min - 2 hours |
| **Storage** | Full model (14GB) | Adapter only (50MB) |
| **Performance** | 100% | 95-99% of full fine-tuning |
| **Multiple Adapters** | No (one model) | Yes (multiple adapters) |

**Key Advantages:**
1. **10-100x faster** training
2. **50-75% less memory** required
3. **Multiple adapters** can be combined
4. **Easy to switch** between adapters
5. **Small storage** (adapter is tiny)

**Key LoRA Parameters:**

**1. lora_r (Rank)**
- **What it is**: Dimension of the low-rank matrices
- **Range**: Typically 8-32
- **Impact**: 
  - Higher r = more capacity, more parameters, longer training
  - Lower r = less capacity, fewer parameters, faster training
- **Choosing value**:
  - Start with r=16 (good balance)
  - Simple tasks: r=8
  - Complex tasks: r=32
  - Very complex: r=64 (rarely needed)

```python
# Example
lora_r = 16  # Good default
# For simple task: lora_r = 8
# For complex task: lora_r = 32
```

**2. lora_alpha**
- **What it is**: Scaling factor for LoRA weights
- **Range**: Typically 2× to 4× lora_r
- **Impact**: Controls how much LoRA affects original weights
- **Choosing value**:
  - Usually: lora_alpha = 2 × lora_r
  - If r=16, then alpha=32
  - Higher alpha = stronger LoRA influence

```python
# Example
lora_r = 16
lora_alpha = 32  # 2 × lora_r (standard)
```

**3. learning_rate**
- **What it is**: How fast the model learns
- **Range**: 1e-5 to 5e-4
- **Impact**: 
  - Too high = unstable training, poor results
  - Too low = slow training, may not converge
- **Choosing value**:
  - Start with: 2e-4 (good default)
  - Small dataset: 1e-4
  - Large dataset: 3e-4 to 5e-4
  - Fine-tune based on loss curves

```python
# Example
learning_rate = 2e-4  # Good default (0.0002)
# Adjust based on training:
# - Loss not decreasing: try higher (3e-4)
# - Loss unstable: try lower (1e-4)
```

**4. num_epochs**
- **What it is**: Number of times to iterate through dataset
- **Range**: 1-10 (typically 3-5)
- **Impact**:
  - Too few = underfitting
  - Too many = overfitting
- **Choosing value**:
  - Start with: 3 epochs
  - Small dataset (< 1000 examples): 5-10 epochs
  - Large dataset (> 10000 examples): 1-3 epochs
  - Monitor validation loss to stop early

```python
# Example
num_epochs = 3  # Good default
# Small dataset: num_epochs = 5
# Large dataset: num_epochs = 1-2
```

**Complete Parameter Selection Guide:**

```python
# Scenario 1: Simple task, small dataset
config = {
    "lora_r": 8,
    "lora_alpha": 16,
    "learning_rate": 1e-4,
    "num_epochs": 5
}

# Scenario 2: Medium complexity, medium dataset (RECOMMENDED STARTING POINT)
config = {
    "lora_r": 16,
    "lora_alpha": 32,
    "learning_rate": 2e-4,
    "num_epochs": 3
}

# Scenario 3: Complex task, large dataset
config = {
    "lora_r": 32,
    "lora_alpha": 64,
    "learning_rate": 3e-4,
    "num_epochs": 2
}
```

**Training Process with LoRA:**

```python
from transformers import AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model

# Load base model
model = AutoModelForCausalLM.from_pretrained("llama3.2")

# Configure LoRA
lora_config = LoraConfig(
    r=16,                    # Rank
    lora_alpha=32,           # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.05,       # Dropout for LoRA layers
    bias="none",             # Don't train bias
    task_type="CAUSAL_LM"
)

# Apply LoRA to model
model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-4,       # Learning rate
    num_train_epochs=3,      # Number of epochs
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)
trainer.train()
```

**Monitoring and Adjusting:**

**Loss Curves:**
- **Good**: Loss decreases steadily, plateaus
- **Overfitting**: Training loss decreases, validation loss increases
- **Underfitting**: Both losses plateau at high value
- **Unstable**: Loss jumps around

**Adjustments:**
```python
# If overfitting:
num_epochs = 2  # Reduce epochs
lora_dropout = 0.1  # Increase dropout

# If underfitting:
num_epochs = 5  # Increase epochs
learning_rate = 3e-4  # Increase learning rate
lora_r = 32  # Increase rank

# If unstable:
learning_rate = 1e-4  # Decrease learning rate
```

**Why LoRA > Full Fine-Tuning:**

1. **Efficiency**: 10-100x faster training
2. **Resource**: Works on consumer GPUs (8GB VRAM)
3. **Flexibility**: Can combine multiple adapters
4. **Storage**: Adapter is 50MB vs 14GB for full model
5. **Performance**: 95-99% of full fine-tuning quality

**Example: Training Time Comparison**

```
Full Fine-Tuning:
- 7B model, 10K examples
- Time: 8-12 hours
- Memory: 24GB VRAM

LoRA Fine-Tuning:
- Same model, same examples
- Time: 1-2 hours
- Memory: 12GB VRAM
- Performance: 97% of full fine-tuning
```

LoRA is the preferred method for most fine-tuning tasks because it provides nearly the same performance with dramatically reduced resources and time.

---

## Question 9: Fine-Tuning Workflow & Dataset Preparation (15 points)

**Scenario**: You have a collection of customer support Q&A pairs and want to fine-tune a model to better handle your domain.

### Part A (8 points)
Describe the complete fine-tuning workflow from data preparation to deployment. Include:
- Dataset format requirements
- Data quality considerations
- Training process
- Model conversion to Ollama format
- Deployment steps

### Part B (7 points)
You have 500 Q&A pairs. Is this sufficient? What dataset size would you recommend for:
- Simple task adaptation
- Domain-specific knowledge
- Production system

Explain your reasoning and expected improvement percentages.

---

### **ANSWER TO QUESTION 9**

#### **Part A: Complete Fine-Tuning Workflow**

**Step 1: Dataset Format Requirements**

**Format 1: Instruction-Input-Output (Recommended)**
```json
[
  {
    "instruction": "Answer this customer support question",
    "input": "How do I reset my password?",
    "output": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and you'll receive a reset link within 5 minutes."
  },
  {
    "instruction": "Answer this customer support question",
    "input": "What are your business hours?",
    "output": "Our business hours are Monday-Friday 9am-5pm EST, and Saturday 10am-2pm EST. We're closed on Sundays."
  }
]
```

**Format 2: Chat Format (Alternative)**
```json
[
  {
    "messages": [
      {"role": "system", "content": "You are a helpful customer support agent."},
      {"role": "user", "content": "How do I reset my password?"},
      {"role": "assistant", "content": "To reset your password, go to the login page..."}
    ]
  }
]
```

**Step 2: Data Quality Considerations**

**Quality Checklist:**
1. **Diversity**: Cover various question types and scenarios
2. **Accuracy**: Answers must be correct and complete
3. **Consistency**: Maintain consistent style and format
4. **Completeness**: Include edge cases and difficult questions
5. **Balance**: Mix of simple and complex questions

**Data Cleaning:**
```python
def clean_dataset(data):
    cleaned = []
    for item in data:
        # Remove empty entries
        if not item.get("input") or not item.get("output"):
            continue
        
        # Normalize whitespace
        item["input"] = " ".join(item["input"].split())
        item["output"] = " ".join(item["output"].split())
        
        # Remove very short or very long entries
        if len(item["input"]) < 10 or len(item["output"]) < 20:
            continue
        if len(item["input"]) > 1000 or len(item["output"]) > 2000:
            continue
        
        cleaned.append(item)
    return cleaned
```

**Step 3: Dataset Preparation Script**

```python
import json
from datasets import Dataset

def prepare_dataset(input_file: str, output_file: str):
    """Prepare dataset for fine-tuning"""
    
    # Load raw data
    with open(input_file, 'r') as f:
        raw_data = json.load(f)
    
    # Clean data
    cleaned_data = clean_dataset(raw_data)
    
    # Split into train/validation (90/10)
    split_idx = int(len(cleaned_data) * 0.9)
    train_data = cleaned_data[:split_idx]
    val_data = cleaned_data[split_idx:]
    
    # Convert to HuggingFace Dataset format
    train_dataset = Dataset.from_list(train_data)
    val_dataset = Dataset.from_list(val_data)
    
    # Save
    train_dataset.save_to_disk(f"{output_file}_train")
    val_dataset.save_to_disk(f"{output_file}_val")
    
    print(f"Training examples: {len(train_data)}")
    print(f"Validation examples: {len(val_data)}")
    
    return train_dataset, val_dataset
```

**Step 4: Training Process**

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model
from datasets import load_from_disk

# Load base model
model_name = "llama3.2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Load datasets
train_dataset = load_from_disk("dataset_train")
val_dataset = load_from_disk("dataset_val")

# Tokenize datasets
def tokenize_function(examples):
    # Format: instruction + input + output
    texts = [
        f"Instruction: {inst}\nInput: {inp}\nOutput: {out}"
        for inst, inp, out in zip(
            examples["instruction"],
            examples["input"],
            examples["output"]
        )
    ]
    return tokenizer(texts, truncation=True, max_length=512)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    learning_rate=2e-4,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss"
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# Train
print("Starting training...")
trainer.train()

# Save model
trainer.save_model("./fine-tuned-model")
print("Training complete!")
```

**Step 5: Model Conversion to Ollama Format**

```python
import os
import shutil

def convert_to_ollama(model_path: str, model_name: str):
    """Convert fine-tuned model to Ollama format"""
    
    # Create Ollama model directory
    ollama_dir = f"./ollama-{model_name}"
    os.makedirs(ollama_dir, exist_ok=True)
    
    # Copy model files
    shutil.copytree(
        f"{model_path}/adapter_model.bin",
        f"{ollama_dir}/adapter_model.bin"
    )
    
    # Create Modelfile
    modelfile_content = f"""
FROM {model_path}

# Fine-tuned model for customer support
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM \"\"\"
You are a helpful customer support agent trained on our company's support data.
You provide accurate, friendly, and helpful responses to customer inquiries.
\"\"\"
"""
    
    with open(f"{ollama_dir}/Modelfile", "w") as f:
        f.write(modelfile_content)
    
    print(f"Model converted to Ollama format in {ollama_dir}")
    return ollama_dir
```

**Step 6: Deployment Steps**

```bash
# Step 1: Create model in Ollama
ollama create my-support-model -f ./ollama-model/Modelfile

# Step 2: Test the model
ollama run my-support-model "How do I reset my password?"

# Step 3: Integrate with application
# Update your code to use Ollama instead of OpenAI
```

**Integration Example:**
```python
# Before (OpenAI)
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "How do I reset my password?"}]
)

# After (Ollama)
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Not used, but required
)
response = client.chat.completions.create(
    model="my-support-model",  # Your fine-tuned model
    messages=[{"role": "user", "content": "How do I reset my password?"}]
)
# Same API, different model!
```

**Complete Workflow Summary:**

```
1. Collect Data → 2. Clean & Format → 3. Split Train/Val
        ↓
4. Configure LoRA → 5. Train Model → 6. Evaluate
        ↓
7. Convert to Ollama → 8. Deploy → 9. Test → 10. Integrate
```

#### **Part B: Dataset Size Recommendations**

**Is 500 Q&A Pairs Sufficient?**

**Short Answer**: It depends on the complexity, but 500 is a good starting point for simple tasks.

**Detailed Analysis:**

**For Simple Task Adaptation:**
- **Minimum**: 50-100 examples
- **Recommended**: 200-500 examples
- **500 pairs**: ✅ **SUFFICIENT**
- **Expected Improvement**: 30-50% better accuracy
- **Reasoning**: Simple tasks (like FAQ responses) don't need much data. The model mainly needs to learn your specific format and style.

**For Domain-Specific Knowledge:**
- **Minimum**: 200-500 examples
- **Recommended**: 1,000-5,000 examples
- **500 pairs**: ⚠️ **BORDERLINE** (may work, but more is better)
- **Expected Improvement**: 40-60% better accuracy
- **Reasoning**: Domain knowledge requires more examples to cover terminology, concepts, and edge cases. 500 might work but 1,000+ is better.

**For Production System:**
- **Minimum**: 1,000 examples
- **Recommended**: 10,000+ examples
- **500 pairs**: ❌ **INSUFFICIENT**
- **Expected Improvement**: 50-70% better accuracy
- **Reasoning**: Production systems need comprehensive coverage, edge cases, and high quality. 500 is too small for reliable production use.

**Dataset Size Guidelines Table:**

| Use Case | Minimum | Recommended | 500 Pairs? | Expected Improvement |
|----------|---------|------------|------------|---------------------|
| **Simple Task** | 50-100 | 200-500 | ✅ Sufficient | 30-50% |
| **Domain Knowledge** | 200-500 | 1,000-5,000 | ⚠️ Borderline | 40-60% |
| **Production** | 1,000 | 10,000+ | ❌ Insufficient | 50-70% |
| **Complex Reasoning** | 500-1,000 | 5,000-10,000 | ⚠️ Borderline | 40-60% |

**Improvement Expectations:**

**With 500 Examples:**
- **Simple tasks**: 30-50% improvement
  - Example: FAQ responses, basic Q&A
  - Model learns your style and common questions
  
- **Domain knowledge**: 20-40% improvement
  - Example: Technical support, industry-specific
  - May miss edge cases and advanced topics

- **Production**: Not recommended
  - Insufficient coverage
  - May have gaps in knowledge
  - Risk of poor performance on unseen questions

**With 1,000 Examples:**
- **Simple tasks**: 50-60% improvement
- **Domain knowledge**: 40-50% improvement
- **Production**: 30-40% improvement (minimum viable)

**With 10,000 Examples:**
- **Simple tasks**: 60-70% improvement
- **Domain knowledge**: 50-70% improvement
- **Production**: 50-70% improvement (production-ready)

**Quality vs Quantity:**

**500 High-Quality Examples > 5,000 Low-Quality Examples**

**High Quality Means:**
- Accurate answers
- Diverse question types
- Edge cases included
- Consistent formatting
- Complete coverage of topics

**Recommendation for 500 Pairs:**

**If you have 500 pairs:**
1. ✅ **Start with it** - It's enough to begin
2. ✅ **Test and evaluate** - See how well it performs
3. ✅ **Identify gaps** - Find what's missing
4. ✅ **Iterate** - Add more examples based on gaps
5. ⚠️ **Don't deploy to production yet** - Get to 1,000+ first

**Expansion Strategy:**
```python
# Phase 1: Start with 500 (proof of concept)
train_500_examples()
evaluate()
# Expected: 30-40% improvement

# Phase 2: Expand to 1,000 (minimum viable)
add_500_more_examples()  # Focus on gaps
train_1000_examples()
evaluate()
# Expected: 40-50% improvement

# Phase 3: Expand to 5,000 (production-ready)
add_4000_more_examples()  # Comprehensive coverage
train_5000_examples()
evaluate()
# Expected: 50-70% improvement
```

**Data Collection Strategy:**

1. **Start with existing data** (500 pairs)
2. **Identify common questions** from support tickets
3. **Add edge cases** that current model struggles with
4. **Include difficult questions** that require expertise
5. **Cover all product areas** evenly
6. **Add negative examples** (what NOT to do)

**Expected Timeline:**

```
500 examples → Train → Test → 2-4 weeks
    ↓
Identify gaps → Collect more data → 2-4 weeks
    ↓
1,000 examples → Train → Test → 2-4 weeks
    ↓
Production ready → Deploy
```

**Conclusion:**

500 Q&A pairs is **sufficient for starting** and **proof of concept**, but you should plan to expand to **1,000+ for production**. The key is to start with 500, evaluate, identify gaps, and iteratively improve.

---

## Question 10: Complete System Design Challenge (35 points)

**Design a "Smart Business Assistant" that:**

- Uses AI agents with LangGraph for multi-step reasoning
- Integrates with business systems via MCP servers
- Maintains conversation context across sessions
- Can be fine-tuned on company-specific data

**Your design should include:**

1. **Architecture Overview (10 points)**
2. **MCP Integration (8 points)**
3. **LangGraph Agent Design (8 points)**
4. **Fine-Tuning Strategy (5 points)**
5. **Production Considerations (4 points)**

---

### **ANSWER TO QUESTION 10**

#### **1. Architecture Overview (10 points)**

**Complete System Architecture:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  (Web App, Mobile App, Chat Interface)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   API GATEWAY / BACKEND                          │
│  - Authentication                                              │
│  - Request routing                                              │
│  - Session management                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              LANGGRAPH AGENT ORCHESTRATION LAYER                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  State Management (TypedDict)                            │  │
│  │  - Messages (conversation history)                       │  │
│  │  - User context                                          │  │
│  │  - Session metadata                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Agent Nodes                                             │  │
│  │  - Reasoning node (LLM)                                   │  │
│  │  - Tool calling node                                     │  │
│  │  - Memory management node                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Checkpointing (SQLiteSaver)                             │  │
│  │  - Thread-based session persistence                      │  │
│  │  - Conversation history                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP INTEGRATION LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Billing MCP  │  │   CRM MCP    │  │ Inventory MCP│         │
│  │   Server     │  │   Server     │  │   Server     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│                  MCP Client Manager                             │
│                  (Connection pooling)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS SYSTEMS LAYER                        │
│  - Billing System (Database)                                     │
│  - CRM System (Database)                                         │
│  - Inventory System (Database)                                   │
│  - Other business applications                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINE-TUNED MODEL LAYER                        │
│  - Base Model: Llama 3.2                                        │
│  - Fine-tuned on company data                                   │
│  - Deployed via Ollama                                           │
│  - Domain-specific knowledge                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Component Interactions:**

```
User Query
    ↓
API Gateway (authenticates, routes)
    ↓
LangGraph Agent (reasons about query)
    ↓
Agent decides: "I need to check billing"
    ↓
MCP Client → Billing MCP Server
    ↓
Billing MCP Server → Billing Database
    ↓
Results flow back through MCP → Agent
    ↓
Agent synthesizes response using fine-tuned model
    ↓
Response sent to user
    ↓
State checkpointed for next interaction
```

**Data Flow:**

1. **User Input** → API Gateway
2. **API Gateway** → LangGraph Agent (with user context)
3. **Agent Reasons** → Determines needed tools
4. **Agent Calls** → MCP Client Manager
5. **MCP Client** → Appropriate MCP Server (billing/CRM/inventory)
6. **MCP Server** → Business System (database/API)
7. **Results** → MCP Server → MCP Client → Agent
8. **Agent Synthesizes** → Fine-tuned LLM generates response
9. **Response** → Checkpointed → Returned to user

#### **2. MCP Integration (8 points)**

**MCP Server Design:**

**Server 1: Billing MCP Server**

```typescript
// servers/billing/src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "billing-mcp-server",
  version: "1.0.0"
});

// Tool 1: Get Invoice
server.registerTool("billing.get_invoice", {
  description: "Retrieve invoice details by ID",
  inputSchema: {
    invoice_id: z.string().describe("Invoice ID")
  }
}, async ({ invoice_id }) => {
  const invoice = await billingDB.getInvoice(invoice_id);
  return { content: [{ type: "text", text: JSON.stringify(invoice) }] };
});

// Tool 2: Create Invoice
server.registerTool("billing.create_invoice", {
  description: "Create a new invoice",
  inputSchema: {
    amount: z.number().min(0),
    currency: z.string().length(3),
    customer_email: z.string().email(),
    idempotency_key: z.string()
  }
}, async (params) => {
  const invoice = await billingDB.createInvoice(params);
  return { content: [{ type: "text", text: JSON.stringify(invoice) }] };
});

// Tool 3: List Invoices
server.registerTool("billing.list_invoices", {
  description: "List invoices with optional filters",
  inputSchema: {
    customer_email: z.string().email().optional(),
    status: z.enum(["draft", "sent", "paid"]).optional(),
    limit: z.number().max(100).optional()
  }
}, async (params) => {
  const invoices = await billingDB.listInvoices(params);
  return { content: [{ type: "text", text: JSON.stringify(invoices) }] };
});
```

**Server 2: CRM MCP Server**

```typescript
// servers/crm/src/index.ts
const crmServer = new McpServer({
  name: "crm-mcp-server",
  version: "1.0.0"
});

// Tool 1: Get Customer
crmServer.registerTool("crm.get_customer", {
  description: "Get customer information by email or ID",
  inputSchema: {
    customer_id: z.string().optional(),
    email: z.string().email().optional()
  }
}, async (params) => {
  const customer = await crmDB.getCustomer(params);
  return { content: [{ type: "text", text: JSON.stringify(customer) }] };
});

// Tool 2: Update Customer
crmServer.registerTool("crm.update_customer", {
  description: "Update customer information",
  inputSchema: {
    customer_id: z.string(),
    updates: z.object({
      name: z.string().optional(),
      email: z.string().email().optional(),
      phone: z.string().optional()
    })
  }
}, async ({ customer_id, updates }) => {
  const customer = await crmDB.updateCustomer(customer_id, updates);
  return { content: [{ type: "text", text: JSON.stringify(customer) }] };
});
```

**MCP Client Manager:**

```typescript
// backend/src/mcpClientManager.ts
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

class MCPClientManager {
  private clients: Map<string, Client> = new Map();
  
  async getClient(serverName: string): Promise<Client> {
    if (this.clients.has(serverName)) {
      return this.clients.get(serverName)!;
    }
    
    const transport = new StdioClientTransport({
      command: "node",
      args: ["dist/index.js"],
      cwd: `../servers/${serverName}`
    });
    
    const client = new Client({
      name: `backend-${serverName}-client`,
      version: "1.0.0"
    });
    
    await client.connect(transport);
    this.clients.set(serverName, client);
    return client;
  }
  
  async callTool(serverName: string, toolName: string, args: any) {
    const client = await this.getClient(serverName);
    return await client.request({
      method: "tools/call",
      params: { name: toolName, arguments: args }
    });
  }
}

export const mcpManager = new MCPClientManager();
```

**Transport Method Selection:**

- **stdio**: Used for local MCP servers (billing, CRM, inventory)
- **Reason**: Fast, simple, no network overhead for local services
- **Alternative**: HTTP for remote servers if needed

#### **3. LangGraph Agent Design (8 points)**

**State Schema:**

```python
from typing_extensions import TypedDict
from typing import Annotated, Optional, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class BusinessAssistantState(TypedDict):
    # Conversation history
    messages: Annotated[list[AnyMessage], add_messages]
    
    # User context
    user_id: str
    user_email: Optional[str]
    user_role: Optional[str]  # "admin", "customer", "employee"
    
    # Current task context
    current_task: Optional[str]
    task_history: list[Dict[str, Any]]
    
    # MCP tool results cache
    tool_results: Dict[str, Any]
    
    # Session metadata
    session_id: str
    start_time: str
    priority: str  # "low", "medium", "high"
```

**Node Structure:**

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Initialize fine-tuned model (via Ollama)
model = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="company-assistant-model"  # Fine-tuned model
)

# Define tools (MCP tool calls)
tools = [
    "billing.get_invoice",
    "billing.create_invoice",
    "crm.get_customer",
    "crm.update_customer"
]

model_with_tools = model.bind_tools(tools)

def reasoning_node(state: BusinessAssistantState):
    """Main reasoning node using fine-tuned model"""
    # Get user context
    user_context = f"User: {state.get('user_email', 'unknown')}, Role: {state.get('user_role', 'customer')}"
    
    # Build context-aware prompt
    system_message = SystemMessage(content=f"""
    You are a helpful business assistant for our company.
    {user_context}
    Use available tools to help users with billing, CRM, and other business tasks.
    """)
    
    # Get response from fine-tuned model
    response = model_with_tools.invoke([system_message] + state["messages"])
    
    return {"messages": [response]}

def mcp_tool_node(state: BusinessAssistantState):
    """Execute MCP tool calls"""
    last_message = state["messages"][-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        results = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call['name']
            args = tool_call['args']
            
            # Parse tool name: "billing.get_invoice" -> server="billing", tool="get_invoice"
            server, tool = tool_name.split('.', 1)
            
            # Call MCP server
            result = await mcpManager.callTool(server, tool_name, args)
            results.append(result)
        
        # Create tool messages
        tool_messages = [
            ToolMessage(content=json.dumps(r), tool_call_id=tc['id'])
            for r, tc in zip(results, last_message.tool_calls)
        ]
        
        return {"messages": tool_messages}

def create_business_assistant():
    """Create the complete agent graph"""
    builder = StateGraph(BusinessAssistantState)
    
    # Add nodes
    builder.add_node("reasoning", reasoning_node)
    builder.add_node("tools", mcp_tool_node)
    
    # Add edges
    builder.add_edge(START, "reasoning")
    builder.add_conditional_edges(
        "reasoning",
        tools_condition,
        {
            "tools": "tools",
            "__end__": END
        }
    )
    builder.add_edge("tools", "reasoning")  # ReACT loop
    
    # Add checkpointing
    from langgraph.checkpoint.sqlite import SqliteSaver
    checkpointer = SqliteSaver.from_conn_string("assistant_sessions.db")
    
    return builder.compile(checkpointer=checkpointer)
```

**ReACT Pattern Implementation:**

- **Reasoning node**: Uses fine-tuned model to understand query and decide on tools
- **Tools node**: Calls MCP servers to get business data
- **Loop back**: Agent sees tool results and can reason further
- **Checkpointing**: Saves state after each step for session persistence

#### **4. Fine-Tuning Strategy (5 points)**

**Dataset Preparation:**

```python
# Collect company-specific data
training_data = [
    {
        "instruction": "Answer this business question",
        "input": "How do I create an invoice?",
        "output": "To create an invoice, I'll need the amount, currency, and customer email. Let me help you with that using our billing system."
    },
    {
        "instruction": "Answer this business question",
        "input": "What's the status of invoice INV-123?",
        "output": "I'll check the invoice status for you. Let me look that up in our billing system."
    },
    # ... 5,000+ examples covering:
    # - Common business questions
    # - Company-specific terminology
    # - Product/service knowledge
    # - Support procedures
]
```

**Fine-Tuning Configuration:**

```python
# Use LoRA for efficiency
lora_config = {
    "lora_r": 16,
    "lora_alpha": 32,
    "learning_rate": 2e-4,
    "num_epochs": 3,
    "base_model": "llama3.2"
}

# Expected improvements:
# - 50-70% better on company-specific questions
# - Understands company terminology
# - Matches company communication style
# - Better at multi-step business tasks
```

**Deployment:**

```bash
# Convert to Ollama
ollama create company-assistant-model -f Modelfile

# Deploy locally
ollama serve

# Use in application
# Model automatically used in reasoning_node
```

#### **5. Production Considerations (4 points)**

**Scalability:**

```python
# 1. Connection Pooling for MCP Clients
class MCPClientPool:
    def __init__(self, max_connections=10):
        self.pools = {}  # One pool per MCP server
        self.max_connections = max_connections
    
    async def get_client(self, server_name):
        # Reuse existing connections
        # Create new only if pool not full
        pass

# 2. Load Balancing for Agents
# Multiple agent instances behind load balancer
# Each handles different user sessions

# 3. Caching
# Cache frequent MCP tool results
# Cache LLM responses for common queries
```

**Error Handling:**

```python
def robust_reasoning_node(state: BusinessAssistantState):
    try:
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    except Exception as e:
        # Fallback to base model if fine-tuned fails
        fallback_model = ChatOpenAI(model="gpt-4o")
        response = fallback_model.invoke(state["messages"])
        return {
            "messages": [response],
            "error": str(e),
            "used_fallback": True
        }
```

**Monitoring:**

```python
# Track metrics:
# - Response times
# - Tool call success rates
# - User satisfaction
# - Error rates
# - Session lengths
# - Fine-tuned model performance vs base model
```

**Security:**

- Authentication at API Gateway
- User context isolation (thread IDs)
- MCP server access control
- Input validation
- Rate limiting

**Complete System Benefits:**

1. **Intelligent**: Fine-tuned model understands company domain
2. **Capable**: MCP integration enables real business actions
3. **Contextual**: Maintains conversation history across sessions
4. **Scalable**: Can handle multiple users concurrently
5. **Maintainable**: Modular architecture (MCP servers, agent, model)

This design provides a production-ready intelligent business assistant that combines the best of AI agents, MCP integration, LangGraph orchestration, and fine-tuned models.

---

## 📊 Grading Rubric Summary

| Question | Points | Key Concepts Tested |
|----------|--------|-------------------|
| Q1 | 20 | Agent Architecture, Agent Types |
| Q2 | 20 | ReACT Pattern, Tool Integration |
| Q3 | 25 | MCP Architecture, Tool Design, Transport |
| Q4 | 20 | LangGraph State, TypedDict, Reducers |
| Q5 | 15 | Nodes, Edges, Conditional Routing |
| Q6 | 15 | Checkpointing, Memory, Thread IDs |
| Q7 | 15 | Multi-Agent Systems, Coordination |
| Q8 | 20 | Fine-Tuning, LoRA, Cost Analysis |
| Q9 | 15 | Fine-Tuning Workflow, Dataset Prep |
| Q10 | 35 | Complete System Design |
| **Total** | **200** | **Comprehensive Coverage** |

---

## ⏱️ Time Management Guide for Students

**Total Time**: 3 hours (180 minutes)

**Recommended Allocation:**
- Q1-Q3 (Shorter answers): 45 minutes
- Q4-Q7 (Design questions): 60 minutes  
- Q8-Q9 (Analysis): 30 minutes
- Q10 (Comprehensive): 30 minutes
- Review: 15 minutes

---

**End of Advanced Exam - Questions and Detailed Answers**

*This exam comprehensively tests students' understanding of AI Agents, Model Context Protocol (MCP), LangGraph architecture, offline model fine-tuning, and practical implementation skills.*

