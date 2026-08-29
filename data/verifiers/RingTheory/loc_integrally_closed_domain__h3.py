import sympy
from sympy import ZZ, QQ

# Top-level setup
# ZZ and QQ are available for witness construction

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    try:
        # H_1: R is an integrally closed domain
        # In sympy, ZZ and QQ are domains. We check if it's a UFD or Field,
        # both of which imply the domain is integrally closed.
        h1 = bool(getattr(R, 'is_UFD', False) or getattr(R, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        # H_2: S is a multiplicatively closed subset of R
        is_subset = all(s in R for s in S)
        is_mult_closed = all((s1 * s2) in S for s1 in S for s2 in S)
        h2 = bool(is_subset and is_mult_closed)
    except Exception:
        h2 = False
        
    try:
        # ¬Q: S^{-1}R is not an integrally closed domain
        # The localization S^{-1}R is an integrally closed domain UNLESS 0 is in S.
        # If 0 is in S, S^{-1}R is the zero ring, which is not an integral domain.
        neg_q = bool(0 in S)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integrally closed domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}R is not an integrally closed domain"
]

N_HYP = 2
NEG_Q_INDEX = 2