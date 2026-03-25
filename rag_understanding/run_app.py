#!/usr/bin/env python3
"""
Simple script to run the RAG Understanding Interactive Tutorial
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please run: pip install -r requirements.txt")
        sys.exit(1)

def run_streamlit():
    """Run the Streamlit app"""
    print("🚀 Starting RAG Understanding Interactive Tutorial...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using the RAG Understanding Tutorial!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 RAG Understanding Interactive Tutorial")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ Error: streamlit_app.py not found")
        print("Please make sure you're in the correct directory")
        sys.exit(1)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main()
