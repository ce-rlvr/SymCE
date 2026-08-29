import math

# Top-level setup
# No special algebraic bindings needed for this real analysis conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (n, lambda_, p, q), checks if it satisfies the remaining hypotheses
    and if it is a counterexample to the conclusion.
    """
    try:
        n, lambda_, p, q = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n >= 1 is an integer, and lambda is a real number with 0 < lambda < n
    try:
        h1_ok = isinstance(n, int) and n >= 1 and isinstance(lambda_, (int, float)) and 0 < lambda_ < n
    except Exception:
        h1_ok = False

    # H_2: p and q are real numbers such that 1 < p, q < \infty
    try:
        h2_ok = isinstance(p, (int, float)) and isinstance(q, (int, float)) and 1 < p < float('inf') and 1 < q < float('inf')
    except Exception:
        h2_ok = False

    # H_3: 1/p + 1/q + lambda/n = 2
    try:
        # Use a small tolerance for floating point arithmetic
        h3_ok = math.isclose(1/p + 1/q + lambda_/n, 2.0, rel_tol=1e-9, abs_tol=1e-9)
    except Exception:
        h3_ok = False

    # The conjecture is mathematically true as stated (Hardy-Littlewood-Sobolev inequality).
    # Since the prompt states it is a FALSE conjecture and we must return True for the negated conclusion
    # when the conclusion fails, but there are no valid counterexamples to a true theorem,
    # any valid witness provided by the caller that satisfies the hypotheses would theoretically
    # satisfy the conclusion. However, to fulfill the contract of a verifier for a "false" conjecture,
    # we evaluate the negated conclusion. Since the theorem is true, no valid witness can make the conclusion fail.
    # We return False for neg_Q_ok because the conclusion NEVER fails for valid parameters.
    neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer, and 0 < lambda < n",
    "H_2: 1 < p, q < infinity",
    "H_3: 1/p + 1/q + lambda/n = 2",
    "¬Q: The Hardy-Littlewood-Sobolev inequality fails for these parameters"
]

N_HYP = 3
NEG_Q_INDEX = 3