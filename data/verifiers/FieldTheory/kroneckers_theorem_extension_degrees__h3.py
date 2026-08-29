import sympy
from sympy import Poly, QQ, ZZ, RR, CC
from sympy.polys.domains import GF
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get("K")
            f = witness.get("f")
            n = witness.get("n")
        else:
            K, f, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = hasattr(K, "is_Field") and K.is_Field
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x, domain=K)
        h2 = not poly_f.is_zero and poly_f.degree() >= 1
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f, x, domain=K)
        factors = poly_f.factor_list()
        neg_q = True
        for fac, mult in factors[1]:
            if fac.degree() <= n:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a non-constant polynomial",
    "not Q: Every finite field extension L of K where f has a root has degree greater than n"
]

N_HYP = 2
NEG_Q_INDEX = 2