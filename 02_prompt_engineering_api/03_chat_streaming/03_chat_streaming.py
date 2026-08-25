"""The previous chat, now printing text as it arrives."""

import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")
previous_id = None

while True:
    user_text = input("You: ").strip()
    if user_text.lower() in {"quit", "exit"}:
        break

    events = client.responses.create(
        model=model,
        input=user_text,
        previous_response_id=previous_id,
        stream=True,
    )
    print("Assistant: ", end="", flush=True)
    for event in events:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
            previous_id = event.response.id
    print()
