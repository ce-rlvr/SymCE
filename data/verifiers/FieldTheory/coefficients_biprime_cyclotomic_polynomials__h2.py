import sympy
from sympy import Symbol, Poly, cyclotomic_poly
from sympy.ntheory import isprime

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
        else:
            p, q = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1 = False

    try:
        x = Symbol('x')
        poly_expr = cyclotomic_poly(p * q, x)
        coeffs = Poly(poly_expr, x).all_coeffs()
        q_holds = all(int(c) in [-1, 0, 1] for c in coeffs)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "¬Q: Not every coefficient of Phi_{pq}(x) is in {-1, 0, 1}"
]

N_HYP = 1
NEG_Q_INDEX = 1