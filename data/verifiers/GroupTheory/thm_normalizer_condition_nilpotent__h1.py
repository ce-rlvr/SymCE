import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "¬Q: H is not strictly contained in N_G(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(H.is_subgroup(G) and H.order() < G.order())
    except Exception:
        h1 = False
        
    try:
        neg_q = True
        for g in G.generate():
            if g not in H:
                normalizes = True
                for gen in H.generators:
                    if (g * gen * ~g) not in H:
                        normalizes = False
                        break
                if normalizes:
                    neg_q = False
                    break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]