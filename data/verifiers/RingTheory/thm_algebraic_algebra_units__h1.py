import sympy
from sympy import ZZ, QQ

Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, A, x = witness
            elif len(witness) == 2:
                A, x = witness
                K = ZZ
            else:
                return [False, False, False, False]
        else:
            K, A, x = ZZ, ZZ, witness
    except Exception:
        return [False, False, False, False]

    # H1: A is a unital K-algebra
    try:
        h1 = False
        k_is_ring = getattr(K, 'is_ring', False) or K in (ZZ, QQ)
        a_is_ring = getattr(A, 'is_ring', False) or A in (ZZ, QQ)
        
        if k_is_ring and a_is_ring:
            if K == A or K == ZZ:
                h1 = True
    except Exception:
        h1 = False

    # H2: A is algebraic over K
    try:
        h2 = False
        if h1:
            if K == A:
                h2 = True
            elif K == ZZ and A == QQ:
                h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of A that is not a zero-divisor
    try:
        h3 = False
        if h1 and (x in A):
            is_domain = getattr(A, 'is_domain', False) or A in (ZZ, QQ)
            if is_domain:
                if x != 0:
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: x is not a unit in A
    try:
        neg_q = False
        if h1 and (x in A):
            if hasattr(A, 'is_unit'):
                neg_q = not A.is_unit(x)
            else:
                if A == ZZ:
                    neg_q = x not in (1, -1)
                elif A == QQ:
                    neg_q = x == 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a unital K-algebra",
    "H_2: A is algebraic over K",
    "H_3: x is an element of A that is not a zero-divisor",
    "¬Q: x is not a unit in A"
]

N_HYP = 3
NEG_Q_INDEX = 3