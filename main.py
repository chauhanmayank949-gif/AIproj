import sys
from functions.call_function import call_function
import json
import os 
from dotenv import load_dotenv 
from openai import OpenAI 
from prompts import system_prompts
import argparse
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions  = [
      schema_get_files_info,
      schema_get_file_content,
      schema_run_python_file,
      schema_write_file,
]
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key :
   raise RuntimeError("OPENROUTER_API_KEY environment variable not found")

client = OpenAI(
     base_url = "https://openrouter.ai/api/v1",
     api_key = api_key,
)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

messages = [
     system_prompts,
     {"role": "user", "content": str(args.user_prompt)},
]
tools=[get_files_info, get_file_content]
max_iterations =20

for _ in range(max_iterations):
     response = client.chat.completions.create(
        model = "openrouter/free",
        messages=messages,
        tools=available_functions,
     )
     if not response or not getattr(response, "choices", None):
            print(f"API Error or empty choices: {response}")
            break
     message = response.choices[0].message

     messages.append(message)

     if not message.tool_calls:
         print(f"Final response:\n{message.content}")
         sys.exit(0)
     for tool_call in message.tool_calls:
         print(f"- Calling function: {tool_call.function.name}")
         result = call_function(tool_call, verbose=args.verbose)

         if isinstance(result, dict) and result.get("role") == "tool":
             messages.append(result)
         else:
             messages.append({
               "role": "tool",
               "tool_call_id": tool_call.id,
               "content": str(result),
              })
print("Error: Reaches maximum iterations without a final response.", file=sys.stderr)
sys.exit(1)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools =available_functions,
)
message = response.choices[0].message


usage = response.usage 
if usage is None:
   raise RuntimeError("Response usage information is unavailable")
prompt_tokens = usage.prompt_tokens
response_tokens= usage.completion_tokens
if args.verbose:
    print(f"User prompt:{args.user_prompt}")
    print(f"Prompt tokens:{prompt_tokens}")
    print(f"Response tokens:{response_tokens}")
message = response.choices[0].message
message.append(message)
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"Calling tool: {tool_call.function.name}")
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message.get("content"):
            raise Exception("Tool message content is empty")
        message.append(result_message)
        if args.verbose:
            print(f"-> {result_message['content']}")
elif message.content:
    print(f"Final response:\n{message.content}")
    sys.exit(0)
