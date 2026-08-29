import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Pre-define common polynomial rings that might be used as witnesses
Zx = ZZ.poly_ring(x)
Qx = QQ.poly_ring(x)
Zxy = ZZ.poly_ring(x, y)
Qxy = QQ.poly_ring(x, y)

CONDITION_LABELS = [
    "H_1: R is an integral domain (has a field of fractions K)",
    "H_2: S is a subring of K containing R",
    "¬Q: S is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is an integral domain (has a field of fractions K)
    try:
        K = R.get_field()
        h1 = K is not None
    except Exception:
        h1 = False
        
    # H_2: S is a subring of K containing R
    try:
        K = R.get_field()
        # R.unify(S) == S means R is contained in S
        r_in_s = (R.unify(S) == S)
        # S.unify(K) == K means S is contained in K
        s_in_k = (S.unify(K) == K)
        h2 = r_in_s and s_in_k
    except Exception:
        h2 = False
        
    # ¬Q: S is not a principal ideal domain
    try:
        # We check explicitly for False to ensure it is known not to be a PID
        neg_q = (S.is_PID is False)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]