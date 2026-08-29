import sympy as sp
from sympy.abc import x

def conditions(witness):
    try:
        n = int(witness)
        h1 = (n > 0 and n == witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The minimal polynomial of zeta_n over Q is the n-th cyclotomic polynomial.
            p = sp.cyclotomic_poly(n, x)
            poly_p = sp.Poly(p, x)
            d = poly_p.degree()
            
            # The field trace of zeta_n in Q(zeta_n)/Q is the sum of its Galois conjugates,
            # which is the negative of the coefficient of x^(d-1) in its minimal polynomial.
            trace = -poly_p.nth(d - 1)
            mu = sp.mobius(n)
            
            # The conjecture claims trace == mu. We check if it fails.
            neg_q = bool(trace != mu)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "not Q: The field trace Tr_{Q(zeta_n)/Q}(zeta_n) is not equal to mu(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1