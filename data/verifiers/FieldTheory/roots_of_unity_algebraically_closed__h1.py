import math
from sympy import Symbol, Poly, Integer, QQ, RR, CC, ZZ, GF

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, n, p = witness
            elif len(witness) == 2:
                K, n = witness
                p = getattr(K, 'char', 0)
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            K = witness.get('K')
            n = witness.get('n')
            p = witness.get('p', getattr(K, 'char', 0))
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: If p > 0, then n is coprime to p
    try:
        if p > 0:
            h2 = math.gcd(int(n), int(p)) == 1
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The polynomial x^n - 1 does not have exactly n distinct roots in K
    try:
        poly = Poly(x**n - 1, x, domain=K)
        rts = poly.ground_roots()
        neg_q = len(rts) != n
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: If p > 0, then n is coprime to p",
    "¬Q: The polynomial x^n - 1 does not have exactly n distinct roots in K"
]

N_HYP = 2
NEG_Q_INDEX = 2