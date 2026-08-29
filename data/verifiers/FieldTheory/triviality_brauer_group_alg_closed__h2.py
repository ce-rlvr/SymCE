import sympy
from sympy import S
from sympy.polys.domains import CC, QQ, RR, ZZ

Complexes = S.Complexes
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers

def is_alg_closed_field(x):
    return x in (S.Complexes, CC) or str(x) in (
        'CC', 'Complexes', 'ComplexField', 'C', 'AlgebraicNumbers', 'QQbar'
    )

def is_isomorphic(x, y):
    if x in (S.Complexes, CC) and y in (S.Complexes, CC):
        return True
    if x == y:
        return True
    if str(x) == str(y):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            D = witness.get('D')
        else:
            K, D = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(is_alg_closed_field(K))
    except Exception:
        h1 = False

    try:
        neg_q = not is_isomorphic(D, K)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: D is not isomorphic to K or Br(K) is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1