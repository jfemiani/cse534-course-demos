"""The smallest useful OpenAI Responses API program."""

import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

response = client.responses.create(model=model, input="Say hello to CSE 534.")
print(response.output_text)
