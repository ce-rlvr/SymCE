import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
    except Exception:
        return [False, False, False]

    # H_1: n is a composite integer
    try:
        h1 = (n > 1) and not sympy.isprime(n)
    except Exception:
        h1 = False

    # H_2: n is not of the form p^k for any prime p and integer k >= 1
    try:
        if n > 1:
            factors = sympy.factorint(n)
            h2 = len(factors) > 1
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The field norm N_{Q(zeta_n)/Q}(1-zeta_n) is not equal to 1
    try:
        if n >= 1:
            poly = sympy.cyclotomic_poly(n, x)
            norm = poly.subs(x, 1)
            neg_q = bool(norm != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a composite integer",
    "H_2: n is not of the form p^k for any prime p and integer k >= 1",
    "¬Q: The field norm N_{Q(zeta_n)/Q}(1-zeta_n) is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2