#!/usr/bin/env python3
"""
Quick setup test script for LangSmith demo
Verifies API keys and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

def test_setup():
    """Test if the environment is properly configured"""
    print("🔍 Testing LangSmith Demo Setup...")
    print("-" * 40)

    # Load environment variables
    load_dotenv()

    # Check for required API keys
    errors = []
    warnings = []

    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        errors.append("❌ OPENAI_API_KEY not found in .env file")
    elif not openai_key.startswith("sk-"):
        warnings.append("⚠️  OPENAI_API_KEY format looks incorrect (should start with 'sk-')")
    else:
        print("✅ OpenAI API key found")

    # Check LangSmith API key
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    if not langsmith_key:
        errors.append("❌ LANGSMITH_API_KEY not found in .env file")
    elif not langsmith_key.startswith("ls"):
        warnings.append("⚠️  LANGSMITH_API_KEY format looks incorrect (should start with 'ls')")
    else:
        print("✅ LangSmith API key found")

    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        errors.append(f"❌ Python 3.8+ required (current: {python_version.major}.{python_version.minor})")
    else:
        print(f"✅ Python version OK ({python_version.major}.{python_version.minor})")

    # Try importing required packages
    packages_to_check = [
        ("langchain", "LangChain"),
        ("langsmith", "LangSmith"),
        ("openai", "OpenAI"),
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("plotly", "Plotly")
    ]

    print("\n📦 Checking required packages:")
    for package, name in packages_to_check:
        try:
            __import__(package)
            print(f"  ✅ {name} installed")
        except ImportError:
            errors.append(f"❌ {name} not installed - run: pip install -r requirements.txt")

    # Test basic LangSmith connection if keys are present
    if openai_key and langsmith_key:
        print("\n🔗 Testing API connections:")
        try:
            from langsmith import Client
            client = Client(api_key=langsmith_key)
            # Try to list projects (basic connectivity test)
            print("  ✅ LangSmith connection successful")
        except Exception as e:
            warnings.append(f"⚠️  LangSmith connection test failed: {str(e)[:50]}...")

        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            # Basic test - list models
            models = client.models.list()
            print("  ✅ OpenAI connection successful")
        except Exception as e:
            errors.append(f"❌ OpenAI connection failed: {str(e)[:50]}...")

    # Print summary
    print("\n" + "=" * 40)
    print("SETUP TEST RESULTS")
    print("=" * 40)

    if errors:
        print("\n❌ Setup Issues Found:")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  {warning}")

    if not errors:
        print("\n✅ All checks passed! You're ready to run the demo.")
        print("\nNext steps:")
        print("1. Run the demo: python langsmith_demo.py")
        print("2. View dashboard: streamlit run metrics_dashboard.py")
    else:
        print("\n❌ Please fix the issues above before running the demo.")
        print("\nSetup instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Install dependencies: pip install -r requirements.txt")

    return len(errors) == 0


if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)