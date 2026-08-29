import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        # A finite group is bi-orderable if and only if it is the trivial group.
        # We assume the witness provides finite groups (e.g., PermutationGroup).
        h1 = (H.order() == 1)
    except Exception:
        h1 = False
        
    try:
        # The direct product G x H is bi-orderable iff its order is 1 (for finite groups).
        # We want the negation of the conclusion, so it should NOT be bi-orderable.
        neg_q = (G.order() * H.order() > 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a bi-orderable group",
    "¬Q: G x H is not a bi-orderable group"
]

N_HYP = 1
NEG_Q_INDEX = 1
