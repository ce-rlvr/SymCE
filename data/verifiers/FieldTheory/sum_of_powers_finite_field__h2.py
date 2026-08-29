import sympy
from sympy.ntheory import factorint

def conditions(witness) -> list[bool]:
    """
    witness: a tuple (q, k) where q is the size of the finite field and k is the power
    """
    try:
        q, k = witness
    except Exception:
        return [False, False]

    # H_1: F_q is a finite field with q elements
    try:
        h1_ok = isinstance(q, int) and q >= 2 and len(factorint(q)) == 1
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion FAILS at the witness
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # The sum \sum_{x \in F_q} x^k
            # If k < 0, 0^k is undefined (division by zero in the field),
            # so the sum cannot evaluate to 0 as the conclusion claims for the "otherwise" case.
            # If k >= 0, the sum evaluates to -1 if k > 0 and (q-1)|k, and 0 otherwise,
            # which perfectly matches the conclusion.
            if k < 0:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: The sum does not evaluate to -1 if k > 0 and q-1 divides k, or does not evaluate to 0 otherwise"
]

N_HYP = 1
NEG_Q_INDEX = 1