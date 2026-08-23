---
name: regenerate_demo
description: Use when a course demo script fails because the OpenAI Responses API or SDK changed. Checks current official docs and updates the script while preserving its original teaching scenario.
---

# Regenerate a Course Demo

1. Read the failing script's top docstring. It names the concept being taught and the exact scenario (which tools, which documents, which question) that has to stay the same.
2. Check the current official OpenAI API documentation for the endpoint the script uses.
3. Update only what changed: parameter names, response shapes, method names.
4. Keep the same demo scenario so the script still illustrates the same concept.
5. Run the script and confirm the output still makes the same teaching point.
