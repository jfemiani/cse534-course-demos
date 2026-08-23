"""Demo: giving the model a tool it cannot fake.

Concept: tool use, also called function calling. The model does not run
code. It emits a structured request naming a function and arguments; our
code runs the real function and sends the result back as a
function_call_output item. This demo asks a question language models are
famous for getting wrong on their own (counting letters in a word), so the
tool's answer is visibly better than a guess would be.

Endpoint: OpenAI Responses API (client.responses.create), tools=[...] with
tool_choice="required" so the demo reliably calls the tool.

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API function-calling format. Keep the
single tool, the single round trip, and the letter-counting question."
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
