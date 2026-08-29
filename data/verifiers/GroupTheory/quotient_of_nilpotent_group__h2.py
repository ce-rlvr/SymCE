import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a nilpotent group
    try:
        h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False
        
    # ¬Q: G/N is not a nilpotent group
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = True
        elif not G.is_subgroup(N):
            neg_q = True
        elif not G.is_normal(N):
            neg_q = True
        else:
            Q_grp = G.quotient_group(N)
            neg_q = not bool(Q_grp.is_nilpotent)
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G/N is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1