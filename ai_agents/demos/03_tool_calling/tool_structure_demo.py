import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    max_tokens=512,
    temperature=0.1,
)

print("📊 Understanding Tool Call Structure")
print("=" * 50)

# Define multiple tools
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# Bind all tools to model
tools = [add, subtract, multiply]
model_with_tools = model.bind_tools(tools)

print("Available Tools:")
for i, tool in enumerate(tools, 1):
    print(f"  {i}. {tool.__name__}: {tool.__doc__}")
print()

# Test with different questions
test_questions = [
    "What is 10 plus 5?",
    "Calculate 20 minus 8",
    "What is 6 times 7?"
]

for i, question in enumerate(test_questions, 1):
    print(f"--- Test {i} ---")
    print(f"Question: {question}")
    
    result = model_with_tools.invoke([HumanMessage(content=question)])
    
    print(f"AI Response: {result.content}")
    
    if result.tool_calls:
        for j, tool_call in enumerate(result.tool_calls, 1):
            print(f"Tool Call {j}:")
            print(f"  Name: {tool_call['name']}")
            print(f"  Arguments: {tool_call['args']}")
            print(f"  ID: {tool_call['id']}")
            
            # Execute the tool
            func_name = tool_call['name']
            args = tool_call['args']
            
            if func_name == 'add':
                result_value = add(args['a'], args['b'])
            elif func_name == 'subtract':
                result_value = subtract(args['a'], args['b'])
            elif func_name == 'multiply':
                result_value = multiply(args['a'], args['b'])
            
            print(f"  Result: {result_value}")
    else:
        print("No tool calls made")
    
    print()