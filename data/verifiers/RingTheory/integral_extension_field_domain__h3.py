import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y

# Setup standard rings and fields for potential witnesses
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_frac_x = ZZ.frac_field(x)
QQ_frac_x = QQ.frac_field(x)

def is_domain(D):
    try:
        from sympy.polys.domains import Domain
        if isinstance(D, Domain):
            return True
    except Exception:
        pass
    return hasattr(D, 'is_Field') and hasattr(D, 'unify')

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are integral domains
    try:
        h1 = is_domain(R) and is_domain(S)
    except Exception:
        h1 = False
        
    # H_2: R is a subring of S
    try:
        # In sympy's domain system, S.unify(R) returns the smallest domain containing both.
        # If S.unify(R) == S, then R is a subring of S.
        h2 = (S.unify(R) == S)
    except Exception:
        h2 = False
        
    # ¬Q: R is a field if and only if S is a field is FALSE
    # This means exactly one of them is a field and the other is not.
    try:
        neg_q = bool(R.is_Field) != bool(S.is_Field)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are integral domains",
    "H_2: R is a subring of S",
    "¬Q: R is a field if and only if S is a field is false"
]

N_HYP = 2
NEG_Q_INDEX = 2