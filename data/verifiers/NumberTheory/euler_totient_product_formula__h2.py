import sympy
from sympy.ntheory import totient, primefactors
from sympy import Rational

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    # H_1: n is an integer
    try:
        if isinstance(witness, int):
            h1 = True
        elif hasattr(witness, 'is_integer') and witness.is_integer:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: phi(n) != n * prod_{p|n} (1 - 1/p)
    try:
        n = int(witness)
        lhs = totient(n)
        rhs = n
        for p in primefactors(n):
            rhs *= Rational(p - 1, p)
        q_holds = (lhs == rhs)
        neg_q = not q_holds
    except Exception:
        # If primefactors(n) raises an error (e.g., for n=0), the formula is undefined,
        # hence the conclusion fails.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: phi(n) != n * prod_{p|n} (1 - 1/p)"
]

N_HYP = 1
NEG_Q_INDEX = 1