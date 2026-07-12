import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    for i in range(20):
        if args.verbose:
            print(f"Loop #{i+1}")

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions
        )

        if not response.usage:
            raise RuntimeError("The API request flopped")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                function_result = call_function(tool_call, verbose=args.verbose)
                result_message = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_result["content"]
                }
                messages.append(result_message)

                if not function_result["content"]:
                    raise Exception("The returned tool message had an empty content")
                if args.verbose:
                    print(f"-> {function_result['content']}")
        else:
            print(message.content)
            return 0
    print("Exiting: Maximum agent iterations reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
