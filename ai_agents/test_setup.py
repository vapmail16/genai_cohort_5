import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Please make sure your .env file contains: OPENAI_API_KEY=your_actual_api_key_here")
    exit(1)

# Initialize model
model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

# Test connection
print("Testing OpenAI connection...")
msg = HumanMessage(content="Hi, how are you?")
response = model.invoke([msg])
print("Response:", response.content)
print("✅ Setup successful!")