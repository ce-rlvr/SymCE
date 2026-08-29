import sympy
import sympy.polys.domains

RR = sympy.RR
CC = sympy.CC
QQ = sympy.QQ
ZZ = sympy.ZZ
Reals = sympy.S.Reals
Complexes = sympy.S.Complexes

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            K, L = witness
        else:
            K = witness
            L = None
    except Exception:
        K = witness
        L = None

    try:
        h1 = bool(K in (sympy.RR, sympy.S.Reals) or type(K).__name__ == 'RealField')
    except Exception:
        h1 = False

    try:
        if (K in (sympy.RR, sympy.S.Reals) or type(K).__name__ == 'RealField') and \
           (L in (sympy.CC, sympy.S.Complexes) or type(L).__name__ == 'ComplexField'):
            q = True
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a real closed field",
    "¬Q: The extension degree of L over K is not 2, or L is not K(sqrt(-1))"
]

N_HYP = 1
NEG_Q_INDEX = 1