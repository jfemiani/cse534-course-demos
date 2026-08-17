# Demo 04: Joint and Conditional Probability

Demonstrates autoregressive word generation using joint and conditional probabilities.

At each step, computes:
- **P(context)** - marginal probability of current prefix
- **P(next | context)** - conditional probability of each possible next letter
- **P(context, next)** - joint probability after adding the sampled letter

Shows the relationship: **P(next | context) = P(context, next) / P(context)**

Generates a 5-letter word step-by-step:
1. Start with empty context
2. For each position: show all P(next | context), sample next letter
3. Update context and repeat

**Connection to GenAI**: This is exactly how LLMs generate text token-by-token using autoregressive generation. Each token is sampled from P(next | all previous tokens).

