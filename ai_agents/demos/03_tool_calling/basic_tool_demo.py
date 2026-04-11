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

print("🛠️ Basic Tool Calling Demo")
print("=" * 50)

# Step 1: Define the Tool Function
def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers and returns an integer
    
    Args:
        a: first integer
        b: second integer
    """
    return a * b

print("1. Tool Function Created:")
print(f"   Function: multiply(a: int, b: int) -> int")
print(f"   Docstring: {multiply.__doc__.strip()}")
print()

# Step 2: Bind Tools to Model
model_with_tools = model.bind_tools([multiply])
print("2. Model with Tools Created:")
print("   Model now knows about the multiply function")
print()

# Step 3: Test Tool Calling
print("3. Testing Tool Calling:")
print("   Question: What is 4 times 6?")
print()

result = model_with_tools.invoke([HumanMessage(content="What is 4 times 6?")])

print("AI Response:", result.content)
print("Tool Calls:", result.tool_calls)
print()

# Step 4: Inspect Tool Call Details
if result.tool_calls:
    tool_call = result.tool_calls[0]
    print("4. Tool Call Details:")
    print(f"   Function name: {tool_call['name']}")
    print(f"   Arguments: {tool_call['args']}")
    print(f"   Call ID: {tool_call['id']}")
    print()
    
    # Step 5: Execute the Tool
    print("5. Executing the Tool:")
    args = tool_call['args']
    result_value = multiply(args['a'], args['b'])
    print(f"   multiply({args['a']}, {args['b']}) = {result_value}")
else:
    print("4. No tool calls made")