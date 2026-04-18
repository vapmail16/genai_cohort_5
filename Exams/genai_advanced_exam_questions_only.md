# GenAI Advanced Exam - Questions Only

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

## Question 8: Offline Models & Fine-Tuning Fundamentals (20 points)

**Scenario**: You want to fine-tune a model for your specific domain without sending data to external APIs.

### Part A (10 points)
Compare fine-tuning with OpenAI vs fine-tuning with Ollama (local). Include cost analysis, privacy considerations, iteration speed, and customization capabilities. Show a cost comparison table for training 10M tokens.

### Part B (10 points)
Explain LoRA (Low-Rank Adaptation) fine-tuning. Why is it preferred over full fine-tuning? What are the key parameters (lora_r, lora_alpha, learning_rate, num_epochs) and how do you choose appropriate values?

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

## Question 10: Complete System Design Challenge (35 points)

**Design a "Smart Business Assistant" that:**

- Uses AI agents with LangGraph for multi-step reasoning
- Integrates with business systems via MCP servers
- Maintains conversation context across sessions
- Can be fine-tuned on company-specific data

**Your design should include:**

1. **Architecture Overview (10 points)**
   - Complete system architecture diagram
   - Component interactions
   - Data flow

2. **MCP Integration (8 points)**
   - Design MCP servers for at least 2 business domains (e.g., billing, CRM)
   - Tool definitions with schemas
   - Transport method selection and justification

3. **LangGraph Agent Design (8 points)**
   - State schema design
   - Node structure (reasoning, tool calling, memory)
   - ReACT pattern implementation
   - Checkpointing strategy

4. **Fine-Tuning Strategy (5 points)**
   - Dataset preparation approach
   - Fine-tuning method (LoRA vs full)
   - Expected improvements

5. **Production Considerations (4 points)**
   - Scalability approach
   - Error handling
   - Monitoring and observability

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

*Good luck with your exam preparation!*

