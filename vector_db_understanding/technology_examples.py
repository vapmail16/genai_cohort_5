import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Technology Functions
def show_qdrant_details():
    st.markdown("""
    ### Qdrant - High-Performance Vector Database
    
    Qdrant is an open-source vector database designed for high-performance similarity search and machine learning applications.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Qdrant Characteristics")
        
        metrics = {
            "Storage Engine": "Custom in-memory/disk",
            "Index Type": "HNSW",
            "Query Processing": "Multi-threaded, SIMD optimized",
            "API": "REST, gRPC, Python client",
            "License": "Open Source (Apache 2.0)"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ Qdrant Strengths")
        st.success("""
        - **High Performance**: <1ms latency for small datasets
        - **Advanced Filtering**: Complex metadata filtering
        - **Horizontal Scaling**: Sharding and replication
        - **Production Ready**: Used in production systems
        - **Rich Features**: Payload, filtering, multiple indexes
        """)
        
        st.markdown("#### ❌ Qdrant Limitations")
        st.error("""
        - **Self-hosted**: Requires infrastructure management
        - **Learning Curve**: More complex than managed services
        - **Operational Overhead**: Need to manage scaling
        - **Resource Intensive**: Requires significant resources
        """)
    
    with col2:
        st.markdown("#### 🎯 Performance Metrics")
        
        # Simulate performance data
        dataset_sizes = [10000, 100000, 1000000, 10000000]
        latencies = [0.5, 2.0, 10.0, 50.0]  # ms
        throughputs = [10000, 8000, 5000, 2000]  # QPS
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dataset_sizes,
            y=latencies,
            mode='lines+markers',
            name='Latency (ms)',
            line=dict(color='blue'),
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            x=dataset_sizes,
            y=[t/100 for t in throughputs],  # Scale for visibility
            mode='lines+markers',
            name='Throughput (QPS/100)',
            line=dict(color='red'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Qdrant Performance vs Dataset Size',
            xaxis_title='Dataset Size (vectors)',
            yaxis=dict(title='Latency (ms)', side='left'),
            yaxis2=dict(title='Throughput (QPS/100)', side='right', overlaying='y'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Production systems requiring high performance
        - Applications needing complex filtering
        - Large-scale similarity search
        - When you need full control over infrastructure
        """)

def show_pinecone_details():
    st.markdown("""
    ### Pinecone - Managed Vector Database Service
    
    Pinecone is a fully-managed vector database service that provides easy-to-use APIs for building AI applications.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Pinecone Characteristics")
        
        metrics = {
            "Storage Engine": "Distributed cloud storage",
            "Index Type": "Proprietary optimized",
            "Query Processing": "Cloud-native, auto-scaling",
            "API": "REST API with multiple SDKs",
            "License": "Managed Service (SaaS)"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ Pinecone Strengths")
        st.success("""
        - **Fully Managed**: No infrastructure management
        - **Easy Integration**: Simple API and SDKs
        - **Auto-scaling**: Handles traffic spikes automatically
        - **Global Distribution**: Multi-region deployment
        - **Built-in Monitoring**: Performance and usage metrics
        """)
        
        st.markdown("#### ❌ Pinecone Limitations")
        st.error("""
        - **Cost**: Pay per use model can be expensive
        - **Vendor Lock-in**: Dependent on Pinecone service
        - **Limited Control**: Less control over infrastructure
        - **API Dependency**: Requires internet connection
        """)
    
    with col2:
        st.markdown("#### 💰 Cost Analysis")
        
        # Simulate cost calculation
        num_vectors = st.slider("Number of vectors:", 10000, 10000000, 1000000)
        queries_per_month = st.slider("Queries per month:", 10000, 10000000, 1000000)
        
        # Simplified cost calculation (not actual Pinecone pricing)
        storage_cost = (num_vectors * 1536 * 4) / (1024**3) * 0.10  # $0.10 per GB
        query_cost = queries_per_month * 0.0001  # $0.0001 per query
        total_cost = storage_cost + query_cost
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Storage Cost", f"${storage_cost:.2f}/month")
        with col_b:
            st.metric("Query Cost", f"${query_cost:.2f}/month")
        with col_c:
            st.metric("Total Cost", f"${total_cost:.2f}/month")
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Rapid prototyping and development
        - Startups and small teams
        - Applications requiring global distribution
        - When you want to focus on application logic
        """)

def show_pgvector_details():
    st.markdown("""
    ### PG Vector - PostgreSQL Vector Extension
    
    PG Vector is an open-source vector similarity search extension for PostgreSQL, bringing vector capabilities to the popular relational database.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 PG Vector Characteristics")
        
        metrics = {
            "Storage Engine": "PostgreSQL with vector extension",
            "Index Type": "IVFFlat, HNSW (PostgreSQL 15+)",
            "Query Processing": "SQL-based with vector operations",
            "API": "Standard PostgreSQL interface",
            "License": "Open Source (PostgreSQL license)"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ PG Vector Strengths")
        st.success("""
        - **ACID Compliance**: Full transactional guarantees
        - **SQL Integration**: Rich SQL querying capabilities
        - **Existing Infrastructure**: Leverage PostgreSQL expertise
        - **Complex Queries**: Combine vector and relational queries
        - **Mature Ecosystem**: Large PostgreSQL community
        """)
        
        st.markdown("#### ❌ PG Vector Limitations")
        st.error("""
        - **Performance**: Slower than specialized vector databases
        - **Scalability**: Limited by PostgreSQL scaling
        - **Index Limitations**: Fewer index options than specialized DBs
        - **Learning Curve**: Need PostgreSQL knowledge
        """)
    
    with col2:
        st.markdown("#### 🔍 SQL + Vector Example")
        
        st.code("""
-- Create a table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    embedding VECTOR(1536)
);

-- Create HNSW index
CREATE INDEX ON documents 
USING hnsw (embedding vector_cosine_ops);

-- Search for similar documents
SELECT title, content, 
       embedding <=> '[0.1,0.2,0.3,...]' AS distance
FROM documents 
ORDER BY embedding <=> '[0.1,0.2,0.3,...]' 
LIMIT 10;
        """, language='sql')
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Enterprise applications with existing PostgreSQL
        - When ACID compliance is required
        - Complex queries mixing vector and relational data
        - Teams with strong PostgreSQL expertise
        """)

def show_chroma_details():
    st.markdown("""
    ### Chroma - Open Source Embeddings Database
    
    Chroma is an open-source embeddings database that makes it easy to build AI applications with embeddings.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Chroma Characteristics")
        
        metrics = {
            "Storage Engine": "SQLite, DuckDB, or PostgreSQL",
            "Index Type": "HNSW with configurable parameters",
            "Query Processing": "Python-native, easy integration",
            "API": "Python client, REST API",
            "License": "Open Source (Apache 2.0)"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ Chroma Strengths")
        st.success("""
        - **Easy Setup**: Simple installation and configuration
        - **Python Native**: Excellent Python integration
        - **Flexible Storage**: Multiple storage backends
        - **Good Documentation**: Comprehensive guides
        - **Development Friendly**: Perfect for prototyping
        """)
        
        st.markdown("#### ❌ Chroma Limitations")
        st.error("""
        - **Performance**: Limited compared to production systems
        - **Scalability**: Not designed for massive scale
        - **Feature Set**: Fewer advanced features
        - **Production Readiness**: More suited for development
        """)
    
    with col2:
        st.markdown("#### 🐍 Python Integration Example")
        
        st.code("""
import chromadb

# Create client
client = chromadb.Client()

# Create collection
collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=["Document 1 content", "Document 2 content"],
    embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    ids=["doc1", "doc2"]
)

# Query similar documents
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]],
    n_results=5
)
        """, language='python')
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Rapid prototyping and development
        - Small to medium-scale applications
        - Research and academic projects
        - Learning and experimentation
        """)

def show_technology_comparison():
    st.markdown("### 📊 Vector Database Technology Comparison")
    
    # Comparison table
    comparison_data = {
        "Technology": ["Qdrant", "Pinecone", "PG Vector", "Chroma"],
        "Type": ["Self-hosted", "Managed Service", "Extension", "Open Source"],
        "Performance": ["Very High", "High", "Medium", "Medium"],
        "Scalability": ["High", "Very High", "Medium", "Low"],
        "Ease of Use": ["Medium", "Very Easy", "Medium", "Easy"],
        "Cost": ["Infrastructure", "Pay per use", "Infrastructure", "Free"],
        "Best For": ["Production", "Startups", "Enterprise", "Development"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    st.markdown("### 🎯 Technology Selection Guide")
    
    use_case = st.selectbox(
        "What's your primary use case?",
        ["Production System", "Startup/Prototype", "Enterprise Integration", "Development/Research", "Cost Sensitive"]
    )
    
    if use_case == "Production System":
        st.success("**Recommended: Qdrant** - High performance, production-ready, full control")
    elif use_case == "Startup/Prototype":
        st.success("**Recommended: Pinecone or Chroma** - Easy to use, quick setup")
    elif use_case == "Enterprise Integration":
        st.success("**Recommended: PG Vector** - Integrates with existing PostgreSQL infrastructure")
    elif use_case == "Development/Research":
        st.success("**Recommended: Chroma** - Easy to use, good for experimentation")
    elif use_case == "Cost Sensitive":
        st.success("**Recommended: Qdrant or Chroma** - Open source, no per-use costs")

# Real-World Example Functions
def show_ecommerce_example():
    st.markdown("""
    ### E-commerce Product Search - Finding Similar Products
    
    Vector databases power modern e-commerce search by understanding product similarity beyond just text matching.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive E-commerce Demo")
        
        # Sample product database
        products = {
            "iPhone 15 Pro": {
                "vector": [0.9, 0.8, 0.1, 0.2, 0.7],  # [tech, premium, budget, fashion, utility]
                "price": 999,
                "category": "Electronics"
            },
            "Samsung Galaxy S24": {
                "vector": [0.8, 0.7, 0.2, 0.3, 0.6],
                "price": 899,
                "category": "Electronics"
            },
            "Nike Air Max": {
                "vector": [0.1, 0.3, 0.4, 0.9, 0.6],
                "price": 120,
                "category": "Fashion"
            },
            "MacBook Pro": {
                "vector": [0.95, 0.9, 0.0, 0.1, 0.8],
                "price": 1999,
                "category": "Electronics"
            },
            "Adidas Sneakers": {
                "vector": [0.1, 0.2, 0.5, 0.8, 0.7],
                "price": 80,
                "category": "Fashion"
            }
        }
        
        # Query product selection
        query_product = st.selectbox("Search for similar products to:", list(products.keys()))
        k = st.slider("Number of similar products:", 1, 4, 3)
        
        # Calculate similarities
        query_vector = products[query_product]["vector"]
        similarities = []
        
        for product, data in products.items():
            if product != query_product:
                # Cosine similarity
                dot_product = sum(a * b for a, b in zip(query_vector, data["vector"]))
                norm_query = (sum(a * a for a in query_vector)) ** 0.5
                norm_product = (sum(b * b for b in data["vector"])) ** 0.5
                similarity = dot_product / (norm_query * norm_product) if norm_query != 0 and norm_product != 0 else 0
                similarities.append((product, similarity, data))
        
        # Sort by similarity and get top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_k = similarities[:k]
        
        st.markdown("#### 📊 Search Results")
        st.write(f"**Query Product**: {query_product}")
        st.write(f"**Similar Products:**")
        
        for i, (product, similarity, data) in enumerate(top_k, 1):
            st.write(f"{i}. **{product}** (Similarity: {similarity:.3f}) - ${data['price']} - {data['category']}")
        
        # Visualize
        categories = ['Tech', 'Premium', 'Budget', 'Fashion', 'Utility']
        
        fig = go.Figure()
        
        # Query product
        fig.add_trace(go.Scatterpolar(
            r=query_vector + [query_vector[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=query_product,
            line_color='red',
            line_width=3
        ))
        
        # Similar products
        colors = ['blue', 'green', 'orange', 'purple']
        for i, (product, similarity, data) in enumerate(top_k):
            fig.add_trace(go.Scatterpolar(
                r=data["vector"] + [data["vector"][0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=f"{product} ({similarity:.3f})",
                line_color=colors[i % len(colors)],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"Similar Products to {query_product}"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏪 E-commerce Use Cases")
        
        st.markdown("**1. Product Recommendations**")
        st.info("""
        - "Customers who bought X also bought Y"
        - Cross-selling and upselling
        - Personalized product suggestions
        - Seasonal recommendations
        """)
        
        st.markdown("**2. Visual Search**")
        st.info("""
        - Upload image to find similar products
        - "Find products like this"
        - Fashion and home decor search
        - Reverse image search
        """)
        
        st.markdown("**3. Semantic Search**")
        st.info("""
        - "Find comfortable running shoes"
        - "Show me premium tech gadgets"
        - Natural language product search
        - Intent-based search
        """)
        
        st.markdown("#### 📊 Business Impact")
        
        impact_data = {
            "Metric": ["Search Conversion", "Average Order Value", "Customer Satisfaction", "Time to Purchase"],
            "Improvement": ["+25%", "+15%", "+30%", "-40%"],
            "Vector DB Benefit": ["Better relevance", "Better recommendations", "Better search", "Faster results"]
        }
        
        df = pd.DataFrame(impact_data)
        st.table(df)
        
        st.markdown("#### 🎯 Implementation Tips")
        st.success("""
        1. **Product Embeddings**: Use product descriptions, images, and attributes
        2. **User Behavior**: Incorporate click, purchase, and view data
        3. **Real-time Updates**: Keep embeddings current with new products
        4. **A/B Testing**: Test different similarity metrics
        5. **Performance**: Cache frequent queries for speed
        """)

def show_recommendation_example():
    st.markdown("""
    ### Recommendation Systems - Personalizing Content
    
    Vector databases enable sophisticated recommendation systems by understanding user preferences and content similarity.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Recommendation Demo")
        
        # Sample user and content database
        users = {
            "Alice": [0.8, 0.6, 0.9, 0.3, 0.7],  # [action, comedy, drama, horror, romance]
            "Bob": [0.9, 0.2, 0.4, 0.8, 0.1],
            "Charlie": [0.3, 0.9, 0.2, 0.1, 0.8],
            "Diana": [0.7, 0.5, 0.8, 0.2, 0.9]
        }
        
        movies = {
            "The Matrix": [0.9, 0.1, 0.3, 0.2, 0.1],
            "Titanic": [0.1, 0.0, 0.9, 0.0, 0.9],
            "Deadpool": [0.8, 0.9, 0.2, 0.3, 0.1],
            "The Exorcist": [0.2, 0.1, 0.4, 0.9, 0.0],
            "La La Land": [0.1, 0.3, 0.6, 0.0, 0.9],
            "John Wick": [0.95, 0.2, 0.1, 0.4, 0.0],
            "The Notebook": [0.0, 0.2, 0.8, 0.0, 0.9],
            "Scary Movie": [0.3, 0.9, 0.1, 0.6, 0.2]
        }
        
        # User selection
        user = st.selectbox("Select user:", list(users.keys()))
        
        # Calculate recommendations
        user_vector = users[user]
        recommendations = []
        
        for movie, movie_vector in movies.items():
            # Cosine similarity
            dot_product = sum(a * b for a, b in zip(user_vector, movie_vector))
            norm_user = (sum(a * a for a in user_vector)) ** 0.5
            norm_movie = (sum(b * b for b in movie_vector)) ** 0.5
            similarity = dot_product / (norm_user * norm_movie) if norm_user != 0 and norm_movie != 0 else 0
            recommendations.append((movie, similarity, movie_vector))
        
        # Sort by similarity and get top 5
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = recommendations[:5]
        
        st.markdown("#### 📊 Recommendations for " + user)
        
        for i, (movie, similarity, vector) in enumerate(top_recommendations, 1):
            st.write(f"{i}. **{movie}** (Match: {similarity:.3f})")
        
        # Visualize user preferences vs recommendations
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
        
        fig = go.Figure()
        
        # User preferences
        fig.add_trace(go.Scatterpolar(
            r=user_vector + [user_vector[0]],
            theta=genres + [genres[0]],
            fill='toself',
            name=f"{user}'s Preferences",
            line_color='blue',
            line_width=3
        ))
        
        # Top recommendation
        if top_recommendations:
            top_movie, top_similarity, top_vector = top_recommendations[0]
            fig.add_trace(go.Scatterpolar(
                r=top_vector + [top_vector[0]],
                theta=genres + [genres[0]],
                fill='toself',
                name=f"{top_movie} (Top Match)",
                line_color='red',
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"User Preferences vs Top Recommendation"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Recommendation Types")
        
        st.markdown("**1. Collaborative Filtering**")
        st.info("""
        - Find users with similar preferences
        - Recommend items liked by similar users
        - "Users like you also liked..."
        - Works well with explicit ratings
        """)
        
        st.markdown("**2. Content-Based Filtering**")
        st.info("""
        - Analyze item features and user preferences
        - Recommend items similar to liked content
        - "More like this..."
        - Works well with item metadata
        """)
        
        st.markdown("**3. Hybrid Approaches**")
        st.info("""
        - Combine collaborative and content-based
        - Use multiple signals for better accuracy
        - Machine learning models
        - Real-time personalization
        """)
        
        st.markdown("#### 📊 Recommendation Metrics")
        
        metrics_data = {
            "Metric": ["Precision@10", "Recall@10", "NDCG", "Coverage", "Diversity"],
            "Description": ["Relevant items in top 10", "Relevant items found", "Ranking quality", "Item coverage", "Recommendation variety"],
            "Good Score": ["> 0.3", "> 0.2", "> 0.4", "> 0.8", "> 0.6"]
        }
        
        df = pd.DataFrame(metrics_data)
        st.table(df)
        
        st.markdown("#### 🎯 Implementation Best Practices")
        st.success("""
        1. **Cold Start**: Handle new users and items
        2. **Real-time Updates**: Update recommendations quickly
        3. **Diversity**: Balance relevance with variety
        4. **Scalability**: Handle millions of users/items
        5. **A/B Testing**: Continuously improve algorithms
        """)

def show_document_example():
    st.markdown("""
    ### Document Retrieval - Finding Relevant Information
    
    Vector databases enable semantic document search, understanding meaning beyond keyword matching.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Document Search")
        
        # Sample document database
        documents = {
            "Machine Learning Guide": {
                "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models.",
                "vector": [0.9, 0.8, 0.1, 0.2, 0.7]  # [tech, education, business, health, science]
            },
            "Python Programming": {
                "content": "Python is a high-level programming language known for its simplicity and readability.",
                "vector": [0.8, 0.9, 0.2, 0.1, 0.6]
            },
            "Business Strategy": {
                "content": "Strategic planning involves setting goals and determining actions to achieve long-term objectives.",
                "vector": [0.2, 0.3, 0.9, 0.1, 0.4]
            },
            "Health and Fitness": {
                "content": "Regular exercise and a balanced diet are essential for maintaining good health.",
                "vector": [0.1, 0.2, 0.3, 0.9, 0.5]
            },
            "Data Science": {
                "content": "Data science combines statistics, programming, and domain expertise to extract insights from data.",
                "vector": [0.9, 0.7, 0.4, 0.1, 0.8]
            },
            "Financial Planning": {
                "content": "Investment strategies should be based on risk tolerance and long-term financial goals.",
                "vector": [0.3, 0.4, 0.8, 0.0, 0.6]
            }
        }
        
        # Search query
        query = st.text_input("Search query:", "How to learn artificial intelligence?")
        
        # Simulate query vector (in reality, you'd use an embedding model)
        query_vector = [0.8, 0.9, 0.2, 0.1, 0.7]  # Similar to tech/education
        
        # Calculate similarities
        similarities = []
        for doc_id, doc_data in documents.items():
            # Cosine similarity
            dot_product = sum(a * b for a, b in zip(query_vector, doc_data["vector"]))
            norm_query = (sum(a * a for a in query_vector)) ** 0.5
            norm_doc = (sum(b * b for b in doc_data["vector"])) ** 0.5
            similarity = dot_product / (norm_query * norm_doc) if norm_query != 0 and norm_doc != 0 else 0
            similarities.append((doc_id, similarity, doc_data))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("#### 📊 Search Results")
        st.write(f"**Query**: \"{query}\"")
        st.write("**Ranked Results:**")
        
        for i, (doc_id, similarity, doc_data) in enumerate(similarities, 1):
            st.write(f"{i}. **{doc_id}** (Relevance: {similarity:.3f})")
            st.write(f"   *{doc_data['content'][:100]}...*")
        
        # Visualize document similarity
        categories = ['Tech', 'Education', 'Business', 'Health', 'Science']
        
        fig = go.Figure()
        
        # Query vector
        fig.add_trace(go.Scatterpolar(
            r=query_vector + [query_vector[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Query',
            line_color='red',
            line_width=3
        ))
        
        # Top 3 documents
        colors = ['blue', 'green', 'orange']
        for i, (doc_id, similarity, doc_data) in enumerate(similarities[:3]):
            fig.add_trace(go.Scatterpolar(
                r=doc_data["vector"] + [doc_data["vector"][0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=f"{doc_id} ({similarity:.3f})",
                line_color=colors[i % len(colors)],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Query vs Document Similarity"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📚 Document Search Use Cases")
        
        st.markdown("**1. Enterprise Search**")
        st.info("""
        - Search internal documents and knowledge base
        - Find relevant policies and procedures
        - Employee self-service information
        - Compliance and audit support
        """)
        
        st.markdown("**2. Academic Research**")
        st.info("""
        - Find relevant papers and publications
        - Literature review and citation analysis
        - Research collaboration discovery
        - Trend analysis in research fields
        """)
        
        st.markdown("**3. Customer Support**")
        st.info("""
        - Search FAQ and help articles
        - Find solutions to customer problems
        - Knowledge base for support agents
        - Automated response generation
        """)
        
        st.markdown("#### 📊 Search Quality Metrics")
        
        quality_data = {
            "Metric": ["Precision", "Recall", "F1 Score", "MRR", "NDCG"],
            "Description": ["Relevant results / Total results", "Relevant found / Total relevant", "Harmonic mean", "Mean reciprocal rank", "Normalized discounted gain"],
            "Target": ["> 0.8", "> 0.7", "> 0.75", "> 0.6", "> 0.7"]
        }
        
        df = pd.DataFrame(quality_data)
        st.table(df)
        
        st.markdown("#### 🎯 Implementation Tips")
        st.success("""
        1. **Document Preprocessing**: Clean and normalize text
        2. **Embedding Models**: Use domain-specific models
        3. **Hybrid Search**: Combine semantic and keyword search
        4. **Relevance Tuning**: Adjust similarity thresholds
        5. **User Feedback**: Learn from click and interaction data
        """)

def show_image_example():
    st.markdown("""
    ### Image Similarity Search - Visual Content Discovery
    
    Vector databases enable powerful image search by understanding visual similarity and content.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Image Search Demo")
        
        # Sample image database (simulated with feature vectors)
        images = {
            "Beach Sunset": {
                "description": "Beautiful sunset over ocean with palm trees",
                "vector": [0.8, 0.9, 0.1, 0.2, 0.7]  # [nature, warm, cool, bright, peaceful]
            },
            "Mountain Landscape": {
                "description": "Snow-capped mountains with clear blue sky",
                "vector": [0.9, 0.2, 0.8, 0.7, 0.6]
            },
            "City Skyline": {
                "description": "Modern city with tall buildings and lights",
                "vector": [0.1, 0.3, 0.2, 0.6, 0.4]
            },
            "Forest Path": {
                "description": "Winding path through dense green forest",
                "vector": [0.9, 0.4, 0.3, 0.2, 0.8]
            },
            "Urban Night": {
                "description": "City at night with neon lights and traffic",
                "vector": [0.0, 0.1, 0.1, 0.9, 0.3]
            }
        }
        
        # Query image selection
        query_image = st.selectbox("Find images similar to:", list(images.keys()))
        
        # Calculate similarities
        query_vector = images[query_image]["vector"]
        similarities = []
        
        for img_id, img_data in images.items():
            if img_id != query_image:
                # Cosine similarity
                dot_product = sum(a * b for a, b in zip(query_vector, img_data["vector"]))
                norm_query = (sum(a * a for a in query_vector)) ** 0.5
                norm_img = (sum(b * b for b in img_data["vector"])) ** 0.5
                similarity = dot_product / (norm_query * norm_img) if norm_query != 0 and norm_img != 0 else 0
                similarities.append((img_id, similarity, img_data))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("#### 📊 Similar Images")
        st.write(f"**Query Image**: {query_image}")
        st.write("**Similar Images:**")
        
        for i, (img_id, similarity, img_data) in enumerate(similarities, 1):
            st.write(f"{i}. **{img_id}** (Similarity: {similarity:.3f})")
            st.write(f"   *{img_data['description']}*")
        
        # Visualize image similarity
        features = ['Nature', 'Warm', 'Cool', 'Bright', 'Peaceful']
        
        fig = go.Figure()
        
        # Query image
        fig.add_trace(go.Scatterpolar(
            r=query_vector + [query_vector[0]],
            theta=features + [features[0]],
            fill='toself',
            name=query_image,
            line_color='red',
            line_width=3
        ))
        
        # Similar images
        colors = ['blue', 'green', 'orange', 'purple']
        for i, (img_id, similarity, img_data) in enumerate(similarities[:3]):
            fig.add_trace(go.Scatterpolar(
                r=img_data["vector"] + [img_data["vector"][0]],
                theta=features + [features[0]],
                fill='toself',
                name=f"{img_id} ({similarity:.3f})",
                line_color=colors[i % len(colors)],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Image Feature Similarity"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🖼️ Image Search Use Cases")
        
        st.markdown("**1. E-commerce Visual Search**")
        st.info("""
        - Upload image to find similar products
        - Fashion and home decor search
        - "Shop the look" functionality
        - Visual product recommendations
        """)
        
        st.markdown("**2. Content Management**")
        st.info("""
        - Find duplicate or similar images
        - Organize photo libraries
        - Content moderation and filtering
        - Digital asset management
        """)
        
        st.markdown("**3. Social Media**")
        st.info("""
        - Find similar posts and content
        - Trend analysis and discovery
        - Content recommendation
        - Duplicate content detection
        """)
        
        st.markdown("#### 🎨 Image Embedding Techniques")
        
        techniques_data = {
            "Technique": ["CNN Features", "CLIP", "ResNet", "EfficientNet"],
            "Description": ["Traditional CNN features", "Vision-language model", "Deep residual networks", "Efficient architecture"],
            "Dimensions": ["2048", "512", "2048", "1280"],
            "Best For": ["Visual similarity", "Text-image matching", "General features", "Mobile applications"]
        }
        
        df = pd.DataFrame(techniques_data)
        st.table(df)
        
        st.markdown("#### 🎯 Implementation Best Practices")
        st.success("""
        1. **Feature Extraction**: Use pre-trained models (CLIP, ResNet)
        2. **Preprocessing**: Normalize images and resize appropriately
        3. **Hybrid Search**: Combine visual and text features
        4. **Caching**: Cache embeddings for faster search
        5. **Indexing**: Use appropriate indexes for high-dimensional vectors
        """)

def show_usecase_comparison():
    st.markdown("### 📊 Use Case Comparison")
    
    # Comparison table
    comparison_data = {
        "Use Case": ["E-commerce Search", "Recommendations", "Document Retrieval", "Image Search"],
        "Vector Type": ["Product embeddings", "User/item vectors", "Text embeddings", "Image embeddings"],
        "Dimensions": ["128-1536", "64-512", "384-1536", "512-2048"],
        "Query Frequency": ["High", "Very High", "Medium", "Medium"],
        "Accuracy Needs": ["High", "Very High", "High", "Medium"],
        "Real-time": ["Yes", "Yes", "No", "No"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    st.markdown("### 🎯 Use Case Selection Guide")
    
    use_case = st.selectbox(
        "What's your primary application?",
        ["Product Search", "Personalization", "Information Retrieval", "Visual Search", "Content Discovery"]
    )
    
    if use_case == "Product Search":
        st.success("**Recommended: E-commerce Search** - Focus on product embeddings and similarity metrics")
    elif use_case == "Personalization":
        st.success("**Recommended: Recommendation Systems** - Use collaborative and content-based filtering")
    elif use_case == "Information Retrieval":
        st.success("**Recommended: Document Retrieval** - Implement semantic search with text embeddings")
    elif use_case == "Visual Search":
        st.success("**Recommended: Image Search** - Use computer vision models for feature extraction")
    elif use_case == "Content Discovery":
        st.success("**Recommended: Hybrid Approach** - Combine multiple techniques for comprehensive search")
