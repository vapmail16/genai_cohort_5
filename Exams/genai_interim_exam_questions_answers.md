# GenAI Interim Exam - Questions and Detailed Answers

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

### **ANSWER TO QUESTION 1**

#### **Part A: BERT vs OpenAI Embeddings**

**BERT Embeddings (768D)**:
- **Architecture**: 12 transformer layers with 768 hidden units
- **How it works**: Bidirectional understanding, reads text both left-to-right and right-to-left
- **Training**: Pre-trained on general language, can be fine-tuned for specific domains
- **Deployment**: Can run locally on your own servers
- **Cost**: Free to use, only infrastructure costs
- **Privacy**: Data stays on your servers, complete control

**OpenAI Embeddings (1536D)**:
- **Architecture**: Based on GPT-3.5 with 1536 hidden units
- **How it works**: Optimized specifically for semantic similarity and search tasks
- **Training**: Large-scale training with focus on retrieval quality
- **Deployment**: Cloud-based API service
- **Cost**: Pay per API call (~$0.0001 per 1K tokens)
- **Privacy**: Data sent to OpenAI servers

**When to Choose Each**:

**Choose BERT (768D) when**:
1. **Privacy is critical**: Medical records, legal documents, confidential business information
2. **Cost control**: High-volume processing (millions of documents)
3. **Custom requirements**: Need to fine-tune for specific industry jargon
4. **Offline operation**: No internet connection available
5. **Regulatory compliance**: Data cannot leave your infrastructure

**Choose OpenAI (1536D) when**:
1. **Best accuracy needed**: Customer-facing search where quality is paramount
2. **Quick deployment**: Need to launch quickly without infrastructure setup
3. **Multilingual support**: Documents in multiple languages
4. **Lower volume**: Processing fewer than 1M documents monthly
5. **Managed service preferred**: Don't want to maintain embedding infrastructure

**Recommendation for Company Internal Documents**:
- **Use BERT** for privacy, cost control, and compliance
- **Use OpenAI** if rapid deployment and best quality are priorities

#### **Part B: Storage Calculation and Optimization**

**Base Storage Calculation**:
```
Given:
- 5 million document chunks
- OpenAI embeddings: 1536 dimensions
- Data type: float32 (4 bytes per number)

Calculation:
Step 1: Size per embedding
1536 dimensions × 4 bytes = 6,144 bytes = 6.144 KB

Step 2: Total storage
5,000,000 chunks × 6,144 bytes = 30,720,000,000 bytes
= 30,720 MB
= 30 GB (approximately)

Step 3: With metadata (assume 1KB per chunk)
Vector data: 30 GB
Metadata: 5M × 1KB = 5 GB
Total: 35 GB
```

**Optimization Strategies**:

**1. Quantization (Recommended)**:
```
Convert float32 to int8 (8-bit integers):
- Reduction: 4 bytes → 1 byte = 75% savings
- New storage: 30 GB × 0.25 = 7.5 GB
- Accuracy loss: ~2-5% (acceptable for most use cases)
```

**2. Product Quantization**:
```
Compress 1536D → codes (256 codes per sub-vector):
- Split into 8 sub-vectors of 192D each
- Replace with 8-bit codes
- Storage: 5M × 8 bytes = 40 MB for codes
- Codebook: ~2 MB
- Total: ~42 MB (99% reduction!)
- Accuracy loss: ~10-15%
```

**3. Dimensionality Reduction**:
```
Use PCA to reduce 1536D → 512D:
- New storage: 5M × 512 × 4 bytes = 10.24 GB
- Savings: 66% reduction
- Accuracy loss: ~5-10%
```

**4. Sparse Storage** (if applicable):
```
If embeddings have many near-zero values:
- Store only non-zero values
- Potential savings: 30-50%
- Best for: Certain embedding types
```

**Recommended Strategy**:
- Use **Scalar Quantization (int8)** for best balance
- Final storage: ~7.5 GB (75% savings)
- Accuracy: >95% maintained
- Query speed: Faster due to smaller data

---

## Question 2: Vector Database Architecture (20 points)

**Scenario**: You need to design a vector database system for an e-commerce product search with 10 million products.

### Part A (10 points)
Compare and contrast three indexing approaches: HNSW (graph-based), LSH (hash-based), and Product Quantization. Which would you choose for this use case and why?

### Part B (10 points)
Explain the "curse of dimensionality" and describe two practical strategies you would implement to mitigate it in your product search system.

---

### **ANSWER TO QUESTION 2**

#### **Part A: Indexing Approaches Comparison**

**1. HNSW (Hierarchical Navigable Small World) - Graph-Based**:

**How it works**:
- Creates a multi-level graph where each level has different connection densities
- Bottom level: Dense connections (many neighbors)
- Top level: Sparse connections (few neighbors)
- Search: Start at top, navigate down to find similar vectors

**Advantages**:
- ✅ Excellent performance for high-dimensional data
- ✅ High search accuracy (>95%)
- ✅ Fast search: O(log n) time complexity
- ✅ Good for production systems

**Disadvantages**:
- ❌ Memory intensive (2-4x vector size)
- ❌ Complex to build and maintain
- ❌ Slower updates (need to rebuild connections)

**Best for**: Production systems with high query frequency

**2. LSH (Locality-Sensitive Hashing) - Hash-Based**:

**How it works**:
- Uses hash functions to put similar vectors in same "buckets"
- Similar vectors get similar hash values
- Search: Hash query, check vectors in same bucket

**Advantages**:
- ✅ Very fast approximate search: O(1) average
- ✅ Memory efficient
- ✅ Simple to implement
- ✅ Good for high-dimensional data

**Disadvantages**:
- ❌ May miss some similar vectors (lower accuracy ~85-90%)
- ❌ Requires careful parameter tuning
- ❌ Hash collisions can affect quality

**Best for**: Large-scale systems where speed > accuracy

**3. Product Quantization - Compression-Based**:

**How it works**:
- Splits vectors into sub-vectors
- Replaces sub-vectors with short codes
- Search: Compare codes instead of full vectors

**Advantages**:
- ✅ Massive memory savings (75-90% reduction)
- ✅ Faster distance calculations
- ✅ Handles very large datasets
- ✅ Good for memory-constrained systems

**Disadvantages**:
- ❌ Accuracy loss (~10-15%)
- ❌ Complex implementation
- ❌ Slower to build initially

**Best for**: Large datasets with memory constraints

**Comparison Table**:

| Aspect | HNSW | LSH | Product Quantization |
|--------|------|-----|---------------------|
| Search Speed | Fast (log n) | Very Fast (O(1)) | Medium |
| Accuracy | High (95%+) | Medium (85-90%) | Medium (85-90%) |
| Memory | High (2-4x) | Medium | Low (0.1-0.25x) |
| Build Time | Medium | Fast | Slow |
| Updates | Slower | Fast | Medium |
| Complexity | High | Medium | High |

**Recommendation for E-commerce (10M products)**:

**Choose HNSW** because:
1. **High query frequency**: E-commerce has many searches per second
2. **Accuracy matters**: Users expect relevant product results
3. **Memory affordable**: 10M products × 512D × 4 bytes × 3x = ~60 GB (manageable)
4. **Production ready**: Proven in similar use cases (Amazon, Alibaba)
5. **Good user experience**: Fast (<50ms) and accurate (>95%)

**Implementation**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="localhost:6333")

client.create_collection(
    collection_name="products",
    vectors_config=VectorParams(
        size=512,  # Embedding dimensions
        distance=Distance.COSINE,
        hnsw_config={
            "m": 16,  # Number of edges per node
            "ef_construction": 200,  # Construction quality
        }
    )
)
```

#### **Part B: Curse of Dimensionality**

**What is the Curse of Dimensionality?**

**Definition**: As the number of dimensions increases, several problematic phenomena occur that make distance-based algorithms less effective.

**Key Problems**:

**1. Distance Concentration**:
```
In high dimensions, all points become approximately equidistant:
- 2D space: Clear near/far distinctions
- 100D space: Most distances are similar
- 1000D space: All distances nearly identical

Example:
2D: Point A to B = 5 units, Point A to C = 50 units (10x difference)
1000D: Point A to B = 31.4 units, Point A to C = 31.7 units (1.01x difference)
```

**2. Volume Explosion**:
```
As dimensions increase, volume grows exponentially:
- 2D circle: Area = πr²
- 3D sphere: Volume = 4/3πr³
- nD hypersphere: Volume = r^n (exponential!)

Result: Data becomes incredibly sparse
```

**3. Computational Cost**:
```
Distance calculation cost grows linearly with dimensions:
- 100D: 100 multiplications + 100 additions
- 1000D: 1000 multiplications + 1000 additions
- 10x dimensions = 10x computation time
```

**Two Practical Mitigation Strategies**:

**Strategy 1: Dimensionality Reduction with PCA**

**How it works**:
- Reduce 1536D OpenAI embeddings to 512D or 256D
- Keep dimensions that capture most variance
- Lose minimal semantic information

**Implementation**:
```python
from sklearn.decomposition import PCA
import numpy as np

# Original embeddings: 1536D
original_embeddings = load_embeddings()  # Shape: (10M, 1536)

# Reduce to 512D
pca = PCA(n_components=512)
reduced_embeddings = pca.fit_transform(original_embeddings)  # Shape: (10M, 512)

# Storage savings
original_size = 10_000_000 * 1536 * 4 = 61.44 GB
reduced_size = 10_000_000 * 512 * 4 = 20.48 GB
savings = 66%

# Accuracy retention: ~95%
```

**Benefits**:
- 66% storage reduction
- 3x faster search
- Maintains 95% accuracy
- One-time preprocessing cost

**Strategy 2: HNSW with Optimized Parameters**

**How it works**:
- Use graph-based indexing designed for high dimensions
- Multi-level structure bypasses curse of dimensionality
- Optimized parameters for e-commerce scale

**Implementation**:
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, HnswConfig

client = QdrantClient(url="localhost:6333")

client.create_collection(
    collection_name="products",
    vectors_config=VectorParams(
        size=1536,  # Full dimensionality
        distance=Distance.COSINE,
        hnsw_config=HnswConfig(
            m=16,  # Connections per node (balance: 8-32)
            ef_construction=200,  # Build quality (higher = better)
            full_scan_threshold=10000,  # Use HNSW above this size
        ),
        on_disk=True  # Store on disk for large datasets
    )
)

# Search with optimized parameters
search_results = client.search(
    collection_name="products",
    query_vector=query_embedding,
    limit=10,
    search_params={"hnsw_ef": 128}  # Search quality
)
```

**Benefits**:
- Works well even in high dimensions
- >95% accuracy maintained
- <50ms search latency
- Proven at scale (billions of vectors)

**Combined Strategy** (Best for E-commerce):
1. Use PCA to reduce to 512D (66% storage savings)
2. Use HNSW on reduced embeddings
3. Result: Fast, accurate, memory-efficient system

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

### **ANSWER TO QUESTION 3**

#### **Scenario A: Movie Recommendations - Use COSINE SIMILARITY**

**Why Cosine Similarity?**

Cosine similarity measures the **angle/pattern** between vectors, ignoring magnitude (how many ratings).

**Example**:
```python
# User A (rates many genres)
user_a = [5, 4, 1, 1, 3, 5, 2]  # Action, Comedy, Horror, Romance, Drama, Sci-Fi, Thriller

# User B (rates few genres)
user_b = [2.5, 2, 0.5, 0.5, 1.5, 2.5, 1]  # Same pattern, half the magnitude

# Cosine similarity = 1.0 (perfect match!)
# Both users have identical taste patterns: Love Action/Sci-Fi, Like Comedy, Hate Horror/Romance
```

**Why this matters**:
- **Pattern focus**: Both users love action and sci-fi, hate horror
- **Magnitude ignored**: Doesn't matter if one user is more expressive with ratings
- **Fair comparison**: Active raters aren't penalized vs passive raters

**Wrong choice - Euclidean Distance**:
- Would say User A and User B are "different" due to magnitude
- Would recommend different movies even though preferences are identical

#### **Scenario B: House Search - Use MANHATTAN DISTANCE**

**Why Manhattan Distance?**

Manhattan distance treats **all dimensions equally** - a $10K price difference is weighted the same as 1 bathroom difference.

**Example**:
```python
# House A
house_a = [500000, 2000, 3, 2]  # [$500K, 2000 sqft, 3 bed, 2 bath]

# House B
house_b = [520000, 2100, 3, 2]  # [$520K, 2100 sqft, 3 bed, 2 bath]

# Manhattan distance
distance = |500000-520000| + |2000-2100| + |3-3| + |2-2|
         = 20000 + 100 + 0 + 0
         = 20,100

# Each feature difference is counted equally
```

**Why this matters**:
- **Equal importance**: Price, size, bedrooms, bathrooms all matter equally
- **Robust to outliers**: Extreme values don't dominate the distance
- **Interpretable**: Total difference across all features
- **Fair weighting**: No single feature dominates similarity

**Alternative - Euclidean Distance** (also acceptable):
- Would work but gives more weight to larger differences (price would dominate)
- Squaring differences means $20K price difference has disproportionate impact

#### **Scenario C: Job Matching - Use DOT PRODUCT**

**Why Dot Product?**

Dot product rewards **alignment with what's most important** - if the job highly values Python (0.9), candidates strong in Python get high scores.

**Example**:
```python
# Job requirements (what's most important)
job_requirements = [0.9, 0.7, 0.8]  # Python, AWS, SQL

# Candidate A (strong where job values it)
candidate_a = [0.9, 0.6, 0.7]  # Python, AWS, SQL

# Candidate B (strong in wrong areas)
candidate_b = [0.3, 0.9, 0.2]  # Python, AWS, SQL

# Dot Product for Candidate A
dot_a = (0.9 × 0.9) + (0.7 × 0.6) + (0.8 × 0.7)
      = 0.81 + 0.42 + 0.56
      = 1.79  # HIGH SCORE

# Dot Product for Candidate B
dot_b = (0.9 × 0.3) + (0.7 × 0.9) + (0.8 × 0.2)
      = 0.27 + 0.63 + 0.16
      = 1.06  # LOWER SCORE
```

**Why this matters**:
- **Weighted importance**: Python skill (0.9) is weighted more heavily
- **Alignment reward**: Being strong where the job needs it most = higher score
- **Practical matching**: Candidate A is better fit despite Candidate B having higher AWS

**Wrong choice - Cosine Similarity**:
- Would normalize both candidates, losing the "importance" weighting
- Wouldn't capture that Python matters more than AWS

**Summary Table**:

| Scenario | Best Metric | Reason |
|----------|-------------|---------|
| Movie Preferences | Cosine Similarity | Ignore rating magnitude, focus on pattern |
| House Search | Manhattan Distance | Equal importance for all features |
| Job Matching | Dot Product | Reward alignment with critical skills |

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

### **ANSWER TO QUESTION 4**

#### **Part A: Architecture Selection**

**Recommended Architecture: CORRECTIVE RAG**

**Why Corrective RAG?**

**Medical requirements demand**:
1. **High accuracy**: Medical information must be correct (life-critical)
2. **Verification**: Need to validate information quality
3. **Multiple sources**: Cross-reference medical sources
4. **Currency**: Access latest medical research and guidelines
5. **Quality control**: Filter out outdated or unreliable information

**How Corrective RAG meets these needs**:
- **Initial retrieval**: Searches medical knowledge base
- **Quality grading**: Evaluates relevance and accuracy of retrieved documents
- **Web search fallback**: Gets latest information if knowledge base is insufficient
- **Correction mechanism**: Validates and corrects information before responding
- **Source attribution**: Provides citations for all medical claims

**Why other architectures are less suitable**:

**Naive RAG** ❌:
- No quality validation
- Single retrieval step might miss important information
- No mechanism to verify accuracy
- **Risk**: Could provide unverified medical information

**HyDE** ❌:
- Generates hypothetical answers first
- **Risk**: Hypothesis could be medically incorrect, biasing retrieval
- No quality validation mechanism

**Multimodal RAG** ⚠️:
- Good for medical images but overcomplicated
- Primary need is text accuracy, not multimodal processing
- **Verdict**: Useful feature but not primary requirement

**Graph RAG** ⚠️:
- Good for understanding drug interactions and relationships
- Requires extensive graph construction
- **Verdict**: Could be combined with Corrective RAG for best results

**Hybrid RAG** ⚠️:
- Excellent performance but higher complexity
- **Verdict**: Good alternative, but Corrective RAG's validation is more critical

**Adaptive RAG** ❌:
- Complexity varies by question
- Medical queries always need high accuracy, regardless of complexity
- **Risk**: Might use simpler methods for "simple" medical questions

**Agentic RAG** ⚠️:
- Excellent for complex medical research
- High complexity and latency
- **Verdict**: Overkill for basic medical Q&A, good for research use cases

#### **Part B: Complete Data Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                  MEDICAL INFORMATION SYSTEM                    │
│                    (Corrective RAG Architecture)                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: USER QUERY                                             │
├─────────────────────────────────────────────────────────────────┤
│  Input: "What are the side effects of aspirin?"                │
│  Processing: Query understanding and intent classification      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: QUERY EMBEDDING                                        │
├─────────────────────────────────────────────────────────────────┤
│  Model: OpenAI text-embedding-ada-002 (1536D)                  │
│  Output: Vector representation of query                        │
│  Medical terms: Normalized and expanded with synonyms          │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: INITIAL RETRIEVAL                                      │
├─────────────────────────────────────────────────────────────────┤
│  Vector Database: Qdrant (HNSW index)                          │
│  Sources:                                                       │
│    - FDA drug database                                          │
│    - Medical journals (PubMed)                                  │
│    - Clinical guidelines                                        │
│    - Drug interaction databases                                │
│  Retrieved: Top 20 relevant chunks                             │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: RELEVANCE GRADING (CRITICAL FOR MEDICAL)               │
├─────────────────────────────────────────────────────────────────┤
│  Grading Model: Fine-tuned classifier for medical relevance    │
│  Checks:                                                        │
│    ✓ Source credibility (FDA > random blog)                    │
│    ✓ Information freshness (< 2 years preferred)               │
│    ✓ Specificity (aspirin side effects, not general NSAIDs)    │
│    ✓ Evidence level (clinical trials > case reports)           │
│  Quality Score: 0.0-1.0 for each chunk                        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: QUALITY DECISION POINT                                 │
├─────────────────────────────────────────────────────────────────┤
│  Threshold: Average quality > 0.7                              │
│  If YES: Use retrieved documents                               │
│  If NO: Trigger web search + additional retrieval              │
└─────────────────────────────────────────────────────────────────┘
            │                            │
            │ (Quality < 0.7)            │ (Quality >= 0.7)
            ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────────────┐
│ STEP 6A: WEB SEARCH     │  │ STEP 6B: USE RETRIEVED DOCS    │
├─────────────────────────┤  ├─────────────────────────────────┤
│  Search:                │  │  Filter: Keep high-quality     │
│    - PubMed API         │  │  Rerank: Cross-encoder model   │
│    - FDA website        │  │  Deduplicate: Remove similar   │
│    - Medical journals   │  │  Select: Top 5 chunks          │
│  Validate:              │  └─────────────────────────────────┘
│    - Source authority   │              │
│    - Date verification  │              │
│  Combine with retrieved │              │
└─────────────────────────┘              │
            │                            │
            └────────────┬───────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: FACT VERIFICATION                                      │
├─────────────────────────────────────────────────────────────────┤
│  Cross-reference:                                               │
│    - Verify claims against multiple sources                    │
│    - Check for contradictions                                  │
│    - Validate dosage and numbers                               │
│  Medical checks:                                               │
│    - Drug name verification                                    │
│    - Contraindication warnings                                 │
│    - Interaction warnings                                      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 8: RESPONSE GENERATION                                    │
├─────────────────────────────────────────────────────────────────┤
│  LLM: GPT-4 with medical-focused system prompt                 │
│  Prompt includes:                                               │
│    - Retrieved medical information                             │
│    - Source citations                                          │
│    - Safety guidelines                                         │
│    - Disclaimer requirements                                   │
│  Output format: Structured with sources                        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 9: POST-GENERATION VALIDATION                            │
├─────────────────────────────────────────────────────────────────┤
│  Checks:                                                       │
│    ✓ Medical terminology accuracy                             │
│    ✓ Dosage information correctness                           │
│    ✓ Warning labels included                                  │
│    ✓ Source citations present                                 │
│    ✓ Disclaimer added                                         │
│  Confidence score: 0.0-1.0                                    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 10: FINAL OUTPUT                                          │
├─────────────────────────────────────────────────────────────────┤
│  Answer: "Common side effects of aspirin include:              │
│          - Stomach upset and heartburn                         │
│          - Increased bleeding risk                             │
│          - Allergic reactions (rare)                           │
│                                                                │
│  Sources:                                                      │
│    [1] FDA Drug Label - Aspirin (Updated: 2023)               │
│    [2] PubMed: "Aspirin Safety Profile" (2023)               │
│    [3] Mayo Clinic: Aspirin Side Effects (2024)               │
│                                                                │
│  ⚠️ IMPORTANT: Consult your healthcare provider before        │
│     starting or stopping any medication."                      │
│                                                                │
│  Confidence: 0.95 (High)                                      │
└─────────────────────────────────────────────────────────────────┘
```

#### **Part C: Safety Mechanisms**

**1. Multi-Source Verification**:
```python
def verify_medical_claim(claim, sources):
    # Require at least 3 authoritative sources
    if len(sources) < 3:
        return "INSUFFICIENT_SOURCES"
    
    # Check source authority
    authoritative_count = 0
    for source in sources:
        if source in ['FDA', 'PubMed', 'Mayo Clinic', 'CDC']:
            authoritative_count += 1
    
    if authoritative_count < 2:
        return "INSUFFICIENT_AUTHORITY"
    
    # Check for contradictions
    if has_contradictions(claim, sources):
        return "CONTRADICTORY_INFORMATION"
    
    return "VERIFIED"
```

**2. Mandatory Disclaimers**:
- **Always include**: "Consult your healthcare provider"
- **Dosage warnings**: Never provide specific dosage recommendations
- **Emergency guidance**: "Seek immediate medical attention if..."
- **Limitation statement**: "This is for informational purposes only"

**3. Confidence Thresholding**:
```python
def should_answer(confidence_score, query_type):
    # High threshold for medical queries
    if query_type == "medication_dosage":
        threshold = 0.95  # Very high confidence required
    elif query_type == "side_effects":
        threshold = 0.85  # High confidence required
    elif query_type == "general_info":
        threshold = 0.75  # Moderate confidence
    
    if confidence_score < threshold:
        return "I don't have sufficient reliable information to answer this. Please consult a healthcare professional."
    
    return "PROCEED"
```

**4. Human-in-the-Loop for Critical Cases**:
```python
critical_keywords = [
    "pregnant", "children", "dosage", "interaction", 
    "emergency", "allergy", "surgery"
]

def check_critical_case(query):
    if any(keyword in query.lower() for keyword in critical_keywords):
        return "ESCALATE_TO_MEDICAL_PROFESSIONAL"
    return "SAFE_TO_ANSWER"
```

**5. Audit Trail**:
- **Log all queries**: Track what medical information was requested
- **Log all sources**: Record which sources were used
- **Log all responses**: Keep record of medical advice given
- **Review process**: Regular review of edge cases and errors

**Complete Safety Pipeline**:
```python
def safe_medical_response(query):
    # Step 1: Check if query is appropriate
    if check_critical_case(query) == "ESCALATE":
        return "This question requires consultation with a healthcare professional."
    
    # Step 2: Retrieve and validate information
    sources = retrieve_medical_information(query)
    verification = verify_medical_claim(query, sources)
    
    if verification != "VERIFIED":
        return "I cannot provide verified medical information for this query. Please consult a healthcare professional."
    
    # Step 3: Generate response with disclaimers
    response = generate_response(query, sources)
    response = add_medical_disclaimers(response)
    response = add_source_citations(response, sources)
    
    # Step 4: Final validation
    confidence = calculate_confidence(response, sources)
    if confidence < 0.85:
        return "I don't have sufficient reliable information. Please consult a healthcare professional."
    
    # Step 5: Log for audit
    log_medical_query(query, response, sources, confidence)
    
    return response
```

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

### **ANSWER TO QUESTION 5**

#### **Part A: Complete System Prompt**

```
ROLE DEFINITION:
You are a professional customer support assistant for TechStore, an online electronics retailer. You have access to our knowledge base, order history, and return policies. Your goal is to help customers resolve their issues efficiently while maintaining a helpful, empathetic, and professional tone.

CORE RESPONSIBILITIES:
1. Understand customer issues thoroughly before responding
2. Provide accurate information based on company policies and knowledge base
3. Always cite specific policy sections or order details when applicable
4. Escalate complex issues to human agents when appropriate
5. Maintain customer satisfaction while following company guidelines

TONE AND STYLE GUIDELINES:
- Professional yet warm and approachable
- Empathetic to customer frustrations
- Clear and concise (avoid jargon)
- Patient and helpful, never defensive
- Positive framing (focus on solutions, not problems)

CONSTRAINTS:
1. NEVER make promises outside company policy
2. NEVER share other customers' information
3. NEVER provide personal opinions on products
4. NEVER process refunds above $500 without human approval
5. ALWAYS verify customer identity before discussing order details
6. ALWAYS provide source citations for policy statements

OUTPUT FORMAT REQUIREMENTS:
Your responses must follow this structure:

1. **Greeting and Acknowledgment**
   - Acknowledge the customer's issue
   - Show empathy

2. **Understanding**
   - Summarize the issue to confirm understanding
   - Ask clarifying questions if needed

3. **Solution/Information**
   - Provide clear, step-by-step guidance
   - Cite relevant policies or sources
   - Include specific timeframes when applicable

4. **Next Steps**
   - Clear action items for customer
   - Expected timeline
   - Follow-up options

5. **Closing**
   - Offer additional assistance
   - Professional sign-off

SOURCE CITATION REQUIREMENTS:
- Format: [Source: Return Policy Section 3.2]
- Required for: All policy statements, timeframes, procedures
- Example: "According to our Refund Policy [Source: Refund Policy v2.1, Section 2.1], refunds are processed within 5-7 business days."

ESCALATION CRITERIA - Escalate to human agent when:
1. **Financial**: Refund or credit > $500
2. **Legal**: Threats of legal action, liability claims
3. **Complex**: Issue involves multiple departments or unclear policy
4. **Emotional**: Customer is highly distressed or aggressive
5. **Technical**: System errors or data discrepancies you cannot resolve
6. **Uncertain**: You're not confident in the accuracy of your response (confidence < 70%)

ESCALATION FORMAT:
"I understand this is a complex situation that requires specialized attention. I'm escalating this to our [Department Name] team who can better assist you. They'll contact you within [Timeframe]. Your case reference number is [Case ID]."

KNOWLEDGE BASE SEARCH:
Before responding:
1. Search knowledge base for relevant policies
2. Verify information is current (check last updated date)
3. Cross-reference with order history if available
4. Use the most specific, relevant information

QUALITY CHECKS:
Before sending response:
- [ ] Issue acknowledged with empathy
- [ ] Solution is clear and actionable
- [ ] Sources cited for all policy statements
- [ ] Next steps are specific
- [ ] Escalation criteria checked
- [ ] Tone is professional and helpful

EXAMPLE RESPONSES:

Good Response:
"I sincerely apologize for the inconvenience with your delivery delay. I understand how frustrating this must be. 

Let me help you track your order #12345. According to our system, your package is currently in transit and expected to arrive by December 15th [Source: Shipping Tracking System]. 

According to our Shipping Policy [Source: Shipping Policy v3.1, Section 2.3], if your package doesn't arrive within 2 business days of the expected date, you're eligible for either a full refund or expedited replacement shipping at no cost.

Next steps:
1. Monitor tracking at [tracking link]
2. If not received by December 17th, contact us for immediate resolution
3. We'll send you a tracking update every 24 hours

Is there anything else I can help you with today?"

Bad Response (Don't do this):
"Your package is delayed. It should come soon. Let me know if you need help."
```

#### **Part B: Chain-of-Thought for Complex Issue**

**Customer Query**: "I was charged twice for an order I never received."

**Chain-of-Thought Prompt**:

```
You are a customer support assistant. A customer says: "I was charged twice for an order I never received."

This is a complex issue. Use step-by-step reasoning to handle it:

STEP 1: IDENTIFY THE COMPONENTS
Think through what's happening:
- Problem 1: Duplicate charge
- Problem 2: Order not received
- Urgency: Financial impact + missing product
- Customer emotion: Likely frustrated/upset

STEP 2: PRIORITIZE ISSUES
Reasoning:
- Duplicate charge = immediate financial impact (high priority)
- Missing order = inconvenience (high priority)
- Both need investigation
Order of resolution: Verify charges → Track order → Provide solution

STEP 3: INFORMATION NEEDED
What information do I need?
- Order number
- Charge amounts and dates
- Expected delivery date
- Current order status
- Customer's account status

STEP 4: CHECK ESCALATION CRITERIA
Is this an escalation case?
- If total charge > $500: YES, escalate to billing team
- If fraud suspected: YES, escalate to fraud team
- If standard case: Handle with standard procedure

STEP 5: SOLUTION PATH
Possible scenarios:
Scenario A: Duplicate charge + order in transit
  → Refund duplicate charge + provide tracking

Scenario B: Duplicate charge + order lost
  → Refund duplicate charge + reship or full refund

Scenario C: System error
  → Investigate with technical team

STEP 6: FORMULATE RESPONSE
Based on reasoning above, provide:
1. Empathetic acknowledgment
2. Request necessary information
3. Explain investigation process
4. Set expectations for timeline
5. Immediate action if possible

Now, generate the response:
```

**Example Response Generated**:

```
I sincerely apologize for this concerning situation - being charged twice for an order you haven't received is absolutely not acceptable, and I'm here to help resolve this immediately.

Let me break down how we'll fix this together:

**Immediate Action Items:**
1. Please provide your order number so I can investigate both charges
2. I'll verify the charge amounts and dates from your account
3. I'll check your order's current delivery status

**Investigation Process:**
I'll need to check three things:
1. **Billing System**: Verify if there are two separate charges or one pending + one posted
2. **Order Status**: Confirm if your order is in transit, lost, or cancelled
3. **Account Review**: Check for any system errors

**What Happens Next:**
- **If duplicate charge confirmed**: I'll process an immediate refund for the duplicate amount (2-3 business days to your account) [Source: Refund Policy Section 2.1]
- **If order is lost/delayed**: We'll either expedite a replacement or provide a full refund for both charges [Source: Shipping Guarantee Section 3.4]
- **If charges > $500 total**: I'll escalate to our Billing Resolution team for same-day handling

**Your Timeline:**
- Investigation: Within 2 hours
- Resolution plan: Same business day
- Refund processing: 2-3 business days [Source: Payment Processing Policy v2.3]

Could you please provide your order number so I can start the investigation right away? If you have screenshots of the duplicate charges, that would be very helpful as well.

I'm committed to resolving this for you today.
```

**Why Chain-of-Thought Helps**:
- **Structured thinking**: Breaks complex issue into manageable parts
- **Better accuracy**: Less likely to miss important aspects
- **Consistent quality**: Follows logical problem-solving process
- **Explainable**: Can trace reasoning if issues arise
- **Comprehensive**: Addresses all aspects of the problem

---

## Question 6: LangChain Application Development (20 points)

### Part A (10 points)
Explain the difference between LangChain's Memory types (ConversationBufferMemory, ConversationSummaryMemory, and ConversationBufferWindowMemory). When would you use each one?

### Part B (10 points)
Design a LangChain-based application that answers questions about a company's HR policies stored in PDF documents. List all components you would use and explain how they work together.

---

### **ANSWER TO QUESTION 6**

#### **Part A: LangChain Memory Types**

**1. ConversationBufferMemory - The Complete History Keeper**

**What it does**:
- Stores **all messages** from the conversation
- Keeps complete history without any loss
- Passes entire conversation to the LLM

**How it works**:
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# User message 1
memory.save_context(
    {"input": "Hello, my name is John"},
    {"output": "Hi John! How can I help you today?"}
)

# User message 2
memory.save_context(
    {"input": "What's my name?"},
    {"output": "Your name is John."}
)

# Memory contains: ALL messages from start to current
print(memory.load_memory_variables({}))
# Output: "Human: Hello, my name is John\nAI: Hi John!...\nHuman: What's my name?\nAI: Your name is John."
```

**When to use**:
- ✅ Short conversations (< 10 exchanges)
- ✅ When complete context is critical
- ✅ Low token limit models aren't an issue
- ✅ Customer support (need full conversation history)

**When NOT to use**:
- ❌ Long conversations (token limit exceeded)
- ❌ Cost-sensitive applications (more tokens = higher cost)
- ❌ Performance-critical systems (processing all history is slow)

**2. ConversationSummaryMemory - The Smart Summarizer**

**What it does**:
- **Summarizes** old messages instead of storing verbatim
- Uses LLM to create concise summaries
- Keeps recent messages in full

**How it works**:
```python
from langchain.memory import ConversationSummaryMemory
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
memory = ConversationSummaryMemory(llm=llm)

# After 10 messages, might summarize to:
# Summary: "The user John is inquiring about return policies for a laptop purchased on Dec 1st. 
# He mentioned the laptop has a defective screen and wants to know about warranty coverage."

# Only recent messages kept in full:
# Human: "How long does the return take?"
# AI: "Returns are processed within 5-7 business days."
```

**When to use**:
- ✅ Long conversations (> 10 exchanges)
- ✅ When context matters but full history isn't needed
- ✅ Token limit constraints
- ✅ Cost optimization (fewer tokens sent)

**When NOT to use**:
- ❌ When exact wording is critical (legal, medical)
- ❌ Short conversations (overhead not worth it)
- ❌ When LLM calls are expensive (summary requires LLM calls)

**3. ConversationBufferWindowMemory - The Recent Focus Keeper**

**What it does**:
- Keeps only the **last K messages**
- Discards older messages completely
- Simple sliding window approach

**How it works**:
```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=2)  # Keep last 2 exchanges

# Messages 1-5 happen...
# Only the last 2 are kept:
# Human: "What's the return policy?"
# AI: "30 days with receipt."
# Human: "Do I need original packaging?"
# AI: "Yes, original packaging is required."

# Earlier messages about user's name, order details are FORGOTTEN
```

**When to use**:
- ✅ Focused conversations (recent context is most important)
- ✅ FAQ chatbots (each question is independent)
- ✅ Token limit constraints
- ✅ Simple, predictable memory usage

**When NOT to use**:
- ❌ When early conversation context is important
- ❌ Multi-step problem solving (need full context)
- ❌ Complex troubleshooting (requires all details)

**Comparison Table**:

| Memory Type | Storage | Use Case | Pros | Cons |
|-------------|---------|----------|------|------|
| Buffer | ALL messages | Short, critical context | Complete history | Token limits |
| Summary | Summarized + recent | Long conversations | Efficient | Summary cost |
| Window | Last K messages | Simple Q&A | Predictable | Lost context |

**Real-World Example**:

**Customer Support (Medical Device)**:
- Use **ConversationBufferMemory**: Need complete history for safety
- Reason: Critical to remember patient details, symptoms mentioned earlier

**FAQ Chatbot (Restaurant Menu)**:
- Use **ConversationBufferWindowMemory (k=2)**: Only recent questions matter
- Reason: "What vegetarian options?" doesn't need previous "What's your hours?"

**Technical Support (Software Troubleshooting)**:
- Use **ConversationSummaryMemory**: Long sessions but need key details
- Reason: Can summarize "tried restarting, still not working" while keeping recent steps

#### **Part B: HR Policy Q&A Application Design**

**Complete LangChain Application Architecture**:

```python
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
```

**Component Breakdown**:

**1. Document Loaders - Getting the Data**:
```python
# Load all HR policy PDFs from directory
loader = DirectoryLoader(
    './hr_policies/',
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)

documents = loader.load()
# Result: List of Document objects with content and metadata
```

**Purpose**: Extract text from HR policy PDFs
**Why this component**: Handles multiple PDF formats, preserves metadata

**2. Text Splitter - Breaking Documents into Chunks**:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Characters per chunk
    chunk_overlap=200,  # Overlap for context preservation
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]  # Try these in order
)

chunks = text_splitter.split_documents(documents)
# Result: ~500 chunks from all HR policies
```

**Purpose**: Create manageable, contextually complete chunks
**Why this component**: Preserves context with overlap, semantic splitting

**3. Embeddings - Converting Text to Vectors**:
```python
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key="your-api-key"
)

# Alternative: Local embeddings for privacy
# from langchain.embeddings import HuggingFaceEmbeddings
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

**Purpose**: Convert text to 1536D vectors for semantic search
**Why this component**: Enables meaning-based search, not just keywords

**4. Vector Store - Storing and Searching**:
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="localhost:6333")

vectorstore = Qdrant(
    client=client,
    collection_name="hr_policies",
    embeddings=embeddings
)

# Add documents to vector store
vectorstore.add_documents(chunks)
```

**Purpose**: Efficient storage and similarity search
**Why this component**: Fast retrieval (HNSW index), production-ready

**5. Retriever - Finding Relevant Information**:
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,  # Return top 5 most relevant chunks
        "score_threshold": 0.7  # Minimum similarity score
    }
)
```

**Purpose**: Configure how documents are retrieved
**Why this component**: Controls relevance threshold and result count

**6. Prompt Template - Structuring the Question**:
```python
template = """You are an HR assistant helping employees understand company policies.

Use the following pieces of context from our HR policy documents to answer the question.
If you don't know the answer, say so - don't make up information.
Always cite the specific policy section you're referencing.

Context from HR Policies:
{context}

Question: {question}

Provide a clear, professional answer that:
1. Directly answers the question
2. Cites the specific policy section
3. Provides any relevant additional information
4. Is easy to understand

Answer:"""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)
```

**Purpose**: Guide the LLM to respond appropriately
**Why this component**: Ensures consistent, policy-compliant responses

**7. LLM - The Brain**:
```python
llm = OpenAI(
    model_name="gpt-4",
    temperature=0.3,  # Low temperature for factual accuracy
    max_tokens=500
)
```

**Purpose**: Generate answers based on retrieved context
**Why this component**: Understands context and generates natural responses

**8. Memory - Conversation Context**:
```python
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    output_key="answer",
    return_messages=True
)
```

**Purpose**: Remember conversation for follow-up questions
**Why this component**: Enables "What about remote work?" after asking about vacation

**9. RetrievalQA Chain - Putting It All Together**:
```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Stuff all context into one prompt
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": PROMPT,
        "memory": memory
    }
)
```

**Purpose**: Coordinate retrieval and generation
**Why this component**: Manages the complete RAG workflow

**Complete Application**:

```python
class HRPolicyAssistant:
    def __init__(self):
        # Initialize all components
        self.setup_document_pipeline()
        self.setup_qa_chain()
    
    def setup_document_pipeline(self):
        """Setup document processing"""
        # Load documents
        loader = DirectoryLoader('./hr_policies/', glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Qdrant.from_documents(
            self.chunks,
            embeddings,
            url="localhost:6333",
            collection_name="hr_policies"
        )
    
    def setup_qa_chain(self):
        """Setup QA chain"""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        llm = OpenAI(model_name="gpt-4", temperature=0.3)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            memory=memory
        )
    
    def ask(self, question: str):
        """Ask question about HR policies"""
        result = self.qa_chain({"query": question})
        
        # Format response with sources
        answer = result['result']
        sources = result['source_documents']
        
        response = f"{answer}\n\nSources:\n"
        for i, source in enumerate(sources, 1):
            response += f"[{i}] {source.metadata['source']} - Page {source.metadata.get('page', 'N/A')}\n"
        
        return response

# Usage
hr_assistant = HRPolicyAssistant()
answer = hr_assistant.ask("What is the vacation policy?")
print(answer)
```

**How Components Work Together**:

1. **User asks question** → "What's the vacation policy?"
2. **Embeddings** convert question to vector
3. **Retriever** searches vector store for top 5 similar chunks
4. **Prompt Template** combines question + retrieved chunks
5. **LLM** generates answer based on context
6. **Memory** stores conversation for follow-up questions
7. **Application** returns answer with source citations

**Complete Data Flow**:
```
User Question 
    ↓
Embedding Model (Convert to vector)
    ↓
Vector Store (Search similar chunks)
    ↓
Retriever (Get top 5 relevant chunks)
    ↓
Prompt Template (Combine question + chunks)
    ↓
LLM (Generate answer)
    ↓
Memory (Store for follow-ups)
    ↓
Return Answer + Sources
```

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

### **ANSWER TO QUESTION 7**

#### **Part A: Chunking Strategy Comparison**

**1. Fixed-Size Chunking (512 tokens)**

**How it works**:
```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separator="\n"
)

chunks = splitter.split_text(manual_text)
# Result: Chunks of exactly 512 tokens each
```

**Advantages**:
- ✅ Simple and predictable
- ✅ Consistent chunk sizes (good for batch processing)
- ✅ Easy to implement and debug
- ✅ Works with any content type

**Disadvantages**:
- ❌ Breaks mid-sentence or mid-code block
- ❌ Loses context boundaries
- ❌ Code snippets might be split incorrectly
- ❌ Tables can be broken across chunks

**Example Problem**:
```
Chunk 1: "...To configure the database connection, follow these steps:
1. Open the config file
2. Set the database URL to postgre..."

Chunk 2: "...sql://localhost:5432
3. Save the file
4. Restart the application..."

❌ Neither chunk is complete or useful alone!
```

**2. Semantic Chunking (by meaning)**

**How it works**:
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "],  # Try semantic boundaries first
)

chunks = splitter.split_text(manual_text)
# Result: Chunks split at natural boundaries (paragraphs, sentences)
```

**Advantages**:
- ✅ Preserves meaning and context
- ✅ Chunks make sense independently
- ✅ Better retrieval quality
- ✅ Natural language boundaries respected

**Disadvantages**:
- ❌ Variable chunk sizes (harder to batch)
- ❌ May still break code blocks
- ❌ Requires understanding of content structure
- ❌ More complex implementation

**Example Success**:
```
Chunk 1: "Database Configuration:
To configure the database connection, follow these steps:
1. Open the config file (config/database.yml)
2. Set the database URL to postgresql://localhost:5432
3. Configure authentication credentials
4. Save the file and restart the application

Note: Ensure PostgreSQL is running before starting."

✅ Complete, self-contained, useful!
```

**3. Hierarchical Chunking (by document structure)**

**How it works**:
```python
def hierarchical_chunking(manual):
    chunks = []
    
    for section in manual.sections:
        # Create chunk for section header
        chunks.append({
            "content": section.title + "\n" + section.intro,
            "metadata": {
                "type": "section_intro",
                "section": section.title,
                "hierarchy": "level_1"
            }
        })
        
        for subsection in section.subsections:
            # Create chunk for each subsection
            chunks.append({
                "content": subsection.full_content,
                "metadata": {
                    "type": "subsection",
                    "section": section.title,
                    "subsection": subsection.title,
                    "hierarchy": "level_2"
                }
            })
    
    return chunks
```

**Advantages**:
- ✅ Preserves document structure
- ✅ Maintains hierarchical context (section → subsection)
- ✅ Respects code blocks and tables
- ✅ Metadata-rich (enables filtering)

**Disadvantages**:
- ❌ Variable chunk sizes (some sections huge, others tiny)
- ❌ Requires document structure parsing
- ❌ Complex implementation
- ❌ Doesn't work for unstructured documents

**Example**:
```
Chunk 1 (Section Introduction):
"Chapter 3: Database Configuration
This chapter covers all aspects of database setup and configuration..."
Metadata: {section: "Database", hierarchy: "chapter"}

Chunk 2 (Subsection):
"3.1 PostgreSQL Setup
To set up PostgreSQL:
[Complete instructions with code...]"
Metadata: {section: "Database", subsection: "PostgreSQL", hierarchy: "subsection"}

✅ Preserves structure, enables "search only in Database section" queries
```

**Comparison for Technical Manual**:

| Strategy | Best For | Accuracy | Complexity |
|----------|----------|----------|------------|
| Fixed-size | Simple content | Medium | Low |
| Semantic | Natural language | High | Medium |
| Hierarchical | Structured docs | Very High | High |

**Recommendation**: **Hierarchical Chunking with Semantic Fallback**
- Use hierarchical for sections with clear structure
- Use semantic for unstructured sections
- Preserve code blocks and tables as single chunks

#### **Part B: Optimal Chunking Strategy Design**

**Hybrid Chunking Strategy for Technical Manual**:

**Parameters**:
```python
CHUNKING_CONFIG = {
    # Size parameters
    "max_chunk_size": 1000,  # tokens
    "min_chunk_size": 200,   # tokens
    "overlap": 150,          # tokens overlap between chunks
    
    # Structure parameters
    "respect_boundaries": [
        "```",  # Code blocks
        "|---|", # Tables
        "####", # Subsection headers
        "\n\n"  # Paragraphs
    ],
    
    # Metadata
    "include_metadata": [
        "section_title",
        "page_number",
        "document_name",
        "content_type"  # (text, code, table)
    ]
}
```

**Implementation**:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

class TechnicalManualChunker:
    def __init__(self, config):
        self.config = config
        self.base_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config["max_chunk_size"],
            chunk_overlap=config["overlap"],
            length_function=len
        )
    
    def chunk_manual(self, manual_text, metadata):
        chunks = []
        
        # Step 1: Identify and protect special content
        protected_blocks = self._extract_protected_blocks(manual_text)
        
        # Step 2: Split by document structure
        sections = self._split_by_structure(manual_text)
        
        for section in sections:
            section_chunks = self._chunk_section(section, protected_blocks)
            
            # Add metadata to each chunk
            for chunk in section_chunks:
                chunk["metadata"] = {
                    **metadata,
                    "section": section["title"],
                    "content_type": chunk["type"]
                }
                chunks.append(chunk)
        
        return chunks
    
    def _extract_protected_blocks(self, text):
        """Extract code blocks and tables that shouldn't be split"""
        protected = {
            "code_blocks": re.findall(r'```[\s\S]*?```', text),
            "tables": re.findall(r'\|.*\|[\s\S]*?\n\n', text)
        }
        return protected
    
    def _chunk_section(self, section, protected_blocks):
        """Chunk a section while preserving protected blocks"""
        chunks = []
        content = section["content"]
        
        # Check if section contains protected blocks
        for code_block in protected_blocks["code_blocks"]:
            if code_block in content:
                # Keep code block as single chunk if reasonable size
                if len(code_block) < self.config["max_chunk_size"]:
                    chunks.append({
                        "content": section["title"] + "\n\n" + code_block,
                        "type": "code"
                    })
                    content = content.replace(code_block, "[CODE_BLOCK_EXTRACTED]")
        
        # Chunk remaining content semantically
        text_chunks = self.base_splitter.split_text(content)
        for chunk in text_chunks:
            if chunk.strip() and chunk != "[CODE_BLOCK_EXTRACTED]":
                chunks.append({
                    "content": section["title"] + "\n\n" + chunk,
                    "type": "text"
                })
        
        return chunks
```

**Example Output**:

```
Chunk 1:
Content: "3.1 Database Connection Setup

To connect to PostgreSQL database:
```python
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="admin",
    password="secret"
)
```
This establishes a connection to your database."

Metadata: {
    "section": "Database Configuration",
    "subsection": "Connection Setup",
    "page": 42,
    "content_type": "code",
    "document": "technical_manual.pdf"
}

Chunk 2:
Content: "3.2 Query Execution

Once connected, you can execute SQL queries using the cursor object.
Always use parameterized queries to prevent SQL injection..."

Metadata: {
    "section": "Database Configuration",
    "subsection": "Query Execution",
    "page": 43,
    "content_type": "text",
    "document": "technical_manual.pdf"
}
```

**Context Preservation Strategies**:

**1. Overlap**:
```
Chunk 1: "...step 3: Configure authentication. Step 4: Test connection..."
Chunk 2: "...Step 4: Test connection. Step 5: Handle errors..."
           ^^^^^^^^^^^^^^^^^^^^^^^^^ (overlap ensures context)
```

**2. Section Headers in Every Chunk**:
```
Each chunk starts with its section title:
"3.1 Database Connection Setup\n\n[content]"
```

**3. Metadata Enrichment**:
```
{
    "section": "Database",
    "subsection": "Connection",
    "previous_subsection": "Installation",
    "next_subsection": "Queries"
}
```

**Benefits of This Strategy**:
- ✅ Code blocks preserved (can copy-paste and run)
- ✅ Tables kept intact (remain readable)
- ✅ Context maintained (overlap + headers)
- ✅ Searchable by section (metadata filtering)
- ✅ Efficient retrieval (optimized chunk sizes)

---



## Question 8: RAG vs Traditional LLM (15 points)

**Compare and contrast these two approaches for a legal research system:**

**Approach A**: Fine-tune a large language model on legal documents

**Approach B**: Use RAG with a vector database of legal documents

Your answer should cover: Cost implications, update frequency, accuracy, source attribution, and scalability.

---

### **ANSWER TO QUESTION 8**

**Recommendation**: **Use RAG** for legal research because source attribution is mandatory, law changes frequently requiring fast updates, and it's more cost-effective ($100K-$350K vs $1.2M-$2.2M over 5 years).

**Key Points**:
- RAG provides exact citations (critical for legal)
- RAG updates in real-time (law changes daily)
- RAG has lower hallucination risk (grounded in sources)
- Fine-tuning is expensive and slow to update
- RAG scales easily as legal database grows

---

## Question 9: Vector Database Query Optimization (20 points)

**Scenario**: Your vector database search queries are taking 500ms on average, but you need to reduce this to under 100ms.

### Part A (10 points)
Describe 5 specific optimization techniques.

### Part B (10 points)
Explain KNN vs ANN trade-offs.

---

### **ANSWER TO QUESTION 9**

#### **Part A: 5 Optimization Techniques**

1. **Switch to HNSW Index**: 10x faster (500ms → 50ms)
2. **Implement Redis Caching**: 50x faster for cached queries (50ms → 1ms)
3. **Use Int8 Quantization**: 3-4x faster (50ms → 15ms)
4. **Pre-filter by Metadata**: 10x faster (50ms → 5ms) by searching smaller subset
5. **Batch Parallel Processing**: 25x faster for multiple queries

**Combined Result**: 500ms → 1-10ms (500x improvement)

#### **Part B: KNN vs ANN**

**Exact (KNN)**:
- 100% accuracy, slow (O(n))
- Use for: Small datasets, critical accuracy, legal/medical

**Approximate (ANN)**:
- 95%+ accuracy, fast (O(log n))
- Use for: Large datasets, real-time systems, e-commerce

**Decision**: Sacrifice exact for speed when dataset > 1M vectors and 95% accuracy is acceptable.

---

## Question 10: Real-World Integration Challenge (30 points)

Build a "Smart Research Assistant" for university researchers.

---

### **ANSWER TO QUESTION 10**

#### **Complete System Design**

**Technology Stack**:
- **RAG Architecture**: Hybrid RAG (multiple search methods)
- **Vector Database**: Qdrant (self-hosted, cost-effective)
- **Embedding Model**: OpenAI Ada-002 (1536D, best semantic understanding)
- **Similarity Metric**: Cosine Similarity (ignores document length)
- **LLM**: GPT-4 (best for academic language)

**Document Processing**:
1. **Extract**: PyMuPDF for text, OCR for images, table detection
2. **Chunk**: Hierarchical by paper sections (Abstract, Methods, Results)
3. **Images**: CLIP embeddings + OCR text combined
4. **Tables**: Convert to markdown, extract key findings
5. **Metadata**: Authors, year, journal, DOI, citations

**Retrieval Strategy**:
1. **Hybrid Search**: Semantic + Keyword + Citation graph
2. **Multi-hop**: Break complex queries into sub-questions
3. **Reranking**: Cross-encoder for final selection
4. **Quality Checks**: Verify facts against sources
5. **Citations**: Auto-generate APA format citations

**Update Handling**:
- Daily batch processing for new papers
- Incremental vector DB updates
- Citation graph updates
- < 24 hour lag for new publications

**Expected Performance**:
- Search: 50-100ms
- Total response: 2-3 seconds
- Accuracy: >95%
- Citation accuracy: 100%

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

## ⏱️ Time Management Guide for Students

**Total Time**: 3 hours (180 minutes)

**Recommended Allocation**:
- Q1-Q3 (Shorter answers): 45 minutes
- Q4-Q7 (Design questions): 60 minutes  
- Q8-Q9 (Analysis): 30 minutes
- Q10 (Comprehensive): 30 minutes
- Review: 15 minutes

---

**End of Interim Exam - Questions and Detailed Answers**

*This exam comprehensively tests students' understanding of LLM fundamentals, vector databases, RAG systems, prompt engineering, LangChain framework, and practical implementation skills.*

