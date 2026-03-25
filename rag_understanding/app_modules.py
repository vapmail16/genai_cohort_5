import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import random

def show_rag_fundamentals():
    st.markdown('<h2 class="section-header">🔍 RAG Fundamentals</h2>', unsafe_allow_html=True)
    
    # Tabs for different fundamental concepts
    tab1, tab2, tab3, tab4 = st.tabs(["What is RAG?", "Core Components", "How RAG Works", "Interactive Demo"])
    
    with tab1:
        show_what_is_rag()
    
    with tab2:
        show_core_components()
    
    with tab3:
        show_how_rag_works()
    
    with tab4:
        show_interactive_demo()

def show_what_is_rag():
    st.markdown("""
    ### What is Retrieval-Augmented Generation (RAG)?
    
    **Simple Definition**: RAG is like giving an AI assistant access to a huge library of information 
    so it can look up facts and give you accurate, up-to-date answers instead of just relying on 
    what it learned during training.
    
    **Think of it as**: Imagine you're asking a smart friend a question, but instead of just using 
    their memory, they can also quickly look up information in books, articles, and databases to 
    give you the most accurate and current answer possible.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🚫 Problems with Regular AI (Without RAG):
        - **Outdated Information**: Like asking someone who only knows what happened before 2021 about current events
        - **Making Things Up**: Sometimes AI gives answers that sound right but are actually wrong
        - **Limited Knowledge**: Can't access your company's documents, recent news, or specialized databases
        - **No Proof**: Can't tell you where it got its information from
        """)
    
    with col2:
        st.markdown("""
        #### ✅ How RAG Fixes These Problems:
        - **Always Up-to-Date**: Can look up the latest information from the internet and databases
        - **Fact-Checked Answers**: Uses real documents and sources to give accurate answers
        - **Shows Sources**: Can tell you exactly where it found the information
        - **Access to Everything**: Can search through your company's documents, research papers, or any knowledge base
        - **Less Guessing**: Instead of making things up, it finds real information to base answers on
        """)

def show_core_components():
    st.markdown("### The 3 Main Parts of RAG Systems")
    
    st.markdown("""
    Think of a RAG system like a super-smart research assistant with three main jobs:
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        #### 🔍 1. The Information Finder (Retrieval Component)
        
        **What it does**: Searches through all available information to find the most relevant pieces for your question.
        
        **Where it looks**:
        - Your Documents (PDFs, Word docs, presentations)
        - Databases (Company records, product catalogs)
        - The Internet (News articles, websites, blogs)
        - Real-time Data (Stock prices, weather, live updates)
        
        **How it searches**:
        - Meaning Search: Understands what you're really asking
        - Keyword Search: Looks for exact words and phrases
        - Smart Combination: Uses both meaning and keywords
        """)
    
    with col2:
        st.markdown("""
        #### ✍️ 2. The Answer Writer (Generation Component)
        
        **What it does**: Takes all the information found and writes a clear, helpful answer to your question.
        
        **How it works**:
        - Puts It All Together: Combines your question with the found information
        - Writes Clearly: Creates a well-structured, easy-to-understand answer
        - Cites Sources: Tells you where each piece of information came from
        - Checks Quality: Makes sure the answer is accurate and relevant
        
        **Different ways it can answer**:
        - Simple Answer: Direct answer based on the information found
        - Comprehensive Answer: Combines information from multiple sources
        - Step-by-Step Answer: Breaks down complex topics
        """)
    
    with col3:
        st.markdown("""
        #### 📚 3. The Information Library (Knowledge Base)
        
        **What it is**: The organized collection of all the information the system can search through.
        
        **How information gets organized**:
        - Document Processing: Converts PDFs, Word docs, etc. into searchable text
        - Smart Chunking: Breaks long documents into smaller, manageable pieces
        - Creating Search Tags: Converts text into searchable "tags"
        - Building Indexes: Creates a searchable catalog of all information
        
        **Where information is stored**:
        - Vector Databases: Special databases for meaning-based search
        - Search Engines: Powerful search systems
        - Regular Databases: Standard databases for structured information
        """)

def show_how_rag_works():
    st.markdown("### How RAG Systems Work - Step by Step")
    
    # Create a flow diagram
    steps = [
        "1. User asks a question",
        "2. System converts question to searchable format",
        "3. System searches through knowledge base",
        "4. System finds relevant documents",
        "5. System combines question + documents",
        "6. AI generates answer with sources",
        "7. User gets accurate, cited answer"
    ]
    
    # Create a visual flow
    fig = go.Figure()
    
    # Add flow boxes
    for i, step in enumerate(steps):
        y_pos = len(steps) - i
        fig.add_trace(go.Scatter(
            x=[0.5],
            y=[y_pos],
            mode='markers+text',
            marker=dict(size=50, color='lightblue'),
            text=[f"<b>{step}</b>"],
            textposition="middle center",
            showlegend=False
        ))
        
        # Add arrows between steps
        if i < len(steps) - 1:
            fig.add_trace(go.Scatter(
                x=[0.5, 0.5],
                y=[y_pos - 0.3, y_pos - 0.7],
                mode='lines',
                line=dict(color='black', width=2),
                showlegend=False
            ))
    
    fig.update_layout(
        title="RAG System Flow",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed explanation
    st.markdown("""
    #### 📋 Detailed Process:
    
    **Step 1: User Query**
    - User asks: "What are the side effects of aspirin?"
    
    **Step 2: Query Processing**
    - System converts question to searchable format
    - Creates embeddings or keywords for search
    
    **Step 3: Knowledge Base Search**
    - Searches through medical databases, drug information, research papers
    - Finds documents about aspirin and side effects
    
    **Step 4: Document Retrieval**
    - Gets the most relevant documents
    - Ranks them by relevance and quality
    
    **Step 5: Context Assembly**
    - Combines the original question with retrieved documents
    - Creates a comprehensive context for the AI
    
    **Step 6: Response Generation**
    - AI generates answer based on the context
    - Ensures answer is accurate and well-structured
    
    **Step 7: Source Attribution**
    - Adds citations and sources to the answer
    - User can verify information independently
    """)

def show_interactive_demo():
    st.markdown("### 🎮 Interactive RAG Demo")
    
    st.markdown("Try asking different types of questions to see how RAG works:")
    
    # Sample questions
    sample_questions = [
        "What are the benefits of renewable energy?",
        "How do I reset my password?",
        "What's our company's vacation policy?",
        "What are the side effects of this medication?",
        "How do I submit an expense report?"
    ]
    
    selected_question = st.selectbox("Choose a sample question:", sample_questions)
    
    if st.button("Ask Question"):
        # Simulate RAG process
        st.markdown("#### 🔍 RAG Process Simulation")
        
        # Get appropriate data based on the selected question
        question_data = get_question_data(selected_question)
        
        # Step 1: Query processing
        with st.expander("Step 1: Query Processing", expanded=True):
            st.write(f"**Original Question**: {selected_question}")
            st.write("**Processing**: Converting to searchable format...")
            st.write(f"**Keywords**: {question_data['keywords']}")
            st.write("**Embedding**: [0.1, 0.8, 0.3, ...] (768-dimensional vector)")
        
        # Step 2: Document retrieval
        with st.expander("Step 2: Document Retrieval", expanded=True):
            st.write("**Searching knowledge base...**")
            
            # Simulate retrieved documents
            documents = question_data['documents']
            
            for i, doc in enumerate(documents, 1):
                st.write(f"**Document {i}**: {doc['title']} (Relevance: {doc['relevance']:.2f})")
                st.write(f"Content: {doc['content'][:100]}...")
                st.write("---")
        
        # Step 3: Response generation
        with st.expander("Step 3: Response Generation", expanded=True):
            st.write("**Combining question with retrieved documents...**")
            st.write("**Generating response...**")
            
            # Simulate response
            response = question_data['response']
            
            st.markdown(response)
        
        # Step 4: Source attribution
        with st.expander("Step 4: Source Attribution", expanded=True):
            st.write("**Sources used in this response:**")
            for i, doc in enumerate(documents, 1):
                st.write(f"- {doc['title']} (Relevance: {doc['relevance']:.2f})")
        
        st.success("✅ RAG process completed successfully!")

def get_question_data(question):
    """Get appropriate data based on the question type"""
    
    if "renewable energy" in question.lower():
        return {
            "keywords": "renewable, energy, benefits, solar, wind, sustainability",
            "documents": [
                {"title": "Renewable Energy Report 2023", "relevance": 0.95, "content": "Renewable energy sources like solar and wind provide clean, sustainable power that reduces our dependence on fossil fuels..."},
                {"title": "Environmental Benefits Study", "relevance": 0.87, "content": "Studies show renewable energy reduces carbon emissions by 40-60% compared to traditional energy sources..."},
                {"title": "Economic Impact Analysis", "relevance": 0.82, "content": "Renewable energy creates jobs and reduces long-term energy costs for consumers and businesses..."}
            ],
            "response": """**Answer**: Renewable energy offers several key benefits:

1. **Environmental Benefits**: Reduces carbon emissions by 40-60% compared to fossil fuels
2. **Economic Benefits**: Creates jobs and reduces long-term energy costs
3. **Sustainability**: Provides clean, sustainable power for future generations
4. **Energy Independence**: Reduces reliance on fossil fuel imports

**Sources**:
- Renewable Energy Report 2023
- Environmental Benefits Study
- Economic Impact Analysis"""
        }
    
    elif "password" in question.lower():
        return {
            "keywords": "password, reset, login, account, security, authentication",
            "documents": [
                {"title": "User Account Management Guide", "relevance": 0.96, "content": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and check your inbox for reset instructions..."},
                {"title": "Security Best Practices", "relevance": 0.89, "content": "When resetting your password, choose a strong password with at least 8 characters, including numbers and special characters..."},
                {"title": "Account Recovery Procedures", "relevance": 0.85, "content": "If you don't receive the reset email, check your spam folder or contact support for assistance with account recovery..."}
            ],
            "response": """**Answer**: To reset your password:

1. **Go to the login page** and click "Forgot Password"
2. **Enter your email address** associated with your account
3. **Check your inbox** for password reset instructions
4. **Follow the link** in the email to create a new password
5. **Choose a strong password** with at least 8 characters, including numbers and special characters

If you don't receive the email, check your spam folder or contact support for assistance.

**Sources**:
- User Account Management Guide
- Security Best Practices
- Account Recovery Procedures"""
        }
    
    elif "vacation policy" in question.lower():
        return {
            "keywords": "vacation, policy, time off, leave, holidays, PTO",
            "documents": [
                {"title": "Employee Handbook - Time Off Policy", "relevance": 0.94, "content": "Employees are entitled to 15 days of paid vacation per year, which increases to 20 days after 5 years of service..."},
                {"title": "Holiday Schedule 2024", "relevance": 0.87, "content": "Company observes 10 paid holidays per year including New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving, and Christmas..."},
                {"title": "Vacation Request Procedures", "relevance": 0.82, "content": "Vacation requests must be submitted at least 2 weeks in advance through the employee portal and require manager approval..."}
            ],
            "response": """**Answer**: Our company vacation policy includes:

1. **Paid Vacation**: 15 days per year (increases to 20 days after 5 years)
2. **Paid Holidays**: 10 company holidays per year
3. **Request Process**: Submit requests 2 weeks in advance through employee portal
4. **Manager Approval**: All vacation requests require manager approval
5. **Accrual**: Vacation time accrues monthly and can be carried over up to 5 days

For specific dates and procedures, refer to the Employee Handbook or contact HR.

**Sources**:
- Employee Handbook - Time Off Policy
- Holiday Schedule 2024
- Vacation Request Procedures"""
        }
    
    elif "medication" in question.lower() or "side effects" in question.lower():
        return {
            "keywords": "medication, side effects, drug, safety, warnings, adverse reactions",
            "documents": [
                {"title": "Medication Safety Guidelines", "relevance": 0.93, "content": "Common side effects may include nausea, dizziness, headache, and mild stomach upset. Contact your doctor if symptoms persist or worsen..."},
                {"title": "Drug Interaction Database", "relevance": 0.88, "content": "This medication may interact with certain foods, alcohol, or other medications. Consult your pharmacist about potential interactions..."},
                {"title": "Emergency Procedures", "relevance": 0.85, "content": "If you experience severe allergic reactions, difficulty breathing, or chest pain, seek immediate medical attention..."}
            ],
            "response": """**Answer**: **Important**: This is for educational purposes only. Always consult your healthcare provider.

Common side effects may include:
- Nausea and mild stomach upset
- Dizziness or headache
- Mild fatigue

**Seek immediate medical attention if you experience:**
- Severe allergic reactions
- Difficulty breathing
- Chest pain
- Severe dizziness or fainting

**Important reminders:**
- Take medication as prescribed
- Avoid alcohol unless approved by your doctor
- Inform your doctor of all other medications you're taking
- Keep all medical appointments for monitoring

**Sources**:
- Medication Safety Guidelines
- Drug Interaction Database
- Emergency Procedures"""
        }
    
    elif "expense report" in question.lower():
        return {
            "keywords": "expense, report, reimbursement, receipts, travel, business expenses",
            "documents": [
                {"title": "Expense Reimbursement Policy", "relevance": 0.95, "content": "Submit expense reports within 30 days of incurring expenses. Include original receipts and proper documentation for all business expenses..."},
                {"title": "Expense Report Submission Guide", "relevance": 0.91, "content": "Use the online expense portal to submit reports. Attach digital copies of receipts and provide detailed descriptions of each expense..."},
                {"title": "Approval Process", "relevance": 0.87, "content": "Expense reports require manager approval and are processed within 5-7 business days. Reimbursements are issued via direct deposit..."}
            ],
            "response": """**Answer**: To submit an expense report:

1. **Access the expense portal** through the employee dashboard
2. **Create a new report** and select the appropriate expense categories
3. **Attach digital receipts** for all expenses (original receipts required)
4. **Provide detailed descriptions** for each expense item
5. **Submit for manager approval** within 30 days of incurring expenses
6. **Track status** through the portal - reports are processed within 5-7 business days

**Eligible expenses include:**
- Business travel (flights, hotels, meals)
- Client entertainment
- Office supplies
- Professional development

Reimbursements are issued via direct deposit to your registered bank account.

**Sources**:
- Expense Reimbursement Policy
- Expense Report Submission Guide
- Approval Process"""
        }
    
    else:
        # Default response for unknown questions
        return {
            "keywords": "general, information, help, support",
            "documents": [
                {"title": "General Information Database", "relevance": 0.75, "content": "This is a general information resource that can help answer various questions about company policies and procedures..."},
                {"title": "Support Documentation", "relevance": 0.70, "content": "For specific questions not covered in our knowledge base, please contact the appropriate department or support team..."}
            ],
            "response": """**Answer**: I found some general information that might be helpful, but for the most accurate and specific answer to your question, I recommend:

1. **Contacting the appropriate department** directly
2. **Checking the employee handbook** for detailed policies
3. **Speaking with your manager** for department-specific information
4. **Using the company support portal** for technical issues

This ensures you get the most current and accurate information for your specific situation.

**Sources**:
- General Information Database
- Support Documentation"""
        }

def show_rag_architectures():
    st.markdown('<h2 class="section-header">🏗️ RAG Architectures</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    RAG systems come in many different shapes and sizes. Each architecture is designed for specific use cases 
    and complexity levels. Let's explore the 8 main RAG patterns:
    """)
    
    # Architecture selection
    architecture = st.selectbox(
        "Choose a RAG architecture to explore:",
        [
            "Naive RAG (Basic RAG)",
            "Self-RAG",
            "Multimodal RAG", 
            "HyDE (Hypothetical Document Embeddings)",
            "Corrective RAG",
            "Graph RAG",
            "Hybrid RAG",
            "Adaptive RAG",
            "Agentic RAG"
        ]
    )
    
    if architecture == "Naive RAG (Basic RAG)":
        show_naive_rag()
    elif architecture == "Self-RAG":
        show_self_rag()
    elif architecture == "Multimodal RAG":
        show_multimodal_rag()
    elif architecture == "HyDE (Hypothetical Document Embeddings)":
        show_hyde_rag()
    elif architecture == "Corrective RAG":
        show_corrective_rag()
    elif architecture == "Graph RAG":
        show_graph_rag()
    elif architecture == "Hybrid RAG":
        show_hybrid_rag()
    elif architecture == "Adaptive RAG":
        show_adaptive_rag()
    elif architecture == "Agentic RAG":
        show_agentic_rag()

def show_naive_rag():
    st.markdown("### Naive RAG (Basic RAG) - The Simple Start")
    
    st.markdown("""
    **Think of it as**: A basic library system where you ask a question, the librarian finds relevant books, 
    and gives you an answer based on those books.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        The simplest RAG implementation that follows a straightforward retrieve-then-generate pattern.
        
        **Flow**:
        1. **User Query**: Receive user question or request
        2. **Embedding**: Convert query to vector representation using embedding model
        3. **Retrieval**: Find relevant documents from vector database using similarity search
        4. **Context Assembly**: Combine query with retrieved documents in prompt template
        5. **Generation**: Generate response using LLM with assembled context
        6. **Response**: Return answer with source attribution
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Simple to implement and understand
        - Fast processing with minimal latency
        - Good baseline performance
        - Easy to debug and maintain
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Limited context understanding
        - No query refinement capabilities
        - Single retrieval step may miss relevant information
        - Basic relevance ranking
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                    🟣 Naive RAG                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🧠 Embedding ──→ 📁 Data Sources       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Output              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│                    "What is machine learning?"                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Query Processing                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Convert to      │  │ Generate        │  │ Create Search   │ │
│  │ Vector          │  │ Embedding       │  │ Query           │ │
│  │ (Port: 3001)    │  │ (Port: 3002)    │  │ (Port: 3003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vector Database                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Similarity      │  │ Retrieve Top    │  │ Rank Results    │ │
│  │ Search          │  │ Documents       │  │ by Relevance    │ │
│  │ (Port: 5432)    │  │ (Port: 5433)    │  │ (Port: 5434)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Response Generation                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine Query   │  │ Generate        │  │ Format &        │ │
│  │ + Documents     │  │ Response        │  │ Add Sources     │ │
│  │ (Port: 4001)    │  │ (Port: 4002)    │  │ (Port: 4003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Final Answer                                │
│              "Machine learning is a subset of AI..."            │
│              Sources: [Document 1, Document 3, Document 7]     │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Question Answering: Answer questions from document collections
        - Document Summarization: Summarize based on retrieved context
        - Information Retrieval: Find and present relevant information
        - Simple Chatbots: Basic conversational interfaces
        """)

def show_self_rag():
    st.markdown("### Self-RAG - The Self-Reflective Approach")
    
    st.markdown("""
    **Think of it as**: A smart student who not only answers questions but also checks their own work, 
    reflects on whether their answer is good enough, and goes back to find better information if needed. 
    It's like having a librarian who double-checks their own research before giving you the final answer.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Self-RAG (Self-Reflective Retrieval-Augmented Generation) adds self-reflection capabilities 
        to the RAG process, allowing the system to evaluate and improve its own responses.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Initial Retrieval**: Retrieve relevant documents
        3. **Initial Generation**: Generate initial response
        4. **Self-Reflection**: Evaluate the quality of the response
        5. **Retrieval Decision**: Decide if more information is needed
        6. **Additional Retrieval**: If needed, retrieve more documents
        7. **Final Generation**: Generate improved response
        8. **Self-Critique**: Final quality check and refinement
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Higher quality responses through self-reflection
        - Ability to identify and correct mistakes
        - Dynamic retrieval based on response quality
        - Better handling of complex queries
        - Improved accuracy and reliability
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Increased computational complexity
        - Longer response times due to reflection steps
        - More complex implementation
        - Requires additional models for reflection
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                  🟣 Self-RAG                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🔍 Initial ──→ 🤖 Initial              │
│       │              Retrieval      Generation             │
│       │                │                │                  │
│       │                │                ▼                  │
│       │                │          🧠 Self-Reflection       │
│       │                │                │                  │
│       │                │                ▼                  │
│       │                │          ⚖️ Retrieval Decision    │
│       │                │                │                  │
│       │                │                ▼                  │
│       │                │          🔍 Additional Retrieval  │
│       │                │                │                  │
│       │                └────────────────┘                  │
│       │                                                   │
│       ▼                                                   │
│  📄 Enhanced Context ──→ 🤖 Final ──→ 📤 High-Quality    │
│                          Generation      Response          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "How does climate change affect agriculture?"     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Initial Retrieval                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Search          │  │ Retrieve        │  │ Rank Initial    │ │
│  │ Knowledge       │  │ Documents       │  │ Results         │ │
│  │ Base            │  │ (Port: 13001)   │  │ (Port: 13002)   │ │
│  │ (Port: 13000)   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Initial Generation                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Generate        │  │ Create          │  │ Format Initial  │ │
│  │ Initial         │  │ Response        │  │ Response        │ │
│  │ Response        │  │ (Port: 14001)   │  │ (Port: 14002)   │ │
│  │ (Port: 14000)   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Self-Reflection                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Evaluate        │  │ Check Quality   │  │ Determine if    │ │
│  │ Response        │  │ and Relevance   │  │ More Info       │ │
│  │ Quality         │  │ (Port: 15001)   │  │ Needed          │ │
│  │ (Port: 15000)   │  │                 │  │ (Port: 15002)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Decision Point                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Quality         │  │ Additional      │  │ Use Current     │ │
│  │ Threshold       │  │ Retrieval       │  │ Response        │ │
│  │ (Port: 16001)   │  │ (Port: 16002)   │  │ (Port: 16003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Final Response Generation                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine All     │  │ Generate        │  │ Add Source      │ │
│  │ Information     │  │ Final           │  │ Citations       │ │
│  │ (Port: 17001)   │  │ Response        │  │ (Port: 17003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    High-Quality Answer                         │
│              "Climate change affects agriculture through..."     │
│              Sources: [Climate Study 2023, Agriculture Report]  │
│              Verified by: [Self-Reflection Process]             │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - High-Quality Q&A: When accuracy is critical
        - Research Assistance: Academic and scientific research
        - Content Creation: Blog posts, articles, and reports
        - Educational Content: Learning materials and explanations
        - Professional Services: Legal, medical, and technical consulting
        """)

def show_multimodal_rag():
    st.markdown("### Multimodal RAG - The Multi-Sensory Approach")
    
    st.markdown("""
    **Think of it as**: A smart assistant that can understand and work with text, images, audio, and video - 
    like having a librarian who can read books, analyze pictures, listen to recordings, and watch videos 
    to answer your questions.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Multimodal RAG processes different types of data (text, images, audio, video) and combines 
        information from multiple modalities to provide comprehensive answers.
        
        **Flow**:
        1. **Multi-Modal Input**: Process text, images, audio, video inputs
        2. **Cross-Modal Embedding**: Convert different modalities to unified vector space
        3. **Multi-Source Retrieval**: Search across text, image, and other databases
        4. **Information Fusion**: Combine information from different modalities
        5. **Context Assembly**: Create rich context with multimodal information
        6. **Multi-Modal Generation**: Generate responses incorporating multiple formats
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Rich information retrieval across modalities
        - Comprehensive understanding of complex content
        - Better user experience with multimedia
        - Handles real-world diverse data types
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Higher computational complexity
        - Requires specialized models for each modality
        - More complex data processing pipeline
        - Higher storage and processing costs
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                  🟣 Multimodal RAG                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🧠 Multi-Modal ──→ 📁 Multi-Modal      │
│       │              Embedding           Data Sources      │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Rich Output         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Modal Input                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    Text     │  │   Images    │  │    Audio    │  │  Video  │ │
│  │ "Find cars" │  │ [car.jpg]   │  │ [car.wav]   │  │[car.mp4]│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Modal Encoders                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Text        │  │ Image       │  │ Audio       │  │ Video   │ │
│  │ Encoder     │  │ Encoder     │  │ Encoder     │  │ Encoder │ │
│  │ (Port: 5001)│  │ (Port: 5002)│  │ (Port: 5003)│  │(Port:5004)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Unified Vector Space                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Cross-Modal     │  │ Vector          │  │ Similarity      │ │
│  │ Alignment       │  │ Fusion          │  │ Matching        │ │
│  │ (Port: 6001)    │  │ (Port: 6002)    │  │ (Port: 6003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Modal Database                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Text            │  │ Image           │  │ Audio/Video     │ │
│  │ Documents       │  │ Database        │  │ Database        │ │
│  │ (Port: 7001)    │  │ (Port: 7002)    │  │ (Port: 7003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Response Generation                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Information     │  │ Multi-Modal     │  │ Format &        │ │
│  │ Fusion          │  │ Response        │  │ Present         │ │
│  │ (Port: 8001)    │  │ (Port: 8002)    │  │ (Port: 8003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Rich Multi-Modal Answer                     │
│              "Found 5 cars matching your description..."        │
│              [Text + Images + Audio + Video Results]           │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Document Analysis: Process documents with images and text
        - Video Understanding: Answer questions about video content
        - Product Search: Search using images and text descriptions
        - Educational Content: Interactive learning with multimedia
        - Medical Diagnosis: Analyze medical images with textual reports
        """)

def show_hyde_rag():
    st.markdown("### HyDE RAG - The 'Guess First' Approach")
    
    st.markdown("""
    **Think of it as**: A smart detective who first makes an educated guess about what the answer might look like, 
    then uses that guess to find better evidence. It's like asking "What would a good answer to this question 
    look like?" and then searching for documents that match that hypothetical answer.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        HyDE (Hypothetical Document Embeddings) generates a hypothetical answer first, then uses that 
        answer to find better matching documents.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Hypothetical Response Generation**: LLM generates hypothetical answer
        3. **Response Embedding**: Convert hypothetical response to vector
        4. **Enhanced Retrieval**: Use hypothetical response embedding for better document retrieval
        5. **Context Assembly**: Combine original query with retrieved documents
        6. **Final Generation**: Generate actual response using retrieved context
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Improved retrieval accuracy through hypothesis generation
        - Better handling of complex and ambiguous queries
        - Enhanced semantic matching between queries and documents
        - Reduced semantic gap between questions and answers
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Additional computational overhead from hypothesis generation
        - Potential for hypothesis bias affecting retrieval
        - More complex pipeline with additional failure points
        - Requires careful prompt engineering for hypothesis generation
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                    🟣 HyDE RAG                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 📝 Hypothetical ──→ 🧠 Embedding        │
│       │              Response              │                │
│       │                │                   │                │
│       │                │                   ▼                │
│       │                │              📁 Data Sources       │
│       │                │                   │                │
│       │                │                   ▼                │
│       │                │              🗄️ Vector DB         │
│       │                │                   │                │
│       │                │                   │                │
│       │                └───────────────────┘                │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Enhanced Output     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "How does machine learning work?"                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hypothesis Generation                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Generate        │  │ Create          │  │ Format          │ │
│  │ Hypothetical    │  │ Answer          │  │ Hypothesis      │ │
│  │ Answer          │  │ Template        │  │ Document        │ │
│  │ (Port: 9001)    │  │ (Port: 9002)    │  │ (Port: 9003)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Enhanced Retrieval                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Convert         │  │ Search with     │  │ Retrieve        │ │
│  │ Hypothesis      │  │ Hypothesis      │  │ Better          │ │
│  │ to Vector       │  │ Vector          │  │ Documents       │ │
│  │ (Port: 10001)   │  │ (Port: 10002)   │  │ (Port: 10003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Document Database                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Similarity      │  │ Rank by         │  │ Filter by       │ │
│  │ Matching        │  │ Relevance       │  │ Quality         │ │
│  │ (Port: 11001)   │  │ (Port: 11002)   │  │ (Port: 11003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Final Response Generation                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine Query   │  │ Generate        │  │ Validate &      │ │
│  │ + Better Docs   │  │ Final Answer    │  │ Format          │ │
│  │ (Port: 12001)   │  │ (Port: 12002)   │  │ (Port: 12003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Improved Answer                             │
│              "Machine learning is a method of data analysis..." │
│              Sources: [Enhanced Document 2, Document 5]        │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Complex Query Answering: When queries are ambiguous or complex
        - Domain-Specific Search: Technical or specialized knowledge retrieval
        - Research Assistance: Academic and scientific information retrieval
        - Legal Research: Finding relevant legal precedents and documents
        """)

def show_corrective_rag():
    st.markdown("### Corrective RAG - The Quality Control System")
    
    st.markdown("""
    **Think of it as**: A smart editor who not only finds information but also checks if it's good enough, 
    corrects mistakes, and even searches the web for better information if needed. It's like having a 
    librarian who double-checks every book before giving you an answer.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Corrective RAG includes quality assessment and correction mechanisms to ensure accurate responses.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Initial Retrieval**: Retrieve documents from knowledge base
        3. **Relevance Grading**: Grade retrieved documents for relevance and quality
        4. **Correction Decision**: Decide if additional retrieval or web search is needed
        5. **Corrective Actions**: Apply corrections and improvements
        6. **Context Assembly**: Combine corrected information with original query
        7. **Generation**: Generate response using validated context
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Higher accuracy through validation and correction
        - Ability to handle incomplete knowledge bases
        - Dynamic information updating through web search
        - Quality control mechanisms
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Increased complexity and processing time
        - Requires additional models for grading and validation
        - Potential for over-correction or false corrections
        - Higher computational and infrastructure costs
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                  🟣 Corrective RAG                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🧠 Embedding ──→ 📁 Data Sources       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              📊 Grade Quality      │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🔍 Query Analyzer     │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🌐 Search Web         │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              ✅ Correct Info       │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Verified Output     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "What are the side effects of aspirin?"           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Initial Retrieval                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Search          │  │ Retrieve        │  │ Rank Initial    │ │
│  │ Knowledge       │  │ Documents       │  │ Results         │ │
│  │ Base            │  │ (Port: 13001)   │  │ (Port: 13002)   │ │
│  │ (Port: 13000)   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Quality Assessment                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Relevance       │  │ Accuracy        │  │ Quality         │ │
│  │ Checker         │  │ Validator       │  │ Scorer          │ │
│  │ (Port: 14001)   │  │ (Port: 14002)   │  │ (Port: 14003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Decision Point                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Quality         │  │ Web Search      │  │ Use Retrieved   │ │
│  │ Threshold       │  │ Trigger         │  │ Documents       │ │
│  │ (Port: 15001)   │  │ (Port: 15002)   │  │ (Port: 15003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Web Search (If Needed)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Search          │  │ Validate        │  │ Combine with    │ │
│  │ Web APIs        │  │ Web Results     │  │ Retrieved Docs  │ │
│  │ (Port: 16001)   │  │ (Port: 16002)   │  │ (Port: 16003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Final Response Generation                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Fact Check      │  │ Generate        │  │ Add Source      │ │
│  │ & Verify        │  │ Verified        │  │ Citations       │ │
│  │ (Port: 17001)   │  │ Response        │  │ (Port: 17003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Verified Answer                             │
│              "Common side effects include stomach upset..."     │
│              Sources: [Medical Journal 2023, FDA.gov, WebMD]   │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Fact-Checking Systems: Verify information accuracy
        - News and Current Events: Get up-to-date information
        - Research Validation: Cross-reference research findings
        - Quality Assurance: Ensure high-quality responses
        """)

def show_graph_rag():
    st.markdown("### Graph RAG - The Relationship Explorer")
    
    st.markdown("""
    **Think of it as**: A detective who doesn't just look for direct answers but explores connections and 
    relationships. It's like having a librarian who knows how every book connects to other books, people, 
    and concepts, and can trace those connections to find the most relevant information.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Graph RAG uses knowledge graphs to understand relationships between entities and concepts.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Entity Extraction**: Extract entities and concepts from query
        3. **Graph Traversal**: Navigate knowledge graph to find related information
        4. **Relationship Analysis**: Analyze connections between entities
        5. **Context Expansion**: Expand context using graph relationships
        6. **Document Retrieval**: Retrieve documents based on graph insights
        7. **Generation**: Generate response incorporating relationship information
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Rich relationship understanding
        - Better context through connected information
        - Improved reasoning capabilities
        - Handles complex multi-hop questions
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Requires graph construction and maintenance
        - Higher complexity in implementation
        - Computational overhead for graph operations
        - Dependency on graph quality and completeness
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                    🟣 Graph RAG                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🧠 Embedding ──→ 📁 Data Sources       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       │              🔗 Graph Generator ──→ 📊 Graph DB    │
│       │                    │                    │           │
│       │                    │                    │           │
│       │                    └────────────────────┘           │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Contextual Output  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "How does climate change affect agriculture?"     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Entity Extraction                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Extract         │  │ Identify        │  │ Create          │ │
│  │ Entities        │  │ Concepts        │  │ Entity          │ │
│  │ (Port: 18001)   │  │ (Port: 18002)   │  │ Graph           │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Graph                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Entity          │  │ Relationship    │  │ Graph           │ │
│  │ Database        │  │ Database        │  │ Traversal       │ │
│  │ (Port: 19001)   │  │ (Port: 19002)   │  │ (Port: 19003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Relationship Exploration                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Find Related    │  │ Follow          │  │ Gather          │ │
│  │ Entities        │  │ Connections     │  │ Context         │ │
│  │ (Port: 20001)   │  │ (Port: 20002)   │  │ (Port: 20003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Document Retrieval                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Retrieve        │  │ Rank by         │  │ Filter by       │ │
│  │ Connected       │  │ Relationship    │  │ Relevance       │ │
│  │ Documents       │  │ Strength        │  │ (Port: 21003)   │ │
│  │ (Port: 21001)   │  │ (Port: 21002)   │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Contextual Response Generation              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine         │  │ Generate        │  │ Add             │ │
│  │ Graph Context   │  │ Rich Response   │  │ Relationship    │ │
│  │ (Port: 22001)   │  │ (Port: 22002)   │  │ Info            │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Rich Contextual Answer                      │
│              "Climate change affects agriculture through..."     │
│              [Temperature] → [Crop Yield] → [Food Security]     │
│              Sources: [Climate Study 2023, Agriculture Report]  │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Knowledge Base Systems: Complex organizational knowledge
        - Scientific Research: Research papers with citation networks
        - Social Network Analysis: Understanding relationships and influences
        - Recommendation Systems: Content recommendation based on relationships
        - Financial Analysis: Company relationships and market connections
        """)

def show_hybrid_rag():
    st.markdown("### Hybrid RAG - The Best of All Worlds")
    
    st.markdown("""
    **Think of it as**: A super-librarian who uses every trick in the book - keyword search, semantic search, 
    relationship exploration, and more - then combines all the best results to give you the most comprehensive 
    answer possible.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Hybrid RAG combines multiple retrieval methods and generation strategies for optimal performance.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Multi-Method Retrieval**: 
           - Dense retrieval using embeddings
           - Sparse retrieval using keywords
           - Graph-based retrieval
        3. **Result Fusion**: Combine results from different retrieval methods
        4. **Ranking and Selection**: Rank and select best documents from combined results
        5. **Context Assembly**: Create rich context from diverse sources
        6. **Generation**: Generate response using hybrid context
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Best performance through method combination
        - Robust retrieval across different query types
        - Improved coverage and accuracy
        - Flexibility in handling diverse use cases
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - High implementation complexity
        - Increased computational requirements
        - More difficult to optimize and tune
        - Higher infrastructure and maintenance costs
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                    🟣 Hybrid RAG                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🧠 Embedding ──→ 📁 Data Sources       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       │              🔗 Graph Generator ──→ 📊 Graph DB    │
│       │                    │                    │           │
│       │                    │                    │           │
│       │                    └────────────────────┘           │
│       │                                                   │
│       │              🔍 Keyword Search ──→ 📚 Text DB     │
│       │                    │                    │           │
│       │                    │                    │           │
│       │                    └────────────────────┘           │
│       │                                                   │
│       │              🔄 Result Fusion ──→ 🎯 Best Results │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Comprehensive Output│
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "What are the benefits of renewable energy?"      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multiple Search Methods                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Keyword     │  │ Semantic    │  │ Graph       │  │ Other   │ │
│  │ Search      │  │ Search      │  │ Search      │  │ Methods │ │
│  │ (Port: 23001)│  │ (Port: 23002)│  │ (Port: 23003)│  │(Port:23004)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Parallel Retrieval                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ BM25/TF-IDF     │  │ Vector          │  │ Knowledge       │ │
│  │ Results         │  │ Similarity      │  │ Graph           │ │
│  │ (Port: 24001)   │  │ Results         │  │ Results         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Result Fusion                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine         │  │ Rank & Score    │  │ Remove          │ │
│  │ Results         │  │ All Results     │  │ Duplicates      │ │
│  │ (Port: 25001)   │  │ (Port: 25002)   │  │ (Port: 25003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Advanced Ranking                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Cross-Encoder   │  │ Diversity       │  │ Final           │ │
│  │ Reranking       │  │ Filtering       │  │ Selection       │ │
│  │ (Port: 26001)   │  │ (Port: 26002)   │  │ (Port: 26003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Comprehensive Response Generation           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Create Rich     │  │ Generate        │  │ Add Multiple    │ │
│  │ Context         │  │ Comprehensive   │  │ Source          │ │
│  │ (Port: 27001)   │  │ Response        │  │ Citations       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Best Comprehensive Answer                   │
│              "Renewable energy offers multiple benefits..."     │
│              Sources: [Scientific Papers, News, Reports]       │
│              [Environmental] + [Economic] + [Social] Benefits   │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Enterprise Search: Comprehensive organizational knowledge retrieval
        - Research Platforms: Academic and scientific research assistance
        - Customer Support: Multi-faceted customer query handling
        - Content Discovery: Finding relevant content across diverse sources
        """)

def show_adaptive_rag():
    st.markdown("### Adaptive RAG - The Smart Chameleon")
    
    st.markdown("""
    **Think of it as**: A shape-shifting librarian who changes their approach based on what kind of question 
    you ask. For simple questions, they use quick methods. For complex questions, they use more sophisticated 
    approaches. It's like having a librarian who adapts their strategy to give you the best possible answer.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Adaptive RAG dynamically adjusts its strategy based on query complexity and requirements.
        
        **Flow**:
        1. **User Query**: Receive user question
        2. **Query Analysis**: Analyze query complexity and requirements
        3. **Strategy Selection**: Choose appropriate retrieval strategy
           - Simple queries → Direct retrieval
           - Complex queries → Multi-step reasoning
        4. **Adaptive Retrieval**: Apply selected retrieval method
        5. **Context Assessment**: Evaluate retrieved context quality
        6. **Generation Adaptation**: Adapt generation based on context and query type
        7. **Response**: Provide response with appropriate level of detail
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Optimal performance for different query types
        - Efficient resource utilization
        - Better user experience through adaptation
        - Scalable across diverse use cases
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - Complex decision-making logic
        - Requires extensive training and tuning
        - Difficult to predict and debug behavior
        - Higher development and maintenance complexity
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                  🟣 Adaptive RAG                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🔍 Query Analyzer ──→ 📊 Strategy       │
│       │                │                    Selection       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🚀 Simple Path       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🧠 Embedding         │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              📁 Data Sources      │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🗄️ Vector DB         │
│       │                │                    │               │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Adaptive Output     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                              │
│              "What is the capital of France?"                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Query Analysis                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Analyze         │  │ Determine       │  │ Select          │ │
│  │ Complexity      │  │ Query Type      │  │ Strategy        │ │
│  │ (Port: 28001)   │  │ (Port: 28002)   │  │ (Port: 28003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Strategy Selection                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Simple      │  │ Complex     │  │ Ambiguous   │  │ Custom  │ │
│  │ Strategy    │  │ Strategy    │  │ Strategy    │  │ Strategy│ │
│  │ (Port: 29001)│  │ (Port: 29002)│  │ (Port: 29003)│  │(Port:29004)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Adaptive Retrieval                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Quick Search    │  │ Deep Analysis   │  │ Clarification   │ │
│  │ (Port: 30001)   │  │ (Port: 30002)   │  │ (Port: 30003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Context Assessment                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Evaluate        │  │ Quality         │  │ Adjust          │ │
│  │ Retrieved       │  │ Check           │  │ Strategy        │ │
│  │ Context         │  │ (Port: 31002)   │  │ (Port: 31003)   │ │
│  │ (Port: 31001)   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Adaptive Response Generation                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Generate        │  │ Adjust Detail   │  │ Format for      │ │
│  │ Appropriate     │  │ Level           │  │ Query Type      │ │
│  │ Response        │  │ (Port: 32002)   │  │ (Port: 32003)   │ │
│  │ (Port: 32001)   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Adaptive Answer                             │
│              "Paris is the capital of France."                 │
│              [Simple, Direct Answer for Simple Question]       │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Intelligent Assistants: Adapt to different user needs
        - Educational Systems: Adjust complexity based on user level
        - Research Tools: Handle varying research complexity
        - Customer Support: Adapt responses to query complexity
        """)

def show_agentic_rag():
    st.markdown("### Agentic RAG - The Team of Experts")
    
    st.markdown("""
    **Think of it as**: A team of specialized librarians, each an expert in their field, working together to 
    answer complex questions. One might be a research expert, another a fact-checker, another a web searcher, 
    and they all coordinate to give you the most comprehensive answer possible.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        #### 🏗️ Architecture Overview
        Agentic RAG uses multiple specialized agents working together to handle complex queries.
        
        **Flow**:
        1. **User Query**: Receive complex user question
        2. **Query Decomposition**: Break down query into sub-tasks
        3. **Agent Assignment**: Assign sub-tasks to specialized agents:
           - Agent 1: ReACT (Reasoning and Acting)
           - Agent 2: CoT (Chain of Thought) Planning
           - Agent 3: Specialized domain agents
        4. **Parallel Processing**: Agents work on their assigned tasks
        5. **Information Synthesis**: Combine results from all agents
        6. **Coordination**: Manage agent interactions and dependencies
        7. **Final Generation**: Generate comprehensive response
        """)
        
        st.markdown("""
        #### ✅ Advantages
        - Handles highly complex, multi-faceted queries
        - Specialized expertise through domain agents
        - Parallel processing for efficiency
        - Comprehensive and thorough responses
        - Scalable agent architecture
        """)
        
        st.markdown("""
        #### ❌ Limitations
        - High complexity in implementation and coordination
        - Significant computational resources required
        - Complex debugging and error handling
        - Potential for agent conflicts or inconsistencies
        - Higher latency due to multi-agent coordination
        """)
    
    with col2:
        # Display the detailed ASCII art diagram from markdown
        st.markdown("""
        #### 🏗️ **Visual Architecture Diagram**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────┐
│                  🟣 Agentic RAG                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👤 User Query ──→ 🤖 Main Agent ──→ 🧠 Memory             │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              📋 Planning          │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🔄 ReACT/CoT         │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🤖 Agent 1           │
│       │                │              🤖 Agent 2           │
│       │                │              🤖 Agent 3           │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              🌐 MCP Servers       │
│       │                │                    │               │
│       │                │                    ▼               │
│       │                │              📊 Local Data        │
│       │                │              🔍 Search Engine     │
│       │                │              ☁️ Cloud Services    │
│       │                │                    │               │
│       │                └────────────────────┘               │
│       │                                                   │
│       ▼                                                   │
│  📄 Prompt Template ──→ 🧠 LLM ──→ 📤 Expert Answer       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🔄 **Detailed Flow**
        """)
        
        st.code("""
┌─────────────────────────────────────────────────────────────────┐
│                        Your Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Frontend  │  │   Backend   │  │   Mobile    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Complex User Query                          │
│              "How does climate change affect global economy?"  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Query Decomposition                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Break Down      │  │ Identify        │  │ Create Task     │ │
│  │ Query           │  │ Sub-tasks       │  │ Assignments     │ │
│  │ (Port: 33001)   │  │ (Port: 33002)   │  │ (Port: 33003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Specialized Agents                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Research    │  │ Fact-Check  │  │ Web Search  │  │ Domain  │ │
│  │ Agent       │  │ Agent       │  │ Agent       │  │ Expert  │ │
│  │ (Port: 34001)│  │ (Port: 34002)│  │ (Port: 34003)│  │(Port:34004)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Parallel Agent Processing                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Climate         │  │ Economic        │  │ Global          │ │
│  │ Research        │  │ Analysis        │  │ Impact          │ │
│  │ (Port: 35001)   │  │ (Port: 35002)   │  │ (Port: 35003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Coordination                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Collect         │  │ Resolve         │  │ Merge           │ │
│  │ Results         │  │ Conflicts       │  │ Information     │ │
│  │ (Port: 36001)   │  │ (Port: 36002)   │  │ (Port: 36003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Information Synthesis                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Combine         │  │ Generate        │  │ Add Expert      │ │
│  │ Agent Results   │  │ Comprehensive   │  │ Citations       │ │
│  │ (Port: 37001)   │  │ Response        │  │ (Port: 37003)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Expert Team Answer                          │
│              "Climate change affects the global economy through..." │
│              [Environmental] → [Economic] → [Social] Impacts    │
│              Sources: [Climate Research, Economic Studies, UN]  │
│              Verified by: [Research Agent, Fact-Check Agent]    │
└─────────────────────────────────────────────────────────────────┘
        """, language="text")
        
        st.markdown("""
        #### 🎯 Use Cases
        - Complex Research: Multi-disciplinary research questions
        - Business Intelligence: Comprehensive business analysis
        - Scientific Discovery: Multi-step scientific investigations
        - Strategic Planning: Complex decision-making scenarios
        - Educational Research: Comprehensive learning assistance
        """)

# Import advanced modules
from advanced_modules import (
    show_implementation_strategies, show_real_world_applications, 
    show_performance_optimization, show_best_practices
)
