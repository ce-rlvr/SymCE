import sympy
from sympy import CC, RR, QQ, ZZ
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # The witness could be a tuple (K, L) or just L (with K implicitly CC)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
        else:
            K = CC
            L = witness
    except Exception:
        return [False, False]
        
    # H_1: K is an algebraically closed field
    try:
        # In SymPy, CC is the standard algebraically closed field
        h1 = (K == CC)
    except Exception:
        h1 = False
        
    # ¬Q: L is NOT a regular extension of K
    try:
        def contains_K(domain, target_K):
            if domain == target_K:
                return True
            if hasattr(domain, 'domain') and domain.domain != domain:
                return contains_K(domain.domain, target_K)
            return False

        # A regular extension must be a field extension.
        is_field = getattr(L, 'is_Field', False)
        is_extension = contains_K(L, K)
        
        if K == CC:
            # Since CC is algebraically closed (hence perfect), any field extension 
            # over CC is separable, and CC is algebraically closed in it.
            # Thus, L is a regular extension of CC iff L is a field extension of CC.
            is_regular = is_field and is_extension
        else:
            # If K is not CC, we cannot easily verify regularity in SymPy,
            # but since H1 requires K == CC, this branch is practically unreachable for a valid witness.
            is_regular = False
            
        neg_q = not is_regular
    except Exception:
        # If evaluation fails, we assume it's not a valid regular extension
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: L is not a regular extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1