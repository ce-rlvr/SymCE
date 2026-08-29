import sympy
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            X = witness.get('X')
            S = witness.get('S')
        else:
            R, X, S = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    try:
        h1 = False
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif type(R).__name__ in ('IntegerRing', 'RationalField', 'RealField', 'ComplexField'):
            h1 = True
    except Exception:
        h1 = False

    # H2: X is an indeterminate over R
    try:
        h2 = isinstance(X, sympy.Symbol)
    except Exception:
        h2 = False

    # neg_Q: S^-1(R[X]) is NOT isomorphic to (S^-1 R)[X]
    try:
        if not isinstance(S, (list, tuple, set)):
            S_list = [S]
        else:
            S_list = S
            
        neg_q = False
        for s in S_list:
            try:
                p = sympy.Poly(s, X)
                if p.degree() > 0:
                    neg_q = True
                    break
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: X is an indeterminate over R",
    "¬Q: localized ring is not isomorphic to polynomial ring over localized ring"
]

N_HYP = 2
NEG_Q_INDEX = 2