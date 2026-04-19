"""
LangSmith Demo Script
Demonstrates key metrics: token usage, cost, errors, and execution time
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import asyncio
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks.manager import get_openai_callback
from langsmith import Client
import openai

# Load environment variables
load_dotenv()

class LangSmithMetricsDemo:
    """Demo class to showcase LangSmith metrics tracking"""

    def __init__(self):
        """Initialize LangSmith client and OpenAI"""
        # Set up API keys
        self.langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.langsmith_api_key or not self.openai_api_key:
            raise ValueError("Please set LANGSMITH_API_KEY and OPENAI_API_KEY in .env file")

        # Initialize LangSmith client
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = self.langsmith_api_key
        os.environ["LANGCHAIN_PROJECT"] = "langsmith-metrics-demo"

        self.client = Client()

        # Initialize OpenAI with different models for cost comparison
        self.models = {
            "gpt-3.5-turbo": ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
            "gpt-4": ChatOpenAI(model="gpt-4", temperature=0.7),
            "gpt-4-turbo": ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.7)
        }

        # Metrics storage
        self.metrics = []

    def create_test_chains(self) -> Dict[str, Any]:
        """Create different chains for testing using new LangChain pattern"""
        chains = {}
        output_parser = StrOutputParser()

        # Simple QA Chain
        qa_prompt = ChatPromptTemplate.from_template(
            "Answer the following question concisely: {question}"
        )
        chains["qa"] = qa_prompt | self.models["gpt-3.5-turbo"] | output_parser

        # Summarization Chain
        summary_prompt = ChatPromptTemplate.from_template(
            "Summarize the following text in 3 bullet points:\n\n{text}"
        )
        chains["summary"] = summary_prompt | self.models["gpt-3.5-turbo"] | output_parser

        # Code Generation Chain
        code_prompt = ChatPromptTemplate.from_template(
            "Write a Python function that {task}. Include docstring and type hints."
        )
        chains["code_gen"] = code_prompt | self.models["gpt-4"] | output_parser

        # Translation Chain
        translation_prompt = ChatPromptTemplate.from_template(
            "Translate the following text to {target_language}:\n\n{text}"
        )
        chains["translation"] = translation_prompt | self.models["gpt-3.5-turbo"] | output_parser

        return chains

    def run_with_metrics(self, chain: Any, inputs: Dict[str, Any],
                        chain_name: str, model_name: str) -> Dict[str, Any]:
        """Run a chain and collect metrics"""

        start_time = time.time()
        metrics_entry = {
            "chain_name": chain_name,
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs,
            "success": False
        }

        try:
            # Use OpenAI callback to track token usage
            with get_openai_callback() as cb:
                result = chain.invoke(inputs)

                # Calculate metrics
                execution_time = time.time() - start_time

                metrics_entry.update({
                    "success": True,
                    "output": result if isinstance(result, str) else str(result),
                    "execution_time_seconds": round(execution_time, 3),
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost_usd": round(cb.total_cost, 6),
                    "error": None
                })

        except Exception as e:
            execution_time = time.time() - start_time
            metrics_entry.update({
                "success": False,
                "output": None,
                "execution_time_seconds": round(execution_time, 3),
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_cost_usd": 0,
                "error": str(e)
            })

        self.metrics.append(metrics_entry)
        return metrics_entry

    def simulate_error_scenario(self):
        """Intentionally create error scenarios for testing"""
        print("\n--- Simulating Error Scenarios ---")

        # Invalid API key scenario
        try:
            bad_llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                openai_api_key="invalid-key"
            )
            prompt = ChatPromptTemplate.from_template("Test: {input}")
            output_parser = StrOutputParser()
            chain = prompt | bad_llm | output_parser

            result = self.run_with_metrics(
                chain=chain,
                inputs={"input": "This should fail"},
                chain_name="error_test",
                model_name="gpt-3.5-turbo"
            )
            print(f"Error test result: {result['error']}")
        except Exception as e:
            print(f"Expected error occurred: {e}")

    def run_demo_scenarios(self):
        """Run various demo scenarios"""
        print("Setting up demo chains...")
        chains = self.create_test_chains()

        # Test scenarios
        test_cases = [
            {
                "chain": "qa",
                "model": "gpt-3.5-turbo",
                "inputs": {"question": "What are the benefits of using LangSmith for LLM monitoring?"}
            },
            {
                "chain": "summary",
                "model": "gpt-3.5-turbo",
                "inputs": {
                    "text": """LangSmith is a platform for building production-grade LLM applications.
                    It lets you debug, test, evaluate, and monitor chains and intelligent agents built
                    on any LLM framework and seamlessly integrates with LangChain, the go-to open source
                    framework for building with LLMs. LangSmith is developed by LangChain, the company
                    behind the open source LangChain framework."""
                }
            },
            {
                "chain": "code_gen",
                "model": "gpt-4",
                "inputs": {"task": "calculates the factorial of a number recursively"}
            },
            {
                "chain": "translation",
                "model": "gpt-3.5-turbo",
                "inputs": {
                    "text": "LangSmith helps developers build better LLM applications.",
                    "target_language": "Spanish"
                }
            }
        ]

        print("\n--- Running Test Scenarios ---")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nScenario {i}: {test_case['chain']} with {test_case['model']}")

            chain = chains[test_case["chain"]]

            # Update the model for specific chains if needed
            if test_case["chain"] == "code_gen":
                # Code gen uses gpt-4
                pass
            else:
                # Recreate chain with specified model
                output_parser = StrOutputParser()
                if test_case["chain"] == "qa":
                    prompt = ChatPromptTemplate.from_template(
                        "Answer the following question concisely: {question}"
                    )
                elif test_case["chain"] == "summary":
                    prompt = ChatPromptTemplate.from_template(
                        "Summarize the following text in 3 bullet points:\n\n{text}"
                    )
                elif test_case["chain"] == "translation":
                    prompt = ChatPromptTemplate.from_template(
                        "Translate the following text to {target_language}:\n\n{text}"
                    )

                if test_case["chain"] != "code_gen":
                    chain = prompt | self.models[test_case["model"]] | output_parser

            result = self.run_with_metrics(
                chain=chain,
                inputs=test_case["inputs"],
                chain_name=test_case["chain"],
                model_name=test_case["model"]
            )

            if result["success"]:
                print(f"✓ Success - Tokens: {result['total_tokens']}, Cost: ${result['total_cost_usd']}, Time: {result['execution_time_seconds']}s")
            else:
                print(f"✗ Failed - Error: {result['error']}")

    def generate_metrics_report(self) -> Dict[str, Any]:
        """Generate a comprehensive metrics report"""
        if not self.metrics:
            return {"error": "No metrics data available"}

        successful_runs = [m for m in self.metrics if m["success"]]
        failed_runs = [m for m in self.metrics if not m["success"]]

        report = {
            "summary": {
                "total_runs": len(self.metrics),
                "successful_runs": len(successful_runs),
                "failed_runs": len(failed_runs),
                "success_rate": round(len(successful_runs) / len(self.metrics) * 100, 2) if self.metrics else 0
            },
            "token_usage": {
                "total_tokens": sum(m["total_tokens"] for m in successful_runs),
                "total_prompt_tokens": sum(m["prompt_tokens"] for m in successful_runs),
                "total_completion_tokens": sum(m["completion_tokens"] for m in successful_runs),
                "avg_tokens_per_run": round(sum(m["total_tokens"] for m in successful_runs) / len(successful_runs), 2) if successful_runs else 0
            },
            "cost_analysis": {
                "total_cost_usd": round(sum(m["total_cost_usd"] for m in successful_runs), 4),
                "avg_cost_per_run": round(sum(m["total_cost_usd"] for m in successful_runs) / len(successful_runs), 6) if successful_runs else 0,
                "cost_by_model": {}
            },
            "performance": {
                "total_execution_time": round(sum(m["execution_time_seconds"] for m in self.metrics), 2),
                "avg_execution_time": round(sum(m["execution_time_seconds"] for m in self.metrics) / len(self.metrics), 3) if self.metrics else 0,
                "fastest_run": min(m["execution_time_seconds"] for m in self.metrics) if self.metrics else 0,
                "slowest_run": max(m["execution_time_seconds"] for m in self.metrics) if self.metrics else 0
            },
            "errors": [
                {
                    "chain": m["chain_name"],
                    "error": m["error"],
                    "timestamp": m["timestamp"]
                }
                for m in failed_runs
            ]
        }

        # Calculate cost by model
        for metric in successful_runs:
            model = metric["model"]
            if model not in report["cost_analysis"]["cost_by_model"]:
                report["cost_analysis"]["cost_by_model"][model] = {
                    "total_cost": 0,
                    "run_count": 0,
                    "avg_cost": 0
                }

            report["cost_analysis"]["cost_by_model"][model]["total_cost"] += metric["total_cost_usd"]
            report["cost_analysis"]["cost_by_model"][model]["run_count"] += 1

        # Calculate average costs per model
        for model in report["cost_analysis"]["cost_by_model"]:
            model_data = report["cost_analysis"]["cost_by_model"][model]
            model_data["avg_cost"] = round(
                model_data["total_cost"] / model_data["run_count"], 6
            ) if model_data["run_count"] > 0 else 0
            model_data["total_cost"] = round(model_data["total_cost"], 6)

        return report

    def save_metrics(self, filename: str = "metrics_log.json"):
        """Save metrics to a JSON file"""
        with open(filename, "w") as f:
            json.dump({
                "metrics": self.metrics,
                "report": self.generate_metrics_report()
            }, f, indent=2)
        print(f"\nMetrics saved to {filename}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("LangSmith Metrics Demo")
    print("=" * 60)

    try:
        # Initialize demo
        demo = LangSmithMetricsDemo()

        # Run demo scenarios
        demo.run_demo_scenarios()

        # Simulate error scenarios
        demo.simulate_error_scenario()

        # Generate and display report
        print("\n" + "=" * 60)
        print("METRICS REPORT")
        print("=" * 60)

        report = demo.generate_metrics_report()

        print(f"\n📊 Summary:")
        print(f"   • Total Runs: {report['summary']['total_runs']}")
        print(f"   • Success Rate: {report['summary']['success_rate']}%")
        print(f"   • Failed Runs: {report['summary']['failed_runs']}")

        print(f"\n🪙 Token Usage:")
        print(f"   • Total Tokens: {report['token_usage']['total_tokens']:,}")
        print(f"   • Prompt Tokens: {report['token_usage']['total_prompt_tokens']:,}")
        print(f"   • Completion Tokens: {report['token_usage']['total_completion_tokens']:,}")
        print(f"   • Avg Tokens/Run: {report['token_usage']['avg_tokens_per_run']}")

        print(f"\n💰 Cost Analysis:")
        print(f"   • Total Cost: ${report['cost_analysis']['total_cost_usd']}")
        print(f"   • Avg Cost/Run: ${report['cost_analysis']['avg_cost_per_run']}")

        if report['cost_analysis']['cost_by_model']:
            print(f"\n   Cost by Model:")
            for model, data in report['cost_analysis']['cost_by_model'].items():
                print(f"   • {model}:")
                print(f"     - Total: ${data['total_cost']}")
                print(f"     - Avg: ${data['avg_cost']}")
                print(f"     - Runs: {data['run_count']}")

        print(f"\n⏱️ Performance:")
        print(f"   • Total Time: {report['performance']['total_execution_time']}s")
        print(f"   • Avg Time/Run: {report['performance']['avg_execution_time']}s")
        print(f"   • Fastest Run: {report['performance']['fastest_run']}s")
        print(f"   • Slowest Run: {report['performance']['slowest_run']}s")

        if report['errors']:
            print(f"\n❌ Errors:")
            for error in report['errors']:
                print(f"   • {error['chain']}: {error['error'][:50]}...")

        # Save metrics
        demo.save_metrics()

        print("\n" + "=" * 60)
        print("Demo completed! Check LangSmith dashboard for detailed traces.")
        print("Visit: https://smith.langchain.com")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("\nPlease check:")
        print("1. Your API keys are correctly set in .env")
        print("2. You have an active internet connection")
        print("3. Your OpenAI account has available credits")


if __name__ == "__main__":
    main()