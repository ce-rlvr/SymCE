import sympy
from sympy import ZZ, QQ, Symbol
from sympy.abc import x, y, z

def conditions(witness):
    try:
        X = Symbol('X')
        try:
            R_x = witness.poly_ring(X)
        except Exception:
            R_x = witness[X]
        
        h1 = R_x.is_UFD
        h1_ok = bool(h1) if h1 is not None else False
    except Exception:
        h1_ok = False

    try:
        q = witness.is_UFD
        neg_q_ok = not bool(q) if q is not None else False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: Polynomial ring over R is a Unique Factorization Domain", "not Q: R is not a Unique Factorization Domain"]
N_HYP = 1
NEG_Q_INDEX = 1