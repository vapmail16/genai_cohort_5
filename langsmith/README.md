# LangSmith Metrics Demo

A comprehensive demonstration of LangSmith's capabilities for monitoring and tracking key metrics in LLM applications, including token usage, costs, errors, and execution time.

## Features

### Core Metrics Tracking
- **Token Usage**: Track prompt, completion, and total tokens
- **Cost Analysis**: Monitor costs per run, per model, and cumulative costs
- **Performance Metrics**: Measure execution time and latency
- **Error Tracking**: Capture and analyze failure patterns
- **Model Comparison**: Compare metrics across different GPT models

### Components

1. **Main Demo Script** (`langsmith_demo.py`)
   - LangSmith integration with OpenAI
   - Multiple chain types (QA, Summarization, Code Generation, Translation)
   - Automatic metrics collection
   - Error simulation for testing
   - JSON export of metrics

2. **Test Scenarios** (`test_scenarios.py`)
   - Predefined test prompts and scenarios
   - Batch processing examples
   - Performance testing scenarios
   - Error-inducing prompts for testing

3. **Metrics Dashboard** (`metrics_dashboard.py`)
   - Interactive Streamlit dashboard
   - Real-time visualization of metrics
   - Filtering and analysis tools
   - Export capabilities (CSV, JSON)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- LangSmith API key (get from [smith.langchain.com](https://smith.langchain.com))

### Installation

1. **Navigate to the langsmith folder:**
```bash
cd langsmith
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file in the langsmith folder:**
```bash
touch .env
```

4. **Add your API keys to the `.env` file:**
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

## Usage

### Running the Demo

1. **Execute the main demo script:**
```bash
python langsmith_demo.py
```

This will:
- Run multiple test scenarios
- Collect metrics for each run
- Simulate some error conditions
- Generate a comprehensive metrics report
- Save results to `metrics_log.json`

### Sample Output
```
============================================================
LangSmith Metrics Demo
============================================================

--- Running Test Scenarios ---

Scenario 1: qa with gpt-3.5-turbo
✓ Success - Tokens: 245, Cost: $0.000367, Time: 1.234s

Scenario 2: summary with gpt-3.5-turbo
✓ Success - Tokens: 189, Cost: $0.000283, Time: 0.987s

...

============================================================
METRICS REPORT
============================================================

📊 Summary:
   • Total Runs: 5
   • Success Rate: 80.0%
   • Failed Runs: 1

🪙 Token Usage:
   • Total Tokens: 1,234
   • Prompt Tokens: 834
   • Completion Tokens: 400
   • Avg Tokens/Run: 246.8

💰 Cost Analysis:
   • Total Cost: $0.0234
   • Avg Cost/Run: $0.00468

   Cost by Model:
   • gpt-3.5-turbo:
     - Total: $0.0089
     - Avg: $0.00297
     - Runs: 3
   • gpt-4:
     - Total: $0.0145
     - Avg: $0.00725
     - Runs: 2

⏱️ Performance:
   • Total Time: 6.543s
   • Avg Time/Run: 1.309s
   • Fastest Run: 0.876s
   • Slowest Run: 2.145s
```

### Viewing the Dashboard

1. **Launch the Streamlit dashboard:**
```bash
streamlit run metrics_dashboard.py
```

2. **Open your browser to the URL shown (typically `http://localhost:8501`)**

3. **Dashboard Features:**
   - Filter by model and chain type
   - View token usage trends
   - Analyze cost breakdown
   - Monitor performance metrics
   - Track error patterns
   - Export data for further analysis

### Monitoring in LangSmith

1. **Visit [smith.langchain.com](https://smith.langchain.com)**
2. **Navigate to your project: `langsmith-metrics-demo`**
3. **View detailed traces for each run:**
   - Input/output pairs
   - Token counts
   - Latency breakdown
   - Error details

## Key Metrics Explained

### Token Usage
- **Prompt Tokens**: Tokens in the input prompt
- **Completion Tokens**: Tokens in the model's response
- **Total Tokens**: Sum of prompt and completion tokens

### Cost Calculation
- Based on OpenAI's pricing model
- Different rates for different models
- Calculated per 1000 tokens

### Performance Metrics
- **Execution Time**: Total time for API call
- **Latency**: Network and processing delay
- **Throughput**: Requests per second capability

### Error Types
- **API Errors**: Rate limits, authentication issues
- **Content Filtering**: Policy violations
- **Timeout Errors**: Long-running requests
- **Network Errors**: Connection issues

## Customization

### Adding New Chain Types

Edit `langsmith_demo.py` to add new chains:
```python
# Example: Add a new chain for sentiment analysis
sentiment_prompt = ChatPromptTemplate.from_template(
    "Analyze the sentiment of this text: {text}"
)
chains["sentiment"] = LLMChain(llm=self.models["gpt-3.5-turbo"], prompt=sentiment_prompt)
```

### Modifying Test Scenarios

Edit `test_scenarios.py` to add custom prompts:
```python
TEST_PROMPTS["custom_prompts"] = [
    "Your custom prompt here",
    "Another test prompt"
]
```

### Dashboard Customization

The Streamlit dashboard can be customized in `metrics_dashboard.py`:
- Add new visualizations
- Modify color schemes
- Add additional metrics
- Customize export formats

## Best Practices

1. **API Key Security**
   - Never commit `.env` files to version control
   - Use environment variables for production
   - Rotate keys regularly

2. **Cost Optimization**
   - Use GPT-3.5-turbo for simple tasks
   - Implement caching for repeated queries
   - Monitor token usage regularly

3. **Error Handling**
   - Implement retry logic with exponential backoff
   - Log all errors for analysis
   - Set up alerts for high error rates

4. **Performance**
   - Batch similar requests when possible
   - Use async operations for concurrent requests
   - Monitor and optimize slow queries

## Troubleshooting

### Common Issues

1. **"API key not found" error:**
   - Ensure `.env` file exists in the langsmith folder
   - Verify API keys are correctly set
   - Check for extra spaces in the `.env` file

2. **"Module not found" error:**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+
   - Check virtual environment activation

3. **Dashboard not loading:**
   - Verify Streamlit is installed: `pip install streamlit`
   - Check if port 8501 is available
   - Try `streamlit run metrics_dashboard.py --server.port 8502`

4. **No metrics showing in dashboard:**
   - Run `python langsmith_demo.py` first to generate data
   - Check if `metrics_log.json` exists
   - Verify file permissions

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com)
- [LangChain Documentation](https://python.langchain.com)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

## License

This demo is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review LangSmith documentation
3. Check OpenAI API status

---

**Note**: This demo uses OpenAI's API which incurs costs. Start with small test runs and monitor your usage on the OpenAI dashboard.