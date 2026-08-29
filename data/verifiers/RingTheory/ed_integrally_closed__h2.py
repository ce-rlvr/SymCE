import sympy
from sympy import ZZ, QQ, sqrt, I, minpoly, Symbol
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: R is not integrally closed in K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (R, K), checks if R is a Euclidean domain and if R is NOT integrally closed in K.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        R, K = witness
    except Exception:
        return [False, False]
    
    # H_1: R is a Euclidean domain
    h1 = False
    try:
        if R == ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif hasattr(R, 'is_EuclideanRing') and R.is_EuclideanRing:
            h1 = True
    except Exception:
        pass

    # ¬Q: R is NOT integrally closed in K
    neg_q = False
    try:
        if R == ZZ:
            # If K is an algebraic field over QQ
            if hasattr(K, 'is_AlgebraicField') and K.is_AlgebraicField:
                if hasattr(K, 'mod') and K.mod.degree() > 1:
                    neg_q = True
                elif hasattr(K, 'ext'):
                    if minpoly(K.ext).degree() > 1:
                        neg_q = True
            # If K is provided as an algebraic element (e.g., sqrt(5))
            elif hasattr(K, 'is_algebraic') and K.is_algebraic:
                if minpoly(K).degree() > 1:
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]