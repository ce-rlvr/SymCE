import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        H1 = hasattr(witness, 'elements') and hasattr(witness, 'identity')
        if H1:
            _ = witness.identity * witness.identity
    except Exception:
        H1 = False

    neg_Q = False
    try:
        if H1:
            elements = list(witness.elements)
            identity = witness.identity
            
            for x in elements:
                x_inv = x**-1
                for y in elements:
                    y_inv = y**-1
                    for z in elements:
                        z_inv = z**-1
                        
                        # Check left-normed interpretation
                        c1 = x_inv * y * x * y_inv
                        c1_inv = c1**-1
                        l1_base = c1_inv * z_inv * c1 * z
                        l1 = y_inv * l1_base * y
                        
                        c2 = y_inv * z * y * z_inv
                        c2_inv = c2**-1
                        l2_base = c2_inv * x_inv * c2 * x
                        l2 = z_inv * l2_base * z
                        
                        c3 = z_inv * x * z * x_inv
                        c3_inv = c3**-1
                        l3_base = c3_inv * y_inv * c3 * y
                        l3 = x_inv * l3_base * x
                        
                        if l1 * l2 * l3 != identity:
                            neg_Q = True
                            break
                        
                        # Check right-normed interpretation
                        rc1 = y * z_inv * y_inv * z
                        rc1_inv = rc1**-1
                        r1_base = x_inv * rc1_inv * x * rc1
                        r1 = y_inv * r1_base * y
                        
                        rc2 = z * x_inv * z_inv * x
                        rc2_inv = rc2**-1
                        r2_base = y_inv * rc2_inv * y * rc2
                        r2 = z_inv * r2_base * z
                        
                        rc3 = x * y_inv * x_inv * y
                        rc3_inv = rc3**-1
                        r3_base = z_inv * rc3_inv * z * rc3
                        r3 = x_inv * r3_base * x
                        
                        if r1 * r2 * r3 != identity:
                            neg_Q = True
                            break
                    if neg_Q:
                        break
                if neg_Q:
                    break
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The Hall-Witt identity fails for some x, y, z in G"
]

N_HYP = 1
NEG_Q_INDEX = 1