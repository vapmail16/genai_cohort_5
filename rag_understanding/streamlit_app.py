import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import random
from datetime import datetime

# Import our custom modules
from app_modules import (
    show_rag_fundamentals, show_rag_architectures, show_implementation_strategies,
    show_real_world_applications, show_performance_optimization, show_best_practices
)

# Page configuration
st.set_page_config(
    page_title="RAG Understanding - Interactive Tutorial",
    page_icon="🤖",
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
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
def main():
    st.markdown('<h1 class="main-header">🤖 RAG Understanding - Interactive Tutorial</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📚 Learning Modules")
    
    page = st.sidebar.selectbox(
        "Choose a module:",
        [
            "🏠 Home",
            "🔍 RAG Fundamentals", 
            "🏗️ RAG Architectures",
            "⚙️ Implementation Strategies",
            "🌍 Real-World Applications",
            "⚡ Performance & Optimization",
            "📋 Best Practices & Tips"
        ]
    )
    
    if page == "🏠 Home":
        show_home()
    elif page == "🔍 RAG Fundamentals":
        show_rag_fundamentals()
    elif page == "🏗️ RAG Architectures":
        show_rag_architectures()
    elif page == "⚙️ Implementation Strategies":
        show_implementation_strategies()
    elif page == "🌍 Real-World Applications":
        show_real_world_applications()
    elif page == "⚡ Performance & Optimization":
        show_performance_optimization()
    elif page == "📋 Best Practices & Tips":
        show_best_practices()

def show_home():
    st.markdown("""
    ## Welcome to the RAG Understanding Interactive Tutorial! 🚀
    
    This comprehensive interactive application will help you master Retrieval-Augmented Generation (RAG) 
    through hands-on examples, visualizations, and practical demonstrations.
    
    ### What You'll Learn:
    - **RAG Fundamentals**: Understanding the core concepts, components, and how RAG works
    - **RAG Architectures**: 9 different RAG patterns from Naive to Agentic RAG
    - **Implementation Strategies**: Step-by-step guides for building RAG systems
    - **Real-World Applications**: Practical examples and use cases
    - **Performance & Optimization**: Making your RAG systems fast and efficient
    - **Best Practices**: Industry tips and common pitfalls to avoid
    
    ### How to Use This Tutorial:
    1. **Navigate** through modules using the sidebar
    2. **Interact** with visualizations and examples
    3. **Experiment** with different parameters and configurations
    4. **Learn** through hands-on practice and real-world scenarios
    
    ### Getting Started:
    Start with "RAG Fundamentals" to build your foundation, then explore other modules based on your interests.
    
    ---
    
    **Pro Tip**: Each module builds on previous concepts, so we recommend following the order in the sidebar!
    
    ### 🎯 Quick Navigation Guide:
    
    **For Beginners:**
    - Start with RAG Fundamentals
    - Explore the first few RAG Architectures
    - Try Implementation Strategies
    
    **For Intermediate Users:**
    - Jump to specific RAG Architectures
    - Focus on Performance & Optimization
    - Study Real-World Applications
    
    **For Advanced Users:**
    - Deep dive into Agentic RAG
    - Master Performance & Optimization
    - Review Best Practices for production systems
    """)

if __name__ == "__main__":
    main()
