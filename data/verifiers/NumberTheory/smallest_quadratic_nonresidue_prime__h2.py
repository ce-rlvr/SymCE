import sympy

# Top-level setup
# No named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            n = witness['n']
        elif hasattr(witness, 'p') and hasattr(witness, 'n'):
            p = witness.p
            n = witness.n
        else:
            p, n = witness
    except Exception:
        return [False, False]

    # H_1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # ¬Q: n is not a prime number
    try:
        neg_q = not bool(sympy.isprime(n))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: n is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1