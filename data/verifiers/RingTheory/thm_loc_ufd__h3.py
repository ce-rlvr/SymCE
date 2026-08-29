import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a Unique Factorization Domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, S = witness
        S = list(S)
    except Exception:
        return [False, False, False]
    
    # H1: R is a UFD
    try:
        h1 = getattr(R, 'is_UFD', False)
        if not h1:
            if R in [ZZ, QQ]:
                h1 = True
    except Exception:
        h1 = False
        
    # H2: S is a multiplicatively closed subset of R
    try:
        in_R = all((a in R) for a in S)
        closed = all(any((a * b) == c for c in S) for a in S for b in S)
        h2 = bool(in_R and closed)
    except Exception:
        h2 = False
        
    # neg_Q: S^{-1}R is NOT a UFD
    # The localization of a UFD at S is a UFD if and only if 0 is not in S.
    # If 0 is in S, the localized ring is the zero ring, which is not an integral domain,
    # and therefore not a Unique Factorization Domain.
    try:
        zero = getattr(R, 'zero', 0)
        neg_q = any(zero == c for c in S)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]