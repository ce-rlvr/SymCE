import sympy
from sympy import Interval, FiniteSet, Union, Intersection, oo, Reals

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: For every a in A and every b in B, a < b.
    try:
        if A.is_empty == True or B.is_empty == True:
            h1 = True
        else:
            sup_A = A.sup
            inf_B = B.inf
            if bool(sup_A < inf_B):
                h1 = True
            elif sup_A == inf_B:
                h1 = (A.intersect(B).is_empty == True)
            else:
                h1 = False
    except Exception:
        h1 = False

    # neg_Q: The conclusion FAILS.
    # Conclusion: There exists a unique real number c such that either c is the maximum of A or c is the minimum of B.
    try:
        C = set()
        
        if A.is_empty != True:
            sup_A = A.sup
            if sup_A.is_real and A.contains(sup_A) in (True, sympy.true):
                C.add(sup_A)
                
        if B.is_empty != True:
            inf_B = B.inf
            if inf_B.is_real and B.contains(inf_B) in (True, sympy.true):
                C.add(inf_B)
                
        # The conclusion holds if there is exactly one such number.
        # It fails if there are 0 or >1 such numbers.
        neg_q = (len(C) != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: For every a in A and every b in B, a < b",
    "¬Q: It is not the case that there exists a unique real number c such that c is the maximum of A or c is the minimum of B"
]

N_HYP = 1
NEG_Q_INDEX = 1