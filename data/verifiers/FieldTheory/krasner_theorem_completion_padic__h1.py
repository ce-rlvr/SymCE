import sympy
from sympy import isprime

# Top-level setup
# The witness is expected to be an integer p representing the base of the p-adic numbers.
# No complex algebraic structures need to be pre-defined for this specific conjecture.

def conditions(witness):
    """
    Checks whether the given witness (an integer p) satisfies the remaining hypotheses
    and fails the conclusion of the conjecture.
    """
    try:
        p = int(witness)
        # Ensure the witness is exactly an integer
        if p != witness:
            h1 = False
        else:
            # p-adic numbers \mathbb{Q}_p are defined for integers p >= 2
            h1 = (p >= 2)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p != witness:
            h2 = False
        else:
            # The metric completion can be formed for any valid base p >= 2
            h2 = (p >= 2)
    except Exception:
        h2 = False

    try:
        p = int(witness)
        if p != witness:
            neg_q = False
        else:
            # The conclusion states that \mathbb{C}_p is an algebraically closed field.
            # This is TRUE if and only if p is a prime number.
            # If p is composite (e.g., p = 4 or p = 10), \mathbb{Q}_p is a ring with zero divisors,
            # not a field, and consequently \mathbb{C}_p is not a field.
            # We want the conclusion to FAIL, so neg_q should be True when p is NOT prime.
            neg_q = not isprime(p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\overline{\\mathbb{Q}_p} is the algebraic closure of the p-adic numbers \\mathbb{Q}_p with the extended p-adic absolute value",
    "H_2: \\mathbb{C}_p is the metric completion of \\overline{\\mathbb{Q}_p}",
    "¬Q: \\mathbb{C}_p is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2