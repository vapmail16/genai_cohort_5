# Vector Databases Interactive Tutorial 🔍

An interactive Streamlit application designed to help you learn and understand vector databases through hands-on examples, visualizations, and practical demonstrations.

## 🚀 Features

- **Interactive Vector Fundamentals**: Create and visualize your own vectors
- **Similarity Metrics**: Hands-on demonstrations of cosine similarity, Euclidean distance, dot product, and Manhattan distance
- **Slide-ready theory**: See **“Cohort slides — Similarity metrics”** in `vector_databases_technical_deep_dive.md` (plain language + hand-calculated examples)
- **Qdrant PDF lab (live)**: Ingest PDFs via the **Qdrant HTTP API**, then inspect **dimensions** and the **first components** of stored vectors (Streamlit module + CLI)
- **Embedding Models**: Compare BERT vs OpenAI embeddings with real examples
- **Index Types**: Explore HNSW, LSH, Product Quantization, and more
- **Visual Learning**: Rich visualizations and interactive examples
- **Real-World Examples**: Practical applications and use cases

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download** this repository to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd vector_db_understanding
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (`sentence-transformers` pulls **PyTorch** — first install can take a few minutes.)

### Qdrant (for the PDF lab)

**Recommended:** [Qdrant Cloud](https://cloud.qdrant.io/) — REST URL + API key (no Docker required).

1. Copy `vector_db_understanding/.env.example` to **`vector_db_understanding/.env`** (gitignored).
2. Set **`QDRANT_URL`** (HTTPS cluster URL, usually port **6333**) and **`QDRANT_API_KEY`** from the Cloud console.
3. Optional: **`QDRANT_COLLECTION`** (default `cohort_pdf_demo`).

The Streamlit **Qdrant PDF lab** and the CLI read these variables automatically. You can still override URL/key in the UI.

**What runs:** PDF text → **local** Sentence-Transformers embeddings → upsert to Qdrant → scroll to inspect vectors. **No LLM** and no RAG answering in this lab.

**Optional:** local Qdrant via Docker (`docker compose up -d` in this folder) only if you want a server on `http://localhost:6333` instead of Cloud.

## 🎯 Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** and go to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Start learning!** Use the sidebar to navigate between different modules

### CLI: PDF → Qdrant (same pipeline as the lab)

With `.env` configured (or flags):

```bash
python qdrant_pdf_pipeline.py path/to/slides.pdf
# Optional overrides:
# python qdrant_pdf_pipeline.py path/to/slides.pdf --qdrant-url https://....:6333 --api-key YOUR_KEY
```

## 📚 Learning Modules

### 🏠 Home
- Introduction and overview
- Navigation guide

### 📐 Vector Fundamentals
- What are vectors?
- Understanding dimensions
- The curse of dimensionality
- Interactive vector creation and visualization

### 🎯 Similarity Metrics
- **Cosine Similarity**: Angle-based approach for finding similar patterns
- **Euclidean Distance**: Straight-line distance for actual values
- **Dot Product**: Raw compatibility scoring
- **Manhattan Distance**: City-block approach for robust measurements

### 📐 Similarity math (theory & examples)
- Plain-language intuition, LaTeX formulas, hand-worked examples
- Expandable **Check** rows that echo `similarity_math.py` (same numbers as the deep-dive doc)
- Quick comparison table + how metrics relate to Qdrant

### 🧠 Embedding Models
- **BERT (768D)**: Context-aware transformer for local development
- **OpenAI Embeddings (1536D)**: Modern language understanding for production
- **Comparison**: Side-by-side analysis of different models
- **Selection Guide**: When to use each model

### 🏗️ Index Types
- **HNSW**: Multi-level graph structure for high accuracy
- **LSH**: Hash-based bucketing for fast approximate search
- **Product Quantization**: Compression approach for memory efficiency
- **Comparison Guide**: Choose the right index for your use case

### 🔍 Query Types *(Coming Soon)*
- K-Nearest Neighbors (KNN)
- Range queries
- Approximate Nearest Neighbors (ANN)

### ⚡ Performance Optimization *(Coming Soon)*
- Memory optimization techniques
- Computational optimization
- Query optimization strategies

### 🌐 Popular Technologies *(Coming Soon)*
- Qdrant, Pinecone, PG Vector, Chroma comparisons
- Technical architecture details
- Use case recommendations

### 💼 Real-World Examples *(Coming Soon)*
- E-commerce product search
- Recommendation systems
- Document retrieval
- Image similarity search

### 📦 Qdrant PDF lab (live)
- Requires **`QDRANT_URL` / `QDRANT_API_KEY`** in `vector_db_understanding/.env` (Qdrant Cloud) or any reachable Qdrant REST endpoint + full `requirements.txt` install
- Upload a PDF, upsert chunks with **384-d** `all-MiniLM-L6-v2` embeddings (local model; **not** an LLM summarizer)
- Inspect **vector dimension**, **L2 norm**, and **first N components** per point

## 🎮 How to Use

1. **Start with Vector Fundamentals** to build your foundation
2. **Explore Similarity Metrics** to understand how vectors are compared
3. **Learn about Embedding Models** to see how text becomes vectors
4. **Study Index Types** to understand how search is optimized
5. **Use the interactive examples** to experiment with different parameters
6. **Navigate between modules** using the sidebar

## 💡 Teaching Tips

- **Use the interactive examples** to demonstrate concepts live
- **Encourage experimentation** with different parameters
- **Connect to real-world examples** using the provided scenarios
- **Show the visualizations** to make abstract concepts concrete
- **Use the comparison tools** to help students understand trade-offs

## 🔧 Customization

You can customize the app by:
- Adding new examples in the respective modules
- Modifying the visualizations
- Adding new similarity metrics
- Including additional embedding models
- Creating new interactive examples

## 📖 Educational Use

This application is perfect for:
- **Computer Science courses** covering vector databases
- **Machine Learning workshops** on embeddings and similarity search
- **Data Science training** on modern search techniques
- **Technical presentations** on vector database concepts
- **Self-paced learning** for understanding vector databases

## 🤝 Contributing

Feel free to:
- Add new interactive examples
- Improve existing visualizations
- Fix bugs or issues
- Suggest new features
- Share your teaching experiences

## 📄 License

This project is open source and available under the MIT License.

## 🧪 Tests

```bash
pytest -m "not slow"   # fast unit tests
pytest -m slow         # loads sentence-transformers (downloads model on first run)
```

## 🆘 Troubleshooting

**App won't start?**
- Make sure you have Python 3.7+ installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Try running: `streamlit run streamlit_app.py --server.port 8501`

**Visualizations not showing?**
- Make sure you have a stable internet connection (for Plotly)
- Try refreshing the browser page
- Check the browser console for any JavaScript errors

**Performance issues?**
- The app works best with modern browsers
- Close other browser tabs to free up memory
- Some visualizations may be slow with large datasets

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the Streamlit documentation
3. Check that all dependencies are properly installed

---

**Happy Learning! 🎉**

Use this interactive tutorial to master vector databases and become an expert in modern search and similarity techniques.
