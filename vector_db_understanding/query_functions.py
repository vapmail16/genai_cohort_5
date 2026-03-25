import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

def show_knn_demo():
    st.markdown("""
    ### K-Nearest Neighbors (KNN) - Find My Top K
    
    KNN finds the K most similar vectors to your query. It's like asking "show me the 5 most similar products" or "find the 3 most relevant documents".
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive KNN Demo")
        
        # Create sample movie database
        movies = {
            "The Matrix": [0.9, 0.8, 0.1, 0.2, 0.7],  # Action, sci-fi, romance, comedy, drama
            "Inception": [0.8, 0.9, 0.2, 0.1, 0.8],
            "Titanic": [0.1, 0.0, 0.9, 0.8, 0.9],
            "Blade Runner": [0.7, 0.9, 0.1, 0.0, 0.6],
            "The Notebook": [0.0, 0.0, 0.9, 0.9, 0.8],
            "The Matrix Reloaded": [0.9, 0.8, 0.1, 0.2, 0.7],
            "Interstellar": [0.6, 0.9, 0.3, 0.1, 0.8],
            "Casablanca": [0.2, 0.0, 0.8, 0.7, 0.9],
            "John Wick": [0.95, 0.3, 0.0, 0.1, 0.4],
            "La La Land": [0.1, 0.0, 0.8, 0.9, 0.7]
        }
        
        # Query movie selection
        query_movie = st.selectbox("Choose a query movie:", list(movies.keys()))
        k = st.slider("Number of similar movies to find (K):", 1, 5, 3)
        
        # Calculate similarities
        query_vector = movies[query_movie]
        similarities = []
        
        for movie, vector in movies.items():
            if movie != query_movie:
                # Cosine similarity
                dot_product = sum(a * b for a, b in zip(query_vector, vector))
                norm_query = math.sqrt(sum(a * a for a in query_vector))
                norm_movie = math.sqrt(sum(b * b for b in vector))
                similarity = dot_product / (norm_query * norm_movie) if norm_query != 0 and norm_movie != 0 else 0
                similarities.append((movie, similarity, vector))
        
        # Sort by similarity and get top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_k = similarities[:k]
        
        st.markdown("#### 📊 Results")
        st.write(f"**Query Movie**: {query_movie}")
        st.write(f"**Top {k} Similar Movies:**")
        
        for i, (movie, similarity, vector) in enumerate(top_k, 1):
            st.write(f"{i}. **{movie}** (Similarity: {similarity:.3f})")
        
        # Visualize
        categories = ['Action', 'Sci-Fi', 'Romance', 'Comedy', 'Drama']
        
        fig = go.Figure()
        
        # Query movie
        fig.add_trace(go.Scatterpolar(
            r=query_vector + [query_vector[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=query_movie,
            line_color='red',
            line_width=3
        ))
        
        # Similar movies
        colors = ['blue', 'green', 'orange', 'purple', 'brown']
        for i, (movie, similarity, vector) in enumerate(top_k):
            fig.add_trace(go.Scatterpolar(
                r=vector + [vector[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=f"{movie} ({similarity:.3f})",
                line_color=colors[i % len(colors)],
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=f"Top {k} Similar Movies to {query_movie}"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 KNN Characteristics")
        
        metrics = {
            "Query Type": "Similarity-based",
            "Result Count": "Fixed (K)",
            "Accuracy": "High (exact)",
            "Speed": "Depends on index",
            "Use Case": "Recommendation systems"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ KNN Strengths")
        st.success("""
        - **Fixed Results**: Always returns exactly K items
        - **High Accuracy**: Finds truly most similar items
        - **Intuitive**: Easy to understand and implement
        - **Flexible**: Can use any similarity metric
        """)
        
        st.markdown("#### ❌ KNN Limitations")
        st.error("""
        - **No Distance Threshold**: May return very different items
        - **Variable Quality**: Last items might be poor matches
        - **No Control**: Can't specify minimum similarity
        - **Scalability**: Can be slow with large datasets
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Recommendation systems
        - Finding similar products
        - Content discovery
        - User matching
        """)

def show_range_queries():
    st.markdown("""
    ### Range Queries - Find Everything Within X Distance
    
    Range queries find all vectors within a certain distance threshold. It's like asking "show me all houses within 5 miles" or "find all products under $100".
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive Range Query Demo")
        
        # Create sample house database
        houses = {
            "House A": [500, 2000, 3, 2],  # Price (k$), Size (sq ft), Bedrooms, Bathrooms
            "House B": [600, 2200, 4, 3],
            "House C": [300, 1500, 2, 1],
            "House D": [550, 2100, 3, 2],
            "House E": [400, 1800, 3, 2],
            "House F": [700, 2500, 4, 3],
            "House G": [350, 1600, 2, 2],
            "House H": [480, 1950, 3, 2]
        }
        
        # Query house selection
        query_house = st.selectbox("Choose a query house:", list(houses.keys()))
        threshold = st.slider("Distance threshold:", 50, 200, 100)
        
        # Calculate distances
        query_vector = houses[query_house]
        results = []
        
        for house, vector in houses.items():
            if house != query_house:
                # Euclidean distance
                distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(query_vector, vector)))
                if distance <= threshold:
                    results.append((house, distance, vector))
        
        # Sort by distance
        results.sort(key=lambda x: x[1])
        
        st.markdown("#### 📊 Results")
        st.write(f"**Query House**: {query_house}")
        st.write(f"**Threshold**: {threshold}")
        st.write(f"**Houses within range**: {len(results)}")
        
        if results:
            for house, distance, vector in results:
                st.write(f"• **{house}** (Distance: {distance:.1f})")
        else:
            st.warning("No houses found within the specified range")
        
        # Visualize in 2D (Price vs Size)
        fig = go.Figure()
        
        # All houses
        prices = [vector[0] for vector in houses.values()]
        sizes = [vector[1] for vector in houses.values()]
        names = list(houses.keys())
        
        fig.add_trace(go.Scatter(
            x=prices,
            y=sizes,
            mode='markers+text',
            text=names,
            textposition="top center",
            marker=dict(size=10, color='lightblue'),
            name='All Houses'
        ))
        
        # Query house (highlighted)
        query_price, query_size = query_vector[0], query_vector[1]
        fig.add_trace(go.Scatter(
            x=[query_price],
            y=[query_size],
            mode='markers+text',
            text=[query_house],
            textposition="top center",
            marker=dict(size=15, color='red'),
            name='Query House'
        ))
        
        # Houses within range
        if results:
            range_prices = [vector[0] for _, _, vector in results]
            range_sizes = [vector[1] for _, _, vector in results]
            range_names = [name for name, _, _ in results]
            
            fig.add_trace(go.Scatter(
                x=range_prices,
                y=range_sizes,
                mode='markers+text',
                text=range_names,
                textposition="bottom center",
                marker=dict(size=12, color='green'),
                name='Within Range'
            ))
        
        fig.update_layout(
            title='House Price vs Size (Range Query)',
            xaxis_title='Price (Thousands $)',
            yaxis_title='Size (sq ft)',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Range Query Characteristics")
        
        metrics = {
            "Query Type": "Distance-based",
            "Result Count": "Variable",
            "Accuracy": "High (exact)",
            "Control": "Distance threshold",
            "Use Case": "Geographic search"
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ Range Query Strengths")
        st.success("""
        - **Distance Control**: Specify exact distance threshold
        - **Quality Control**: Only returns items within range
        - **Flexible Results**: Can return 0 to many items
        - **Geographic**: Perfect for location-based queries
        """)
        
        st.markdown("#### ❌ Range Query Limitations")
        st.error("""
        - **Variable Results**: May return too many or too few
        - **No Ranking**: Results not ordered by similarity
        - **Threshold Tuning**: Need to choose appropriate distance
        - **Performance**: Can be slow with large datasets
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Geographic searches
        - Price range filtering
        - Outlier detection
        - Clustering applications
        """)

def show_ann_demo():
    st.markdown("""
    ### Approximate Nearest Neighbors (ANN) - Fast but Good Enough
    
    ANN finds approximately K most similar vectors, trading some accuracy for speed. It's perfect for large-scale applications where 95% accuracy is good enough.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎮 Interactive ANN Demo")
        
        # Simulate different ANN algorithms
        algorithm = st.selectbox(
            "Choose ANN algorithm:",
            ["LSH (Locality-Sensitive Hashing)", "HNSW (Hierarchical Navigable Small World)", "Product Quantization"]
        )
        
        dataset_size = st.slider("Dataset size:", 1000, 1000000, 100000)
        k = st.slider("Number of results (K):", 5, 50, 10)
        
        # Simulate performance characteristics
        if "LSH" in algorithm:
            search_time = 1  # ms
            accuracy = 92
            memory_usage = "Low"
        elif "HNSW" in algorithm:
            search_time = 5  # ms
            accuracy = 98
            memory_usage = "High"
        else:  # Product Quantization
            search_time = 3  # ms
            accuracy = 95
            memory_usage = "Very Low"
        
        # Simulate exact vs approximate search
        exact_search_time = dataset_size / 10000  # Simulate linear search
        
        st.markdown("#### 📊 Performance Comparison")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Exact Search Time", f"{exact_search_time:.1f} ms")
        with col_b:
            st.metric(f"{algorithm} Time", f"{search_time} ms")
        
        speedup = exact_search_time / search_time
        st.success(f"🚀 **{speedup:.1f}x speedup** with {accuracy}% accuracy!")
        
        # Accuracy vs Speed trade-off visualization
        algorithms = ["Exact Search", "LSH", "Product Quantization", "HNSW"]
        accuracies = [100, 92, 95, 98]
        times = [exact_search_time, 1, 3, 5]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=times,
            y=accuracies,
            mode='markers+text',
            text=algorithms,
            textposition="top center",
            marker=dict(size=15, color=['red', 'blue', 'green', 'orange']),
            name='Algorithms'
        ))
        
        fig.update_layout(
            title='Accuracy vs Speed Trade-off',
            xaxis_title='Search Time (ms)',
            yaxis_title='Accuracy (%)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 ANN Characteristics")
        
        metrics = {
            "Query Type": "Approximate similarity",
            "Result Count": "Fixed (K)",
            "Accuracy": f"{accuracy}% (approximate)",
            "Speed": f"{speedup:.1f}x faster",
            "Memory": memory_usage
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
        
        st.markdown("#### ✅ ANN Strengths")
        st.success("""
        - **Very Fast**: 10-100x faster than exact search
        - **Scalable**: Works with millions of vectors
        - **Good Accuracy**: 90-99% accuracy is often sufficient
        - **Real-time**: Suitable for interactive applications
        """)
        
        st.markdown("#### ❌ ANN Limitations")
        st.error("""
        - **Approximate**: May miss some similar vectors
        - **Parameter Tuning**: Requires optimization
        - **Quality Trade-off**: Speed vs accuracy balance
        - **Complexity**: More complex than exact search
        """)
        
        st.markdown("#### 🎯 Best Use Cases")
        st.info("""
        - Large-scale similarity search
        - Real-time recommendations
        - Interactive applications
        - When 95% accuracy is sufficient
        """)

def show_query_comparison():
    st.markdown("### 📊 Query Type Comparison")
    
    # Comparison table
    comparison_data = {
        "Query Type": ["KNN", "Range Query", "ANN"],
        "Result Count": ["Fixed (K)", "Variable", "Fixed (K)"],
        "Accuracy": ["High (exact)", "High (exact)", "Good (approximate)"],
        "Speed": ["Medium", "Medium", "Very Fast"],
        "Control": ["None", "Distance threshold", "Approximation level"],
        "Best For": ["Recommendations", "Geographic search", "Large scale"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    st.markdown("### 🎯 When to Use Each Query Type")
    
    use_case = st.selectbox(
        "What's your primary need?",
        ["Recommendation System", "Geographic Search", "Large-Scale Search", "Real-time Search", "Exact Results"]
    )
    
    if use_case == "Recommendation System":
        st.success("**Recommended: KNN** - Fixed number of recommendations with high accuracy")
    elif use_case == "Geographic Search":
        st.success("**Recommended: Range Query** - Find everything within distance threshold")
    elif use_case == "Large-Scale Search":
        st.success("**Recommended: ANN** - Fast approximate search for millions of vectors")
    elif use_case == "Real-time Search":
        st.success("**Recommended: ANN** - Fast enough for interactive applications")
    elif use_case == "Exact Results":
        st.success("**Recommended: KNN or Range Query** - Exact algorithms for precise results")
