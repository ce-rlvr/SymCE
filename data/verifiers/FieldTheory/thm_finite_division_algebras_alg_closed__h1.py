import sympy
from sympy import QQ, I, CC, RR, sqrt

# Top-level setup
# The witness should be a tuple (D, K) where D is a finite-dimensional division algebra over K.
# For example, (QQ.algebraic_field(I), QQ) or (CC, RR).

def conditions(witness) -> list[bool]:
    try:
        D, K = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = False
        # Check if D and K are fields (a field is a commutative division algebra)
        if getattr(D, 'is_Field', False) and getattr(K, 'is_Field', False):
            if D == K:
                h1 = True
            # Check if D is a finite extension of K
            elif type(D).__name__ == 'AlgebraicField' and getattr(D, 'domain', None) == K:
                h1 = True
            # CC is a 2-dimensional division algebra over RR
            elif D == CC and K == RR:
                h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = False
        if h1:
            if D == CC and K == RR:
                neg_q = True
            elif D != K:
                # If D is an AlgebraicField over K, it is isomorphic to K iff its degree is 1.
                if type(D).__name__ == 'AlgebraicField' and hasattr(D, 'mod'):
                    if D.mod.degree() > 1:
                        neg_q = True
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: D is a finite-dimensional division algebra over K",
    "¬Q: D is not isomorphic to K"
]

N_HYP = 1
NEG_Q_INDEX = 1