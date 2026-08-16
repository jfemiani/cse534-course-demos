"""A non-streaming, multi-turn terminal chat."""

import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")
previous_id = None

while True:
    user_text = input("You: ").strip()
    if user_text.lower() in {"quit", "exit"}:
        break

    response = client.responses.create(
        model=model,
        input=user_text,
        previous_response_id=previous_id,
    )
    print(f"Assistant: {response.output_text}")
    previous_id = response.id
