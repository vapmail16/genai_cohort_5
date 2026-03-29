# GenAI Interim Exam - Questions Only

## 📝 Exam Information

**Total Points**: 200  
**Time Allowed**: 3 hours  
**Topics Covered**: LLM Fundamentals, Vector Databases, RAG Systems, Prompt Engineering, LangChain, Document Processing

---

## Question 1: LLM Fundamentals & Vector Embeddings (20 points)

**Scenario**: You're building a semantic search system for a company's internal documents.

### Part A (10 points)
Explain the difference between BERT embeddings (768D) and OpenAI embeddings (1536D). When would you choose one over the other for your document search system? Consider factors like cost, privacy, and performance.

### Part B (10 points)
If you store 5 million document chunks using OpenAI embeddings (1536D), calculate the storage requirements. Show your work and explain any optimization strategies you would use to reduce storage costs.

---

## Question 2: Vector Database Architecture (20 points)

**Scenario**: You need to design a vector database system for an e-commerce product search with 10 million products.

### Part A (10 points)
Compare and contrast three indexing approaches: HNSW (graph-based), LSH (hash-based), and Product Quantization. Which would you choose for this use case and why?

### Part B (10 points)
Explain the "curse of dimensionality" and describe two practical strategies you would implement to mitigate it in your product search system.

---

## Question 3: Similarity Metrics Application (15 points)

For each scenario, choose the most appropriate similarity metric and explain why:

### Scenario A (5 points)
Recommending movies based on user preferences where users rate genres on a 1-5 scale, but some users rate many genres while others rate few.

### Scenario B (5 points)
Finding similar houses based on [price, square footage, bedrooms, bathrooms] where all features are equally important.

### Scenario C (5 points)
Matching job candidates to positions based on skill requirements [Python: 0.9, AWS: 0.7, SQL: 0.8] where high alignment in critical skills is more important than overall similarity.

---

## Question 4: RAG Architecture Design (25 points)

**Scenario**: You're building a medical information system that must provide highly accurate, verifiable answers about medications and treatments.

### Part A (10 points)
Choose the most appropriate RAG architecture from the 8 types and justify your choice. Explain why the other architectures would be less suitable.

### Part B (10 points)
Design the complete data flow diagram for your chosen architecture, showing all major components and how they interact.

### Part C (5 points)
What safety mechanisms would you implement to prevent medical hallucinations and ensure answer accuracy?

---

## Question 5: Prompt Engineering for Production (20 points)

**Scenario**: You're building a customer support chatbot that must maintain a professional tone, cite sources, and escalate complex issues.

### Part A (15 points)
Write a complete system prompt that includes:
- Role definition
- Constraints and guidelines
- Output format requirements
- Source citation requirements
- Escalation criteria

### Part B (5 points)
Demonstrate how you would use Chain-of-Thought prompting to help the chatbot handle a complex multi-step customer issue like "I was charged twice for an order I never received."

---

## Question 6: LangChain Application Development (20 points)

### Part A (10 points)
Explain the difference between LangChain's Memory types (ConversationBufferMemory, ConversationSummaryMemory, and ConversationBufferWindowMemory). When would you use each one?

### Part B (10 points)
Design a LangChain-based application that answers questions about a company's HR policies stored in PDF documents. List all components you would use and explain how they work together.

---

## Question 7: Document Chunking Strategies (15 points)

**Scenario**: You have a 500-page technical manual with sections, subsections, code snippets, and tables.

### Part A (8 points)
Compare three chunking strategies:
- Fixed-size chunking (512 tokens)
- Semantic chunking (by meaning)
- Hierarchical chunking (by document structure)

Explain the advantages and disadvantages of each for this technical manual.

### Part B (7 points)
Design a chunking strategy that preserves context while keeping chunks small enough for efficient retrieval. Include specific parameters.

---

## Question 8: RAG vs Traditional LLM (15 points)

**Compare and contrast these two approaches for a legal research system:**

**Approach A**: Fine-tune a large language model on legal documents

**Approach B**: Use RAG with a vector database of legal documents

Your answer should cover: Cost implications, update frequency, accuracy, source attribution, and scalability.

---

## Question 9: Vector Database Query Optimization (20 points)

**Scenario**: Your vector database search queries are taking 500ms on average, but you need to reduce this to under 100ms.

### Part A (10 points)
Describe 5 specific optimization techniques.

### Part B (10 points)
Explain KNN vs ANN trade-offs.

---

## Question 10: Real-World Integration Challenge (30 points)

**Design a "Smart Research Assistant" for university researchers that:**

- Searches across academic papers (PDF), research databases, and institutional repositories
- Handles multimodal content (text, equations, images, tables)
- Provides cited answers with source attribution
- Updates daily with new publications

**Your design should include:**
1. Complete technology stack selection (RAG architecture, vector database, embedding model, similarity metric)
2. Document processing pipeline for multimodal content
3. Retrieval strategy and query optimization
4. How you would handle frequent updates (new papers daily)
5. Expected performance metrics

---

## 📊 Grading Rubric Summary

| Question | Points | Key Concepts Tested |
|----------|--------|-------------------|
| Q1 | 20 | Embeddings, Storage, Optimization |
| Q2 | 20 | Indexing, Curse of Dimensionality |
| Q3 | 15 | Similarity Metrics Application |
| Q4 | 25 | RAG Architecture, Safety |
| Q5 | 20 | Prompt Engineering, CoT |
| Q6 | 20 | LangChain, Memory, Components |
| Q7 | 15 | Chunking Strategies |
| Q8 | 15 | RAG vs Fine-tuning |
| Q9 | 20 | Query Optimization |
| Q10 | 30 | Complete System Design |
| **Total** | **200** | **Comprehensive Coverage** |

---

*Good luck with your exam preparation!*

