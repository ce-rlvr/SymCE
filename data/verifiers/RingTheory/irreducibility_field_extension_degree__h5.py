import sympy
from sympy import Poly, minpoly, QQ, GF, Rational, Integer
from sympy.abc import x
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            alpha = witness.get('alpha')
            f = witness.get('f')
            n = witness.get('n')
        elif len(witness) == 4:
            K, alpha, f, n = witness
        elif len(witness) == 5:
            K, alpha, f, n, _ = witness
        else:
            return [False] * 6
    except Exception:
        return [False] * 6

    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False

    try:
        mp = minpoly(alpha, x, domain=K)
        h2 = True
    except Exception:
        h2 = False

    try:
        h3 = h2
    except Exception:
        h3 = False

    try:
        p = Poly(f, x, domain=K)
        h4 = bool(p.is_monic and p.degree() == n)
    except Exception:
        h4 = False

    try:
        mp = minpoly(alpha, x, domain=K)
        h5 = bool(Poly(mp, x).degree() == n)
    except Exception:
        h5 = False

    try:
        p = Poly(f, x, domain=K)
        neg_q = (p.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is an extension field of K",
    "H_3: alpha is an element of L",
    "H_4: f(x) is a monic polynomial of degree n over K",
    "H_5: The degree of the field extension K(alpha) over K is exactly n",
    "¬Q: f(x) is reducible over K"
]

N_HYP = 5
NEG_Q_INDEX = 5