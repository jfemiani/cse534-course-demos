"""04d: pointing at a folder of documents with OpenAI's hosted file_search tool.

See 04d_hosted_file_search.md for the full explanation.
"""

import io
import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

SAMPLE_DOCUMENTS = {
    "syllabus.txt": "CSE 534 meets Tuesdays and Thursdays. Attendance is not graded.",
    "lab_policy.txt": (
        "Late Lab 3 submissions lose 10 percent of the grade for each day past "
        "the 11:59pm deadline, with no credit given after three days."
    ),
    "office_hours.txt": "Office hours are Tuesdays 2-4pm in Laws Hall 205, no appointment needed.",
}
QUESTION = "How many points do I lose per day if Lab 3 is late?"

vector_store = client.vector_stores.create(name="cse534-demo-docs")

file_ids = []
for filename, text in SAMPLE_DOCUMENTS.items():
    vector_store_file = client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=(filename, io.BytesIO(text.encode())),
    )
    file_ids.append(vector_store_file.id)

response = client.responses.create(
    model=model,
    input=QUESTION,
    tools=[{"type": "file_search", "vector_store_ids": [vector_store.id]}],
    include=["file_search_call.results"],
)

for item in response.output:
    if item.type == "file_search_call":
        print(f"Searched for: {item.queries}")
        for result in item.results or []:
            print(f"  matched {result.filename} (score={result.score:.3f})")

print(f"\nQuestion: {QUESTION}")
print(f"Assistant: {response.output_text}")

for file_id in file_ids:
    client.files.delete(file_id)
client.vector_stores.delete(vector_store.id)
