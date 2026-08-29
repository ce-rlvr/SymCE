import sympy

def conditions(witness):
    try:
        if isinstance(witness, bool):
            return [False, False]
        n = int(witness)
        if n != witness:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = (n > 0)
    except Exception:
        h1 = False

    try:
        # The conclusion states that Gal(Q(ζ_n)/Q) is isomorphic to (Z/nZ)^x.
        # This is a universally true mathematical theorem for all positive integers n.
        # Thus, the conclusion always holds, and its negation is always False.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Gal(ℚ(ζ_n)/ℚ) is not isomorphic to (ℤ/nℤ)^×"
]

N_HYP = 1
NEG_Q_INDEX = 1