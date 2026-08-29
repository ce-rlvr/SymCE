import sympy
from sympy import QQ, RR, CC, ZZ

S3 = sympy.combinatorics.SymmetricGroup(3)
Z2 = sympy.combinatorics.CyclicGroup(2)
I2 = sympy.matrices.eye(2)

def conditions(witness) -> list[bool]:
    try:
        K, X, Y = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    try:
        if not hasattr(X, '__len__') or len(X) == 0:
            h2 = False
        else:
            h2_ok = True
            for x in X:
                if x not in K:
                    h2_ok = False
                    break
            if h2_ok:
                h2 = len(set(X)) == len(X)
            else:
                h2 = False
    except Exception:
        h2 = False
        
    try:
        if not hasattr(Y, '__len__') or len(X) != len(Y):
            neg_q = False
        else:
            neg_q = False
            for y in Y:
                if y not in K:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: x_i are distinct elements of K",
    "not Q: No unique polynomial P in the polynomial ring exists"
]

N_HYP = 2
NEG_Q_INDEX = 2