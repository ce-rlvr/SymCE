import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        p = Poly(witness, x)
        h1_ok = bool(p.domain == sympy.ZZ)
    except Exception:
        h1_ok = False

    try:
        p = Poly(witness, x, domain='ZZ')
        cont, factors = p.factor_list()
        if p.degree() == 0:
            h2_ok = bool(sympy.isprime(abs(cont)))
        else:
            h2_ok = bool(abs(cont) == 1 and len(factors) == 1 and factors[0][1] == 1)
    except Exception:
        h2_ok = False

    try:
        p = Poly(witness, x, domain='ZZ')
        neg_q_ok = bool(abs(p.content()) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is an irreducible polynomial",
    "not Q: f is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2