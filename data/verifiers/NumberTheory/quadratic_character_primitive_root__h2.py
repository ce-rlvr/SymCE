import sympy
from sympy.ntheory import isprime, legendre_symbol

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            g = witness['g']
            p = witness['p']
        else:
            g, p = witness
        g = int(g)
        p = int(p)
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1_ok = False

    try:
        # The conclusion is that (g/p) == -1.
        # The negated conclusion is that (g/p) != -1.
        neg_q_ok = bool(legendre_symbol(g, p) != -1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: The Legendre symbol (g/p) is not equal to -1"
]

N_HYP = 1
NEG_Q_INDEX = 1