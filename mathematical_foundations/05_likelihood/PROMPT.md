# Demo 05: Likelihood and Log-Likelihood

Demonstrates why machine learning uses log-likelihood for optimization.

**Part A: Numerical Stability (05a_likelihood_underflow.py)**
- Computes likelihood L(μ) as product of probabilities
- Computes log-likelihood ℓ(μ) as sum of log probabilities
- Shows likelihood underflows to 0, log-likelihood stays computable

**Part B: Gradient Ascent Failure (05b_likelihood_gradient_fail.py)**
- Attempts gradient ascent on raw likelihood L(μ)
- Shows gradients vanish due to underflow
- Parameter doesn't move from initial value

**Part C: Direct μ Optimization (05c_likelihood_logit.py)**
- Gradient ascent on log-likelihood by optimizing μ directly
- Succeeds but requires manual clamping to keep μ ∈ (0,1)
- Shows that log-likelihood enables gradient-based optimization

**Connection to GenAI**: Neural networks minimize negative log-likelihood (cross-entropy loss) over billions of parameters. Log-likelihood is essential for both numerical stability and gradient-based optimization.
