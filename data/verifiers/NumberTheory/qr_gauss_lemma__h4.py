import math
from sympy import isprime
from sympy.ntheory import jacobi_symbol

# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, p, n) or a dictionary with keys 'a', 'p', 'n',
    checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
            n = witness['n']
        else:
            a, p, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is an odd prime number
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = isinstance(a, int) or (hasattr(a, 'is_integer') and a.is_integer)
        h2 = bool(h2)
    except Exception:
        h2 = False

    # H_3: a and p are coprime
    try:
        h3 = bool(math.gcd(int(a), int(p)) == 1)
    except Exception:
        h3 = False

    # ¬Q: The Legendre symbol (a/p) is not equal to (-1)^n
    try:
        # For an odd prime p, the Jacobi symbol is equivalent to the Legendre symbol
        ls = jacobi_symbol(int(a), int(p))
        rhs = (-1)**n
        neg_q = bool(ls != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: a is an integer",
    "H_3: a and p are coprime",
    "¬Q: The Legendre symbol (a/p) is not equal to (-1)^n"
]

N_HYP = 3
NEG_Q_INDEX = 3