import sympy
from sympy.ntheory import mobius

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be the integer p.
    """
    try:
        if isinstance(witness, tuple):
            p = int(witness[0])
        else:
            p = int(witness)
        # The hypothesis "x is a formal indeterminate" is a structural property.
        # We just ensure p is a valid positive integer for the Bell series.
        h1 = (p >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The conclusion is sum_{k=0}^infty mu(p^k) x^k == 1 - x
            # We check the first few coefficients of the series.
            # For the series to be exactly 1 - x, we need:
            # k=0: mu(p^0) == 1 (always true for p >= 1)
            # k=1: mu(p^1) == -1
            # k=2: mu(p^2) == 0
            # k=3: mu(p^3) == 0
            c1 = mobius(p)
            c2 = mobius(p**2)
            c3 = mobius(p**3)
            
            conclusion_holds = (c1 == -1) and (c2 == 0) and (c3 == 0)
            
            # neg_q is True when the conclusion FAILS
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a formal indeterminate",
    "¬Q: sum_{k=0}^infty mu(p^k) x^k != 1 - x"
]

N_HYP = 1
NEG_Q_INDEX = 1