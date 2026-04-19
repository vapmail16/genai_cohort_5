"""
Test scenarios and prompts for LangSmith demo
"""

# Sample test prompts for different use cases
TEST_PROMPTS = {
    "qa_prompts": [
        "What are the benefits of using LangSmith for LLM monitoring?",
        "How does token tracking help in cost optimization?",
        "What metrics are most important for LLM applications?",
        "Explain the difference between prompt and completion tokens",
        "What is the purpose of tracing in LLM development?"
    ],

    "summarization_texts": [
        """
        LangSmith is a comprehensive platform designed for building, testing, and monitoring
        production-grade LLM applications. It provides developers with powerful debugging tools,
        evaluation capabilities, and monitoring features that seamlessly integrate with popular
        frameworks like LangChain. The platform enables teams to track performance metrics,
        analyze token usage, monitor costs, and identify errors in real-time, making it easier
        to optimize and maintain LLM applications at scale.
        """,
        """
        Token usage in LLM applications directly impacts both performance and cost. Each API call
        consumes tokens based on the input prompt and generated output. Understanding token consumption
        patterns helps developers optimize prompts, reduce unnecessary verbosity, and implement
        efficient caching strategies. By monitoring token usage across different models and use cases,
        teams can make informed decisions about model selection and prompt engineering.
        """,
        """
        Error handling in LLM applications requires careful consideration of various failure modes.
        Common errors include rate limiting, timeout issues, invalid API keys, and content filtering
        violations. Implementing robust error handling with exponential backoff, retry logic, and
        fallback mechanisms ensures application reliability. LangSmith's error tracking capabilities
        help developers identify patterns in failures and implement targeted fixes.
        """
    ],

    "code_generation_tasks": [
        "calculates the factorial of a number recursively",
        "implements a binary search algorithm",
        "creates a decorator for timing function execution",
        "generates a REST API endpoint with error handling",
        "builds a cache with LRU eviction policy"
    ],

    "translation_samples": [
        {
            "text": "LangSmith helps developers build better LLM applications.",
            "target_languages": ["Spanish", "French", "German", "Japanese", "Portuguese"]
        },
        {
            "text": "Monitor your token usage to optimize costs and performance.",
            "target_languages": ["Italian", "Dutch", "Korean", "Chinese", "Russian"]
        }
    ],

    "complex_prompts": [
        {
            "type": "analysis",
            "prompt": """Analyze the following metrics data and provide insights:
            - Total tokens used: 150,000
            - Average response time: 2.3 seconds
            - Error rate: 3.2%
            - Cost per 1000 tokens: $0.002
            Suggest optimization strategies."""
        },
        {
            "type": "comparison",
            "prompt": """Compare GPT-3.5-turbo and GPT-4 for the following use case:
            A customer service chatbot that needs to handle technical queries about
            software products, provide troubleshooting steps, and escalate complex issues."""
        },
        {
            "type": "reasoning",
            "prompt": """A company is seeing increased LLM costs. Their metrics show:
            - 70% of requests use GPT-4
            - Average prompt length: 500 tokens
            - Average completion: 200 tokens
            - Daily request volume: 10,000
            What cost optimization strategies would you recommend?"""
        }
    ],

    "error_inducing_prompts": [
        # These are designed to potentially trigger errors for testing
        {
            "description": "Extremely long prompt to test token limits",
            "prompt": "Explain in detail " + "the history of computing " * 500
        },
        {
            "description": "Prompt with special characters",
            "prompt": "Parse this: ```\\x00\\x01\\x02\\x03```"
        },
        {
            "description": "Request for inappropriate content (should be filtered)",
            "prompt": "Generate content that violates OpenAI usage policies"
        }
    ]
}

# Batch processing scenarios
BATCH_SCENARIOS = [
    {
        "name": "Customer Support Batch",
        "description": "Process multiple customer queries",
        "prompts": [
            "How do I reset my password?",
            "What are your refund policies?",
            "My order hasn't arrived yet, order #12345",
            "How do I upgrade my subscription?",
            "Technical issue: app crashes on startup"
        ]
    },
    {
        "name": "Content Generation Batch",
        "description": "Generate multiple content pieces",
        "prompts": [
            "Write a tweet about AI safety",
            "Create a LinkedIn post about LangSmith benefits",
            "Draft an email subject line for a product launch",
            "Write a brief product description for an LLM monitoring tool",
            "Generate a catchy tagline for a DevOps platform"
        ]
    }
]

# Performance testing scenarios
PERFORMANCE_TESTS = {
    "latency_test": {
        "description": "Test response times across different prompt sizes",
        "small_prompt": "Hi",
        "medium_prompt": "Explain machine learning in one paragraph",
        "large_prompt": "Provide a comprehensive guide on building production-ready LLM applications, covering architecture, best practices, monitoring, testing, deployment strategies, and common pitfalls to avoid"
    },

    "concurrent_requests": {
        "description": "Test handling multiple simultaneous requests",
        "num_requests": 10,
        "prompt": "Generate a random fact about technology"
    },

    "model_comparison": {
        "description": "Compare performance across different models",
        "prompt": "Solve this problem: If a train travels 120 miles in 2 hours, what is its average speed?",
        "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
    }
}

def get_random_test_scenario():
    """Get a random test scenario for demo purposes"""
    import random

    scenario_type = random.choice(["qa", "summary", "code", "translation"])

    if scenario_type == "qa":
        return {
            "type": "qa",
            "prompt": random.choice(TEST_PROMPTS["qa_prompts"])
        }
    elif scenario_type == "summary":
        return {
            "type": "summarization",
            "text": random.choice(TEST_PROMPTS["summarization_texts"])
        }
    elif scenario_type == "code":
        return {
            "type": "code_generation",
            "task": random.choice(TEST_PROMPTS["code_generation_tasks"])
        }
    else:
        sample = random.choice(TEST_PROMPTS["translation_samples"])
        return {
            "type": "translation",
            "text": sample["text"],
            "target_language": random.choice(sample["target_languages"])
        }

if __name__ == "__main__":
    # Example usage
    print("Sample Test Scenario:")
    print(get_random_test_scenario())