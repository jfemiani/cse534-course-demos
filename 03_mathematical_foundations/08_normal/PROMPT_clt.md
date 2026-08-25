# Central Limit Theorem Demonstration

## Purpose
Demonstrates that sample means are approximately normally distributed and that variance scales as 1/n.

## What it does
1. Samples from uniform distribution repeatedly and computes sample means
2. Shows the distribution of these means is approximately normal (CLT)
3. Plots variance of sample means vs sample size n (shows 1/n relationship)
4. Plots inverse variance vs n (shows linear relationship)

## Key insights
- The CLT says sample means are approximately normal, not that data are normal
- Variance of sample mean is σ²/n where σ² is the population variance
- The √n factor in CLT standardization comes from this variance shrinkage
- Same principle as 1/√d scaling in transformer attention

## Connection to course
- Connects to CLT discussion in lesson 6
- Foreshadows the variance normalization used in transformers
- Shows empirical validation of theoretical predictions

## Run
```bash
conda run -n cse434 python3 08_normal_clt_demo.py
```

## Output
- Console: Empirical vs theoretical variance at different sample sizes
- Figure: Three plots showing mean distribution, variance vs n, and inverse variance vs n
