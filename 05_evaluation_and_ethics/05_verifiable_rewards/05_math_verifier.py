"""Demo: a program-based verifier for a math answer, instead of a metric
formula (BLEU) or a second model (LLM-as-judge).

See 05_math_verifier.md for the full explanation.
Same style of candidates as 03_bleu_score.py: one problem, several
candidate "model solutions" chosen to expose one specific behavior each.
"""

import re

PROBLEM = "Twelve friends split a $180 dinner bill equally, then each pays an extra $5 tip. How much does each person pay in total?"
GROUND_TRUTH = 20.0

CANDIDATES = {
    "correct, well-formatted": (
        "180 / 12 = 15 dollars per person for the bill.\n"
        "15 + 5 = 20 dollars per person including the tip.\n"
        "#### 20"
    ),
    "correct, no format marker": (
        "The bill is 180 / 12 = 15 dollars each. Adding the $5 tip, "
        "the answer is 20 dollars."
    ),
    "wrong arithmetic, well-formatted": (
        "180 / 12 = 18 dollars per person for the bill.\n"
        "18 + 5 = 23 dollars per person including the tip.\n"
        "#### 23"
    ),
    "correct, different formatting": (
        "Splitting $180 twelve ways gives $15.00 per person. "
        "Add the $5.00 tip.\n"
        "#### $20.00"
    ),
}


def extract_answer(solution: str) -> float | None:
    """Pull the last number in the solution, preferring one after '####'."""
    marked = re.search(r"####\s*\$?(-?\d+(?:\.\d+)?)", solution)
    if marked:
        return float(marked.group(1))
    numbers = re.findall(r"-?\d+(?:\.\d+)?", solution)
    return float(numbers[-1]) if numbers else None


def has_format_marker(solution: str) -> bool:
    return "####" in solution


print(f"problem: {PROBLEM}\nground truth: {GROUND_TRUTH}\n")
print(f"{'candidate':30s} {'format ok':>10s} {'extracted':>10s} {'accuracy reward':>16s}")
for label, solution in CANDIDATES.items():
    format_ok = has_format_marker(solution)
    extracted = extract_answer(solution)
    correct = extracted is not None and extracted == GROUND_TRUTH
    print(f"{label:30s} {str(format_ok):>10s} {str(extracted):>10s} {str(correct):>16s}")
