import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Import query functions
from query_functions import show_knn_demo, show_range_queries, show_ann_demo, show_query_comparison

# Import performance functions
from performance_functions import show_memory_optimization, show_computational_optimization, show_query_optimization, show_performance_monitoring

# Import technology and example functions
from technology_examples import (
    show_qdrant_details, show_pinecone_details, show_pgvector_details, show_chroma_details, show_technology_comparison,
    show_ecommerce_example, show_recommendation_example, show_document_example, show_image_example, show_usecase_comparison
)

def show_embedding_models():
    st.markdown('<h2 class="section-header">🧠 Embedding Models</h2>', unsafe_allow_html=True)
    
    model_type = st.selectbox(
        "Choose an embedding model to explore:",
        ["BERT (768D)", "OpenAI Embeddings (1536D)", "Comparison", "When to Use Each"]
    )
    
    if model_type == "BERT (768D)":
        show_bert_details()
    elif model_type == "OpenAI Embeddings (1536D)":
        show_openai_details()
    elif model_type == "Comparison":
        show_model_comparison()
    elif model_type == "When to Use Each":
        show_model_selection_guide()

def show_bert_details():
    st.markdown("""
    ### BERT (768D) - Context-Aware Transformer
    
    BERT (Bidirectional Encoder Representations from Transformers) is a revolutionary 
    language model that understands context by reading text in both directions.
    
    **Key Features:**
    - **768 Dimensions**: 12 transformer layers × 64 attention heads
    - **Bidirectional**: Reads text left-to-right AND right-to-left
    - **Pre-trained**: Already knows general language patterns
    - **Context-aware**: Understands "bank" (river) vs "bank" (financial)
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 BERT Embedding Process")
        
        text_input = st.text_input("Enter text to see BERT embedding:", "The cat sat on the mat")
        
        if text_input:
            # Simulate BERT embedding (simplified)
            st.markdown("**Step 1: Tokenization**")
            tokens = text_input.split()
            st.write(f"Tokens: {tokens}")
            
            st.markdown("**Step 2: Add Special Tokens**")
            tokens_with_special = ["[CLS]"] + tokens + ["[SEP]"]
            st.write(f"With special tokens: {tokens_with_special}")
            
            st.markdown("**Step 3: Generate 768D Embedding**")
            # Simulate embedding values
            embedding = np.random.randn(768) * 0.1
            st.write(f"Embedding shape: {embedding.shape}")
            st.write(f"Sample values: {embedding[:5]}")
            
            # Visualize embedding dimensions
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=embedding[:50],  # Show first 50 dimensions
                mode='lines+markers',
                name='BERT Embedding',
                line=dict(color='blue', width=2)
            ))
            fig.update_layout(
                title='BERT Embedding (First 50 Dimensions)',
                xaxis_title='Dimension',
                yaxis_title='Value'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 BERT Characteristics")
        
        # Performance metrics
        metrics = {
            "Dimensions": "768",
            "Model Size": "110M parameters",
            "Training Data": "Books + Wikipedia",
            "Context Window": "512 tokens",
            "Languages": "100+ languages"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ BERT Strengths")
        st.success("""
        - **Context Awareness**: Understands word meaning based on context
        - **Bidirectional**: Better understanding than unidirectional models
        - **Pre-trained**: Ready to use without training from scratch
        - **Fine-tunable**: Can be adapted for specific tasks
        """)
        
        st.markdown("#### ❌ BERT Limitations")
        st.error("""
        - **Fixed Length**: All sentences become 768 dimensions
        - **Computational Cost**: Expensive to run
        - **Context Window**: Limited to 512 tokens
        - **Static**: Doesn't update with new information
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Local development and testing
        - Privacy-sensitive applications
        - Domain-specific fine-tuning
        - Cost-sensitive projects
        """)

def show_openai_details():
    st.markdown("""
    ### OpenAI Embeddings (1536D) - Modern Language Understanding
    
    OpenAI's text-embedding-ada-002 is a state-of-the-art embedding model optimized 
    for semantic similarity and search tasks.
    
    **Key Features:**
    - **1536 Dimensions**: Based on GPT-3.5 architecture
    - **Semantic Understanding**: Excellent at finding similar meanings
    - **Multilingual**: Works across many languages
    - **Optimized**: Specifically tuned for retrieval tasks
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 OpenAI Embedding Process")
        
        text_input = st.text_input("Enter text for OpenAI embedding:", "Machine learning is fascinating", key="openai_input")
        
        if text_input:
            # Simulate OpenAI embedding (simplified)
            st.markdown("**Step 1: Send to OpenAI API**")
            st.code(f"""
response = openai.Embedding.create(
    input="{text_input}",
    model="text-embedding-ada-002"
)
            """)
            
            st.markdown("**Step 2: Extract 1536D Embedding**")
            # Simulate embedding values
            embedding = np.random.randn(1536) * 0.1
            st.write(f"Embedding shape: {embedding.shape}")
            st.write(f"Sample values: {embedding[:5]}")
            
            # Visualize embedding dimensions
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=embedding[:50],  # Show first 50 dimensions
                mode='lines+markers',
                name='OpenAI Embedding',
                line=dict(color='green', width=2)
            ))
            fig.update_layout(
                title='OpenAI Embedding (First 50 Dimensions)',
                xaxis_title='Dimension',
                yaxis_title='Value'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 OpenAI Characteristics")
        
        # Performance metrics
        metrics = {
            "Dimensions": "1536",
            "Model Size": "175B parameters",
            "Training Data": "Internet text",
            "Context Window": "8192 tokens",
            "Languages": "100+ languages"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ OpenAI Strengths")
        st.success("""
        - **Semantic Understanding**: Excellent at finding similar meanings
        - **Multilingual**: Works across many languages
        - **Optimized**: Specifically tuned for retrieval tasks
        - **Consistent**: Produces stable, reliable embeddings
        """)
        
        st.markdown("#### ❌ OpenAI Limitations")
        st.error("""
        - **API Dependency**: Requires internet connection
        - **Cost**: Pay per API call
        - **Privacy**: Text sent to external service
        - **Rate Limits**: Limited requests per minute
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Production search systems
        - Multilingual applications
        - Best semantic understanding
        - Cloud-based applications
        """)

def show_model_comparison():
    st.markdown("### 📊 BERT vs OpenAI Embeddings Comparison")
    
    # Create comparison table
    comparison_data = {
        "Feature": ["Dimensions", "Model Size", "API Required", "Cost", "Privacy", "Context Window", "Best For"],
        "BERT": ["768", "110M params", "No", "Free (local)", "Local processing", "512 tokens", "Development"],
        "OpenAI": ["1536", "175B params", "Yes", "Pay per use", "External service", "8192 tokens", "Production"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎯 Performance Comparison")
        
        # Simulate similarity scores for same documents
        documents = ["The cat sat on the mat", "A feline rested on the rug", "The dog ran in the park"]
        
        st.markdown("**Document Similarities:**")
        
        # BERT similarities (simulated)
        bert_similarities = [1.0, 0.85, 0.23]
        
        # OpenAI similarities (simulated)
        openai_similarities = [1.0, 0.92, 0.18]
        
        for i, doc in enumerate(documents):
            st.write(f"**{doc}**")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("BERT", f"{bert_similarities[i]:.2f}")
            with col_b:
                st.metric("OpenAI", f"{openai_similarities[i]:.2f}")
        
        st.info("💡 OpenAI finds higher similarity for semantically similar text")
    
    with col2:
        st.markdown("#### 💾 Memory Usage Comparison")
        
        dimensions = st.slider("Vector dimensions:", 100, 2000, 768)
        num_vectors = st.slider("Number of vectors:", 1000, 1000000, 100000)
        
        bert_memory = dimensions * num_vectors * 4  # 32-bit float
        openai_memory = 1536 * num_vectors * 4      # OpenAI is always 1536D
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("BERT Storage", f"{bert_memory / (1024**2):.1f} MB")
        with col_b:
            st.metric("OpenAI Storage", f"{openai_memory / (1024**2):.1f} MB")
        
        if bert_memory < openai_memory:
            st.success(f"💡 BERT saves {((openai_memory - bert_memory) / openai_memory * 100):.1f}% storage!")
        else:
            st.warning("OpenAI uses more storage due to higher dimensions")

def show_model_selection_guide():
    st.markdown("### 🎯 When to Use Each Model")
    
    use_case = st.selectbox(
        "Select your use case:",
        [
            "Local Development",
            "Production Search System", 
            "Multilingual Application",
            "Privacy-Sensitive Project",
            "High-Volume Processing",
            "Best Accuracy Needed",
            "Cost-Sensitive Project"
        ]
    )
    
    if use_case == "Local Development":
        st.success("""
        **Recommended: BERT**
        
        ✅ **Why BERT:**
        - No API costs during development
        - Can run offline
        - Easy to test and iterate
        - Good for prototyping
        
        ❌ **Why not OpenAI:**
        - API costs add up during development
        - Requires internet connection
        - Rate limits can slow development
        """)
        
    elif use_case == "Production Search System":
        st.success("""
        **Recommended: OpenAI**
        
        ✅ **Why OpenAI:**
        - Better semantic understanding
        - Optimized for search tasks
        - Consistent, reliable embeddings
        - Handles complex queries well
        
        ❌ **Why not BERT:**
        - May need fine-tuning for optimal performance
        - Lower semantic accuracy
        - Requires more computational resources
        """)
        
    elif use_case == "Multilingual Application":
        st.success("""
        **Recommended: OpenAI**
        
        ✅ **Why OpenAI:**
        - Better multilingual support
        - Consistent across languages
        - Handles code-switching well
        - Pre-trained on diverse data
        
        ❌ **Why not BERT:**
        - May need language-specific models
        - Varying quality across languages
        - More complex setup for multilingual
        """)
        
    elif use_case == "Privacy-Sensitive Project":
        st.success("""
        **Recommended: BERT**
        
        ✅ **Why BERT:**
        - Data stays local
        - No external API calls
        - Full control over processing
        - Compliance with data regulations
        
        ❌ **Why not OpenAI:**
        - Text sent to external service
        - Potential privacy concerns
        - Data leaves your control
        """)
        
    elif use_case == "High-Volume Processing":
        st.success("""
        **Recommended: BERT**
        
        ✅ **Why BERT:**
        - Lower cost per embedding
        - No API rate limits
        - Can batch process efficiently
        - Predictable costs
        
        ❌ **Why not OpenAI:**
        - API costs scale with volume
        - Rate limits may slow processing
        - Unpredictable costs at scale
        """)
        
    elif use_case == "Best Accuracy Needed":
        st.success("""
        **Recommended: OpenAI**
        
        ✅ **Why OpenAI:**
        - Superior semantic understanding
        - Better performance on similarity tasks
        - More sophisticated training
        - Optimized for accuracy
        
        ❌ **Why not BERT:**
        - May require fine-tuning for best results
        - Lower baseline accuracy
        - More complex optimization needed
        """)
        
    elif use_case == "Cost-Sensitive Project":
        st.success("""
        **Recommended: BERT**
        
        ✅ **Why BERT:**
        - Free to run locally
        - No per-request costs
        - Predictable infrastructure costs
        - Good ROI for many use cases
        
        ❌ **Why not OpenAI:**
        - Pay per API call
        - Costs can add up quickly
        - Unpredictable monthly bills
        """)
    
    # Decision matrix
    st.markdown("### 📋 Quick Decision Matrix")
    
    decision_data = {
        "Factor": ["Local Processing", "Best Accuracy", "Multilingual", "Privacy", "Cost", "Production Ready"],
        "BERT": ["✅", "⚠️", "⚠️", "✅", "✅", "⚠️"],
        "OpenAI": ["❌", "✅", "✅", "❌", "❌", "✅"]
    }
    
    df = pd.DataFrame(decision_data)
    st.table(df)

def show_index_types():
    st.markdown('<h2 class="section-header">🏗️ Index Types</h2>', unsafe_allow_html=True)
    
    index_type = st.selectbox(
        "Choose an index type to explore:",
        ["HNSW (Hierarchical Navigable Small World)", "LSH (Locality-Sensitive Hashing)", 
         "Product Quantization", "Comparison & Selection Guide"]
    )
    
    if "HNSW" in index_type:
        show_hnsw_details()
    elif "LSH" in index_type:
        show_lsh_details()
    elif "Product Quantization" in index_type:
        show_pq_details()
    elif "Comparison" in index_type:
        show_index_comparison()

def show_hnsw_details():
    st.markdown("""
    ### HNSW - Hierarchical Navigable Small World
    
    HNSW creates a multi-level graph where each level has different connection densities.
    Think of it like a social network with different levels of connections.
    
    **How it works:**
    - **Level 0 (Dense)**: Everyone knows their neighbors
    - **Level 1 (Medium)**: Only key people know each other  
    - **Level 2 (Sparse)**: Only the most important people are connected
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive HNSW Visualization")
        
        # Simulate HNSW levels
        num_vectors = st.slider("Number of vectors:", 10, 100, 20)
        
        # Generate random 2D points
        np.random.seed(42)
        points = np.random.rand(num_vectors, 2)
        
        # Create visualization
        fig = go.Figure()
        
        # Level 0 - Dense connections
        fig.add_trace(go.Scatter(
            x=points[:, 0],
            y=points[:, 1],
            mode='markers+lines',
            name='Level 0 (Dense)',
            line=dict(color='blue', width=1),
            marker=dict(size=8, color='blue')
        ))
        
        # Level 1 - Medium connections (subset)
        level1_indices = np.random.choice(num_vectors, num_vectors//2, replace=False)
        level1_points = points[level1_indices]
        
        fig.add_trace(go.Scatter(
            x=level1_points[:, 0],
            y=level1_points[:, 1],
            mode='markers+lines',
            name='Level 1 (Medium)',
            line=dict(color='green', width=2),
            marker=dict(size=10, color='green')
        ))
        
        # Level 2 - Sparse connections (small subset)
        level2_indices = np.random.choice(level1_indices, len(level1_indices)//3, replace=False)
        level2_points = points[level2_indices]
        
        fig.add_trace(go.Scatter(
            x=level2_points[:, 0],
            y=level2_points[:, 1],
            mode='markers+lines',
            name='Level 2 (Sparse)',
            line=dict(color='red', width=3),
            marker=dict(size=12, color='red')
        ))
        
        fig.update_layout(
            title='HNSW Multi-Level Graph Structure',
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 HNSW Characteristics")
        
        metrics = {
            "Search Complexity": "O(log n)",
            "Construction Time": "O(n log n)",
            "Memory Usage": "High",
            "Accuracy": "Very High",
            "Update Speed": "Slow",
            "Best For": "High-dimensional data"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ HNSW Strengths")
        st.success("""
        - **Excellent Performance**: Very fast search in high dimensions
        - **High Accuracy**: Finds very similar vectors
        - **Production Ready**: Used in many production systems
        - **Scalable**: Works well with millions of vectors
        """)
        
        st.markdown("#### ❌ HNSW Limitations")
        st.error("""
        - **Memory Intensive**: Uses significant memory
        - **Complex Construction**: Takes time to build
        - **Slow Updates**: Hard to add new vectors
        - **Parameter Sensitive**: Requires tuning
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Production similarity search
        - High-dimensional embeddings
        - When accuracy is critical
        - Large-scale applications
        """)

def show_lsh_details():
    st.markdown("""
    ### LSH - Locality-Sensitive Hashing
    
    LSH puts similar vectors into the same "buckets" using special hash functions.
    Think of it like a smart filing system where similar documents go in the same folder.
    
    **How it works:**
    - Similar vectors get the same hash value
    - They end up in the same bucket
    - Search only looks in relevant buckets
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive LSH Demonstration")
        
        # Create sample vectors
        vectors = [
            [0.8, 0.6, 0.1],  # Movie: Action + Comedy
            [0.7, 0.5, 0.2],  # Similar movie
            [0.1, 0.2, 0.9],  # Movie: Romance
            [0.2, 0.1, 0.8],  # Similar romance movie
            [0.9, 0.1, 0.1],  # Movie: Pure action
        ]
        
        vector_names = ["Action-Comedy 1", "Action-Comedy 2", "Romance 1", "Romance 2", "Pure Action"]
        
        # Simple LSH hash function (sum of vector components)
        def simple_lsh_hash(vector):
            return int(sum(vector)) % 3  # 3 buckets
        
        # Calculate hashes
        hashes = [simple_lsh_hash(v) for v in vectors]
        
        # Create visualization
        fig = go.Figure()
        
        colors = ['red', 'green', 'blue']
        for i, (vector, name, hash_val) in enumerate(zip(vectors, vector_names, hashes)):
            fig.add_trace(go.Scatter3d(
                x=[vector[0]],
                y=[vector[1]], 
                z=[vector[2]],
                mode='markers+text',
                marker=dict(size=10, color=colors[hash_val]),
                text=[name],
                textposition="top center",
                name=f"Bucket {hash_val}"
            ))
        
        fig.update_layout(
            scene=dict(
                xaxis_title="Action",
                yaxis_title="Comedy", 
                zaxis_title="Romance"
            ),
            title="LSH Bucket Assignment"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show bucket contents
        st.markdown("#### 🪣 Bucket Contents")
        buckets = {}
        for vector, name, hash_val in zip(vectors, vector_names, hashes):
            if hash_val not in buckets:
                buckets[hash_val] = []
            buckets[hash_val].append(name)
        
        for bucket_id, movies in buckets.items():
            st.write(f"**Bucket {bucket_id}**: {', '.join(movies)}")
    
    with col2:
        st.markdown("#### 📊 LSH Characteristics")
        
        metrics = {
            "Search Complexity": "O(1) average",
            "Construction Time": "O(n)",
            "Memory Usage": "Low",
            "Accuracy": "Good (approximate)",
            "Update Speed": "Fast",
            "Best For": "High-dimensional data"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ LSH Strengths")
        st.success("""
        - **Very Fast**: O(1) average search time
        - **Memory Efficient**: Low memory usage
        - **Scalable**: Works with huge datasets
        - **Fast Updates**: Easy to add new vectors
        """)
        
        st.markdown("#### ❌ LSH Limitations")
        st.error("""
        - **Approximate**: May miss some similar vectors
        - **Parameter Sensitive**: Requires careful tuning
        - **Hash Collisions**: Different vectors may hash to same bucket
        - **Quality Trade-off**: Speed vs accuracy balance
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Large-scale similarity search
        - When approximate results are OK
        - Real-time applications
        - Memory-constrained environments
        """)

def show_pq_details():
    st.markdown("""
    ### Product Quantization - The Compression Approach
    
    Product Quantization compresses vectors into short codes by splitting them into 
    sub-vectors and replacing each with a code. Think of it like using ZIP codes 
    instead of full addresses.
    
    **How it works:**
    - Split vector into sub-vectors
    - Create codebook for each sub-vector
    - Replace sub-vectors with codes
    - Store only the codes
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive PQ Demonstration")
        
        # Original vector
        original_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        st.markdown(f"**Original Vector (8D)**: {original_vector}")
        
        # Split into sub-vectors
        sub_vector_1 = original_vector[:4]  # First 4 dimensions
        sub_vector_2 = original_vector[4:]  # Last 4 dimensions
        
        st.markdown(f"**Sub-vector 1**: {sub_vector_1}")
        st.markdown(f"**Sub-vector 2**: {sub_vector_2}")
        
        # Simulate quantization (simplified)
        # In reality, you'd use k-means clustering to create codebooks
        code_1 = "A"  # Code for sub-vector 1
        code_2 = "B"  # Code for sub-vector 2
        
        st.markdown(f"**Code 1**: {code_1}")
        st.markdown(f"**Code 2**: {code_2}")
        
        st.markdown(f"**Final PQ Code**: {code_1 + code_2}")
        
        # Show compression
        original_size = len(original_vector) * 4  # 32-bit floats
        pq_size = 2 * 1  # 2 codes of 1 byte each
        
        st.markdown("#### 💾 Compression Results")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Original Size", f"{original_size} bytes")
        with col_b:
            st.metric("PQ Size", f"{pq_size} bytes")
        
        compression_ratio = (original_size - pq_size) / original_size * 100
        st.success(f"💡 Compression saves {compression_ratio:.1f}% storage!")
        
        # Visualization
        fig = go.Figure()
        
        # Original vector
        fig.add_trace(go.Bar(
            name='Original Vector',
            x=[f'Dim {i+1}' for i in range(len(original_vector))],
            y=original_vector,
            marker_color='blue'
        ))
        
        # PQ codes
        fig.add_trace(go.Bar(
            name='PQ Codes',
            x=['Code 1', 'Code 2'],
            y=[0.5, 0.5],  # Placeholder values for visualization
            marker_color='red'
        ))
        
        fig.update_layout(
            title='Vector Compression with Product Quantization',
            xaxis_title='Components',
            yaxis_title='Values',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 PQ Characteristics")
        
        metrics = {
            "Search Complexity": "O(log n)",
            "Construction Time": "O(n)",
            "Memory Usage": "Very Low",
            "Accuracy": "Good (with some loss)",
            "Update Speed": "Medium",
            "Best For": "Large datasets"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ PQ Strengths")
        st.success("""
        - **Massive Compression**: 75-90% storage savings
        - **Fast Distance**: Quick distance calculations
        - **Scalable**: Works with huge datasets
        - **Memory Efficient**: Very low memory usage
        """)
        
        st.markdown("#### ❌ PQ Limitations")
        st.error("""
        - **Accuracy Loss**: Some precision is lost
        - **Complex Setup**: Requires careful parameter tuning
        - **Codebook Size**: Must choose appropriate codebook size
        - **Reconstruction**: Cannot perfectly reconstruct original
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Large-scale datasets with memory constraints
        - When some accuracy loss is acceptable
        - Mobile and embedded applications
        - Cost-sensitive deployments
        """)

def show_index_comparison():
    st.markdown("### 📊 Index Type Comparison")
    
    # Comparison table
    comparison_data = {
        "Index Type": ["HNSW", "LSH", "Product Quantization", "KD-Tree"],
        "Search Speed": ["Very Fast", "Very Fast", "Fast", "Medium"],
        "Memory Usage": ["High", "Low", "Very Low", "Medium"],
        "Accuracy": ["Very High", "Good", "Good", "High"],
        "Construction": ["Slow", "Fast", "Medium", "Medium"],
        "Updates": ["Slow", "Fast", "Medium", "Slow"],
        "Best For": ["Production", "Large scale", "Memory constrained", "Low dimensions"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    st.markdown("### 🎯 Selection Guide")
    
    use_case = st.selectbox(
        "What's your primary concern?",
        ["Best Accuracy", "Fastest Speed", "Lowest Memory", "Easiest to Use", "Large Dataset"]
    )
    
    if use_case == "Best Accuracy":
        st.success("**Recommended: HNSW** - Highest accuracy for similarity search")
    elif use_case == "Fastest Speed":
        st.success("**Recommended: LSH** - Fastest search with good accuracy")
    elif use_case == "Lowest Memory":
        st.success("**Recommended: Product Quantization** - Massive memory savings")
    elif use_case == "Easiest to Use":
        st.success("**Recommended: KD-Tree** - Simple and well-understood")
    elif use_case == "Large Dataset":
        st.success("**Recommended: LSH or Product Quantization** - Scale to millions of vectors")

# Query Types Module
def show_query_types():
    st.markdown('<h2 class="section-header">🔍 Query Types</h2>', unsafe_allow_html=True)
    
    query_type = st.selectbox(
        "Choose a query type to explore:",
        ["K-Nearest Neighbors (KNN)", "Range Queries", "Approximate Nearest Neighbors (ANN)", "Query Comparison"]
    )
    
    if "KNN" in query_type:
        show_knn_demo()
    elif "Range" in query_type:
        show_range_queries()
    elif "ANN" in query_type:
        show_ann_demo()
    elif "Comparison" in query_type:
        show_query_comparison()

def show_performance_optimization():
    st.markdown('<h2 class="section-header">⚡ Performance Optimization</h2>', unsafe_allow_html=True)
    
    optimization_type = st.selectbox(
        "Choose an optimization area:",
        ["Memory Optimization", "Computational Optimization", "Query Optimization", "Performance Monitoring"]
    )
    
    if "Memory" in optimization_type:
        show_memory_optimization()
    elif "Computational" in optimization_type:
        show_computational_optimization()
    elif "Query" in optimization_type:
        show_query_optimization()
    elif "Monitoring" in optimization_type:
        show_performance_monitoring()

def show_popular_technologies():
    st.markdown('<h2 class="section-header">🌐 Popular Technologies</h2>', unsafe_allow_html=True)
    
    technology = st.selectbox(
        "Choose a vector database technology:",
        ["Qdrant", "Pinecone", "PG Vector", "Chroma", "Technology Comparison"]
    )
    
    if technology == "Qdrant":
        show_qdrant_details()
    elif technology == "Pinecone":
        show_pinecone_details()
    elif technology == "PG Vector":
        show_pgvector_details()
    elif technology == "Chroma":
        show_chroma_details()
    elif technology == "Technology Comparison":
        show_technology_comparison()

def show_real_world_examples():
    st.markdown('<h2 class="section-header">💼 Real-World Examples</h2>', unsafe_allow_html=True)
    
    example_type = st.selectbox(
        "Choose a real-world example:",
        ["E-commerce Product Search", "Recommendation Systems", "Document Retrieval", "Image Similarity Search", "Use Case Comparison"]
    )
    
    if "E-commerce" in example_type:
        show_ecommerce_example()
    elif "Recommendation" in example_type:
        show_recommendation_example()
    elif "Document" in example_type:
        show_document_example()
    elif "Image" in example_type:
        show_image_example()
    elif "Comparison" in example_type:
        show_usecase_comparison()
