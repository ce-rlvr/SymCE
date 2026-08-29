import sympy
from sympy import symbols
from sympy.abc import x, y, z

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('h1', False))
            h2 = bool(witness.get('h2', False))
            h3 = bool(witness.get('h3', False))
            neg_q = bool(witness.get('neg_q', False))
            return [h1, h2, h3, neg_q]
        else:
            h1 = bool(getattr(witness, 'h1', False))
            h2 = bool(getattr(witness, 'h2', False))
            h3 = bool(getattr(witness, 'h3', False))
            neg_q = bool(getattr(witness, 'neg_q', False))
            return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: alpha in L is algebraic over K(S)",
    "H_3: m(x) in the polynomial ring over K(S) is the minimal polynomial",
    "neg_Q: no finite subset S_0 of S contains all coefficients"
]

N_HYP = 3
NEG_Q_INDEX = 3