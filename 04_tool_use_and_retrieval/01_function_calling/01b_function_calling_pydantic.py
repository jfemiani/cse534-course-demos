# pip install openai pydantic

"""Demo 1b: tool use with a Pydantic-generated argument schema.

See 01b_function_calling_pydantic.md for the full explanation.
"""

import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")


class CountLetterArgs(BaseModel):
    word: str
    letter: str


def count_letter(word: str, letter: str) -> int:
    """The real function behind the tool. The model never runs this itself."""
    return word.lower().count(letter.lower())


tools = [
    {
        "type": "function",
        "name": "count_letter",
        "description": "Count how many times a letter appears in a word.",
        "parameters": CountLetterArgs.model_json_schema(),
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
args = CountLetterArgs.model_validate_json(call.arguments)
print(f"Model asked to call: {call.name}({args})")

result = count_letter(args.word, args.letter)
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
