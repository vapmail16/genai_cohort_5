import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import random

# Import our custom modules
from app_modules import (
    show_embedding_models, show_index_types, 
    show_query_types, show_performance_optimization,
    show_popular_technologies, show_real_world_examples
)

# Page configuration
st.set_page_config(
    page_title="Vector Databases Interactive Tutorial",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
def main():
    st.markdown('<h1 class="main-header">🔍 Vector Databases Interactive Tutorial</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📚 Learning Modules")
    
    page = st.sidebar.selectbox(
        "Choose a module:",
        [
            "🏠 Home",
            "📐 Vector Fundamentals", 
            "🎯 Similarity Metrics",
            "🧠 Embedding Models",
            "🏗️ Index Types",
            "🔍 Query Types",
            "⚡ Performance Optimization",
            "🌐 Popular Technologies",
            "💼 Real-World Examples"
        ]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📐 Vector Fundamentals":
        show_vector_fundamentals()
    elif page == "🎯 Similarity Metrics":
        show_similarity_metrics()
    elif page == "🧠 Embedding Models":
        show_embedding_models()
    elif page == "🏗️ Index Types":
        show_index_types()
    elif page == "🔍 Query Types":
        show_query_types()
    elif page == "⚡ Performance Optimization":
        show_performance_optimization()
    elif page == "🌐 Popular Technologies":
        show_popular_technologies()
    elif page == "💼 Real-World Examples":
        show_real_world_examples()

def show_home():
    st.markdown("""
    ## Welcome to the Vector Databases Interactive Tutorial! 🚀
    
    This interactive application will help you understand vector databases through hands-on examples, 
    visualizations, and practical demonstrations.
    
    ### What You'll Learn:
    - **Vector Fundamentals**: Understanding dimensions, embeddings, and vector operations
    - **Similarity Metrics**: Cosine similarity, Euclidean distance, and when to use each
    - **Embedding Models**: BERT, OpenAI, and other popular models
    - **Index Types**: HNSW, LSH, and other indexing strategies
    - **Query Types**: KNN, range queries, and approximate search
    - **Performance Optimization**: Memory, computation, and query optimization
    - **Popular Technologies**: Qdrant, Pinecone, PG Vector, and Chroma
    - **Real-World Examples**: Practical applications and use cases
    
    ### How to Use This Tutorial:
    1. **Navigate** through modules using the sidebar
    2. **Interact** with visualizations and examples
    3. **Experiment** with different parameters
    4. **Learn** through hands-on practice
    
    ### Getting Started:
    Start with "Vector Fundamentals" to build your foundation, then explore other modules based on your interests.
    
    ---
    
    **Pro Tip**: Use the sidebar to navigate between modules. Each module builds on previous concepts!
    """)

def show_vector_fundamentals():
    st.markdown('<h2 class="section-header">📐 Vector Fundamentals</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### What are Vectors?
        
        Vectors are mathematical objects that represent data points in multi-dimensional space.
        Each vector contains a list of numbers that describe different features or characteristics.
        
        **Example**: A movie vector might be:
        `[0.8, 0.6, 0.1, 0.2]` representing:
        - Action: 0.8 (high)
        - Comedy: 0.6 (medium)
        - Romance: 0.1 (low)
        - Horror: 0.2 (low)
        """)
        
        # Interactive vector creation
        st.markdown("### 🎮 Create Your Own Vector")
        
        dimensions = st.slider("Number of dimensions:", 2, 10, 4)
        
        vector_values = []
        for i in range(dimensions):
            value = st.slider(f"Dimension {i+1}:", 0.0, 1.0, 0.5)
            vector_values.append(value)
        
        st.write("Your vector:", vector_values)
        
        # Visualize the vector
        if dimensions <= 3:
            fig = go.Figure()
            
            if dimensions == 2:
                fig.add_trace(go.Scatter(
                    x=[0, vector_values[0]], 
                    y=[0, vector_values[1]],
                    mode='lines+markers',
                    name='Vector',
                    line=dict(color='red', width=5),
                    marker=dict(size=10)
                ))
                fig.update_layout(
                    xaxis_title="Dimension 1",
                    yaxis_title="Dimension 2",
                    title="2D Vector Visualization"
                )
            elif dimensions == 3:
                fig.add_trace(go.Scatter3d(
                    x=[0, vector_values[0]], 
                    y=[0, vector_values[1]], 
                    z=[0, vector_values[2]],
                    mode='lines+markers',
                    name='Vector',
                    line=dict(color='red', width=5),
                    marker=dict(size=10)
                ))
                fig.update_layout(
                    scene=dict(
                        xaxis_title="Dimension 1",
                        yaxis_title="Dimension 2",
                        zaxis_title="Dimension 3"
                    ),
                    title="3D Vector Visualization"
                )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Understanding Dimensions
        
        **Dimensions** represent the number of numerical values in a vector.
        
        #### Dimension Types:
        - **Low (1-10)**: Simple features, coordinates
        - **Medium (10-1000)**: Traditional ML features
        - **High (1000+)**: Neural network embeddings
        
        #### The Curse of Dimensionality:
        As dimensions increase:
        - Volume grows exponentially
        - Distance calculations become expensive
        - All points become equidistant
        - Search becomes slower
        """)
        
        # Dimension comparison
        st.markdown("### 📊 Dimension Comparison")
        
        dimension_type = st.selectbox(
            "Select dimension type:",
            ["Low (2D)", "Medium (50D)", "High (1000D)"]
        )
        
        if dimension_type == "Low (2D)":
            st.info("✅ Easy to visualize, fast computation")
        elif dimension_type == "Medium (50D)":
            st.warning("⚠️ Good balance of expressiveness and efficiency")
        else:
            st.error("❌ High computational cost, curse of dimensionality")
        
        # Storage comparison
        st.markdown("### 💾 Storage Comparison")
        
        dimensions = st.slider("Vector dimensions:", 100, 2000, 768)
        num_vectors = st.slider("Number of vectors:", 1000, 1000000, 100000)
        
        storage_32bit = dimensions * num_vectors * 4  # 32-bit float
        storage_8bit = dimensions * num_vectors * 1   # 8-bit quantized
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("32-bit Storage", f"{storage_32bit / (1024**2):.1f} MB")
        with col_b:
            st.metric("8-bit Storage", f"{storage_8bit / (1024**2):.1f} MB")
        
        savings = ((storage_32bit - storage_8bit) / storage_32bit) * 100
        st.success(f"💡 Quantization saves {savings:.1f}% storage!")

def show_similarity_metrics():
    st.markdown('<h2 class="section-header">🎯 Similarity Metrics</h2>', unsafe_allow_html=True)
    
    # Metric selection
    metric_type = st.selectbox(
        "Choose a similarity metric to explore:",
        ["Cosine Similarity", "Euclidean Distance", "Dot Product", "Manhattan Distance"]
    )
    
    if metric_type == "Cosine Similarity":
        show_cosine_similarity()
    elif metric_type == "Euclidean Distance":
        show_euclidean_distance()
    elif metric_type == "Dot Product":
        show_dot_product()
    elif metric_type == "Manhattan Distance":
        show_manhattan_distance()

def show_cosine_similarity():
    st.markdown("""
    ### Cosine Similarity - The Angle-Based Approach
    
    Cosine similarity measures the **angle** between two vectors, not their magnitude.
    It's perfect for finding similar **patterns** regardless of intensity.
    
    **Formula**: `cos(θ) = (A·B) / (||A|| × ||B||)`
    **Range**: [-1, 1] where 1 = identical direction, 0 = perpendicular, -1 = opposite
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Example")
        
        # Create two vectors
        st.markdown("**Vector A (Person 1's movie preferences):**")
        a1 = st.slider("Action movies:", 0.0, 1.0, 0.8)
        a2 = st.slider("Comedy movies:", 0.0, 1.0, 0.6)
        a3 = st.slider("Romance movies:", 0.0, 1.0, 0.1)
        a4 = st.slider("Horror movies:", 0.0, 1.0, 0.2)
        
        vector_a = [a1, a2, a3, a4]
        
        st.markdown("**Vector B (Person 2's movie preferences):**")
        b1 = st.slider("Action movies:", 0.0, 1.0, 0.4, key="b1")
        b2 = st.slider("Comedy movies:", 0.0, 1.0, 0.3, key="b2")
        b3 = st.slider("Romance movies:", 0.0, 1.0, 0.1, key="b3")
        b4 = st.slider("Horror movies:", 0.0, 1.0, 0.1, key="b4")
        
        vector_b = [b1, b2, b3, b4]
        
        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))
        cosine_sim = dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0
        
        st.markdown("#### 📊 Results")
        st.metric("Cosine Similarity", f"{cosine_sim:.3f}")
        
        if cosine_sim > 0.8:
            st.success("🎯 Very similar preferences!")
        elif cosine_sim > 0.5:
            st.info("👍 Somewhat similar preferences")
        elif cosine_sim > 0.0:
            st.warning("🤔 Different preferences")
        else:
            st.error("❌ Opposite preferences")
    
    with col2:
        st.markdown("#### 📈 Visualization")
        
        # Create radar chart
        categories = ['Action', 'Comedy', 'Romance', 'Horror']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=vector_a + [vector_a[0]],  # Close the radar chart
            theta=categories + [categories[0]],
            fill='toself',
            name='Person A',
            line_color='blue'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=vector_b + [vector_b[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Person B',
            line_color='red'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Movie Preference Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        #### 💡 Key Insights
        
        **Why Cosine Similarity?**
        - Ignores magnitude (how strong preferences are)
        - Focuses on pattern (what they prefer)
        - Perfect for recommendation systems
        - Works well with normalized embeddings
        
        **Real-world example**: Both people love action > comedy > romance > horror,
        even though Person A has stronger preferences than Person B.
        """)

def show_euclidean_distance():
    st.markdown("""
    ### Euclidean Distance - The Straight-Line Approach
    
    Euclidean distance measures the **straight-line distance** between two points.
    It's perfect when you care about **actual values**, not just patterns.
    
    **Formula**: `√(Σ(Aᵢ - Bᵢ)²)`
    **Range**: [0, ∞) where 0 = identical, larger = more different
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Example")
        
        st.markdown("**House A Features:**")
        a1 = st.slider("Price ($1000s):", 100, 1000, 500, key="price_a")
        a2 = st.slider("Size (sq ft):", 1000, 5000, 2000, key="size_a")
        a3 = st.slider("Bedrooms:", 1, 6, 3, key="bed_a")
        a4 = st.slider("Bathrooms:", 1, 4, 2, key="bath_a")
        
        vector_a = [a1, a2, a3, a4]
        
        st.markdown("**House B Features:**")
        b1 = st.slider("Price ($1000s):", 100, 1000, 600, key="price_b")
        b2 = st.slider("Size (sq ft):", 1000, 5000, 2200, key="size_b")
        b3 = st.slider("Bedrooms:", 1, 6, 4, key="bed_b")
        b4 = st.slider("Bathrooms:", 1, 4, 3, key="bath_b")
        
        vector_b = [b1, b2, b3, b4]
        
        # Calculate Euclidean distance
        euclidean_dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(vector_a, vector_b)))
        
        st.markdown("#### 📊 Results")
        st.metric("Euclidean Distance", f"{euclidean_dist:.2f}")
        
        if euclidean_dist < 100:
            st.success("🏠 Very similar houses!")
        elif euclidean_dist < 300:
            st.info("👍 Somewhat similar houses")
        elif euclidean_dist < 500:
            st.warning("🤔 Different houses")
        else:
            st.error("❌ Very different houses")
    
    with col2:
        st.markdown("#### 📈 Visualization")
        
        # Create bar chart comparing features
        features = ['Price', 'Size', 'Bedrooms', 'Bathrooms']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='House A',
            x=features,
            y=vector_a,
            marker_color='blue'
        ))
        
        fig.add_trace(go.Bar(
            name='House B',
            x=features,
            y=vector_b,
            marker_color='red'
        ))
        
        fig.update_layout(
            title='House Feature Comparison',
            xaxis_title='Features',
            yaxis_title='Values',
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        #### 💡 Key Insights
        
        **Why Euclidean Distance?**
        - Considers actual values and magnitudes
        - Perfect for coordinates and measurements
        - Good for when scale matters
        - Works well with raw feature vectors
        
        **Real-world example**: House A ($500k, 2000 sq ft) vs House B ($600k, 2200 sq ft)
        are similar in the same market segment, even though they're not identical.
        """)

def show_dot_product():
    st.markdown("""
    ### Dot Product - The Raw Similarity Approach
    
    Dot product multiplies corresponding elements and sums them up.
    It's perfect when you want **raw compatibility** without normalization.
    
    **Formula**: `A·B = Σ(Aᵢ × Bᵢ)`
    **Range**: [-∞, ∞] (no fixed range)
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Example")
        
        st.markdown("**Job Requirements (Importance):**")
        j1 = st.slider("Python skills:", 0.0, 1.0, 0.9, key="job_python")
        j2 = st.slider("SQL skills:", 0.0, 1.0, 0.8, key="job_sql")
        j3 = st.slider("AWS skills:", 0.0, 1.0, 0.6, key="job_aws")
        j4 = st.slider("Communication:", 0.0, 1.0, 0.7, key="job_comm")
        
        job_vector = [j1, j2, j3, j4]
        
        st.markdown("**Candidate A Skills:**")
        c1 = st.slider("Python skills:", 0.0, 1.0, 0.8, key="cand_python")
        c2 = st.slider("SQL skills:", 0.0, 1.0, 0.9, key="cand_sql")
        c3 = st.slider("AWS skills:", 0.0, 1.0, 0.5, key="cand_aws")
        c4 = st.slider("Communication:", 0.0, 1.0, 0.6, key="cand_comm")
        
        candidate_vector = [c1, c2, c3, c4]
        
        # Calculate dot product
        dot_product = sum(j * c for j, c in zip(job_vector, candidate_vector))
        
        st.markdown("#### 📊 Results")
        st.metric("Dot Product Score", f"{dot_product:.3f}")
        
        if dot_product > 2.5:
            st.success("🎯 Excellent match!")
        elif dot_product > 2.0:
            st.info("👍 Good match")
        elif dot_product > 1.5:
            st.warning("🤔 Fair match")
        else:
            st.error("❌ Poor match")
    
    with col2:
        st.markdown("#### 📈 Visualization")
        
        # Create horizontal bar chart
        skills = ['Python', 'SQL', 'AWS', 'Communication']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Job Requirements',
            x=job_vector,
            y=skills,
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Candidate Skills',
            x=candidate_vector,
            y=skills,
            orientation='h',
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title='Job-Candidate Skill Alignment',
            xaxis_title='Skill Level',
            yaxis_title='Skills',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        #### 💡 Key Insights
        
        **Why Dot Product?**
        - Rewards alignment with what's most important
        - No normalization - raw compatibility score
        - Good for weighted features
        - Works well with unnormalized vectors
        
        **Real-world example**: Job values Python (0.9) and SQL (0.8) highly.
        Candidate A excels in these areas, getting a high dot product score
        even if they're weaker in less important skills.
        """)

def show_manhattan_distance():
    st.markdown("""
    ### Manhattan Distance - The City Block Approach
    
    Manhattan distance sums up the absolute differences between corresponding elements.
    It's perfect when you want a **robust measure** that's less affected by outliers.
    
    **Formula**: `Σ|Aᵢ - Bᵢ|`
    **Range**: [0, ∞) where 0 = identical
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Example")
        
        st.markdown("**Student A Test Scores:**")
        a1 = st.slider("Math:", 0, 100, 85, key="math_a")
        a2 = st.slider("Science:", 0, 100, 90, key="sci_a")
        a3 = st.slider("English:", 0, 100, 78, key="eng_a")
        a4 = st.slider("History:", 0, 100, 82, key="hist_a")
        
        vector_a = [a1, a2, a3, a4]
        
        st.markdown("**Student B Test Scores:**")
        b1 = st.slider("Math:", 0, 100, 80, key="math_b")
        b2 = st.slider("Science:", 0, 100, 95, key="sci_b")
        b3 = st.slider("English:", 0, 100, 85, key="eng_b")
        b4 = st.slider("History:", 0, 100, 75, key="hist_b")
        
        vector_b = [b1, b2, b3, b4]
        
        # Calculate Manhattan distance
        manhattan_dist = sum(abs(a - b) for a, b in zip(vector_a, vector_b))
        
        st.markdown("#### 📊 Results")
        st.metric("Manhattan Distance", f"{manhattan_dist}")
        
        if manhattan_dist < 20:
            st.success("🎓 Very similar performance!")
        elif manhattan_dist < 40:
            st.info("👍 Somewhat similar performance")
        elif manhattan_dist < 60:
            st.warning("🤔 Different performance")
        else:
            st.error("❌ Very different performance")
    
    with col2:
        st.markdown("#### 📈 Visualization")
        
        # Create line chart showing differences
        subjects = ['Math', 'Science', 'English', 'History']
        differences = [abs(a - b) for a, b in zip(vector_a, vector_b)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Score Differences',
            x=subjects,
            y=differences,
            marker_color='orange'
        ))
        
        fig.update_layout(
            title='Subject-wise Score Differences',
            xaxis_title='Subjects',
            yaxis_title='Absolute Difference',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        #### 💡 Key Insights
        
        **Why Manhattan Distance?**
        - Treats all differences equally
        - Less sensitive to outliers than Euclidean
        - Good for discrete features
        - Easy to interpret (total difference)
        
        **Real-world example**: Student A and B have similar overall performance
        with small differences in each subject. Manhattan distance captures
        the total difference across all subjects.
        """)

if __name__ == "__main__":
    main()
