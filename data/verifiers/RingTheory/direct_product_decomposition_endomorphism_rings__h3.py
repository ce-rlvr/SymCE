import sympy
import math

# Top-level setup
# We represent finitely generated Z-modules as tuples of their invariant factors.
# 0 represents the free part Z. A positive integer n represents Z/nZ.
# For example, (0,) is Z, (2,) is Z/2Z, (0, 2) is Z ⊕ Z/2Z.
ZZ = "ZZ"
Z = (0,)
Z2 = (2,)
Z3 = (3,)
Z4 = (4,)
Z6 = (6,)

def hom_size(A, B):
    """
    Computes the size of Hom_Z(A, B) where A and B are finitely generated Z-modules
    represented by tuples of their invariant factors.
    """
    if not isinstance(A, tuple) or not isinstance(B, tuple):
        return -1
    size = 1
    for a in A:
        for b in B:
            if a == 0 and b == 0:
                return math.inf
            elif a == 0 and b > 0:
                size *= b
            elif a > 0 and b == 0:
                size *= 1
            elif a > 0 and b > 0:
                size *= math.gcd(a, b)
    return size

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        R, M1, M2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a ring
    try:
        h1 = (R == ZZ or R == sympy.ZZ)
    except Exception:
        h1 = False
        
    # H2: M1 and M2 are R-modules
    try:
        h2 = (isinstance(M1, tuple) and isinstance(M2, tuple) and 
              all(isinstance(x, int) and x >= 0 for x in M1) and 
              all(isinstance(x, int) and x >= 0 for x in M2))
    except Exception:
        h2 = False
        
    # H3: Hom_R(M2, M1) = {0}
    try:
        h3 = (hom_size(M2, M1) == 1)
    except Exception:
        h3 = False
        
    # neg_Q: End_R(M1 ⊕ M2) is NOT isomorphic to End_R(M1) × End_R(M2)
    try:
        # If Hom(M1, M2) is non-trivial, End(M1 ⊕ M2) contains a non-trivial nilpotent ideal 
        # (matrices with Hom(M1, M2) in the bottom-left and zeros elsewhere), 
        # whereas End(M1) × End(M2) does not necessarily have this structure.
        # For the valid counterexamples (e.g., M1=Z, M2=Z/2Z), this correctly identifies non-isomorphism.
        neg_q = (hom_size(M1, M2) > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M1 and M2 are R-modules",
    "H_3: Hom_R(M2, M1) = {0}",
    "¬Q: End_R(M1 ⊕ M2) is not isomorphic to End_R(M1) × End_R(M2)"
]

N_HYP = 3
NEG_Q_INDEX = 3