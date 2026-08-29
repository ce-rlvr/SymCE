import sympy
from sympy.ntheory import legendre_symbol

# Top-level setup
# No named bindings needed for Number Theory; use integers directly.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            k = witness.get('k')
            p = witness.get('p')
        else:
            a, k, p = witness
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: k is a positive integer
    try:
        h2 = bool(int(k) == k and k > 0)
    except Exception:
        h2 = False

    # ¬Q: (a^k/p) != (a/p)^k
    try:
        left = legendre_symbol(a**k, p)
        right = legendre_symbol(a, p)**k
        q = bool(left == right)
    except Exception:
        # If legendre_symbol is undefined (e.g., a is not an integer),
        # the conclusion fails, so ¬Q is True.
        q = False

    neg_q = not q

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: p is an odd prime",
    "H_2: k is a positive integer",
    "¬Q: (a^k/p) != (a/p)^k"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2