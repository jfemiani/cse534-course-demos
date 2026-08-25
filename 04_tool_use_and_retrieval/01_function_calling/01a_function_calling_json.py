# pip install openai

"""Demo 1a: tool use with a hand-typed JSON schema.

See 01a_function_calling_json.md for the full explanation.
"""

import json
import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")


def count_letter(word: str, letter: str) -> int:
    """The real function behind the tool. The model never runs this itself."""
    return word.lower().count(letter.lower())


tools = [
    {
        "type": "function",
        "name": "count_letter",
        "description": "Count how many times a letter appears in a word.",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {"type": "string"},
                "letter": {"type": "string"},
            },
            "required": ["word", "letter"],
        },
    }
]

question = "How many times does the letter 'r' appear in 'strawberry'?"
response = client.responses.create(
    model=model,
    input=question,
    tools=tools,
    tool_choice="required",
)

call = response.output[0]
args = json.loads(call.arguments)
print(f"Model asked to call: {call.name}({args})")

result = count_letter(**args)
print(f"Real function returned: {result}")

follow_up = client.responses.create(
    model=model,
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": str(result),
        }
    ],
)
print(f"Assistant: {follow_up.output_text}")
