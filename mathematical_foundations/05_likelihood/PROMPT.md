# Demo 05: Likelihood and Log-Likelihood

Demonstrates why machine learning uses negative log-likelihood (NLL) as the loss function.

**Part 1: Numerical Stability**
- Computes likelihood L(μ) as product of probabilities
- Computes log-likelihood ℓ(μ) as sum of log probabilities
- Shows likelihood underflows to 0, log-likelihood stays computable
- Both find the same maximum

**Part 2: Gradient Descent**
- Minimizes negative log-likelihood using PyTorch
- Shows NLL gradients enable parameter optimization
- Recovers μ_ML = (1/n)Σx_i from data

**Connection to GenAI**: Neural networks minimize negative log-likelihood (cross-entropy loss) over billions of parameters. Log-likelihood is essential for both numerical stability and gradient-based optimization.
