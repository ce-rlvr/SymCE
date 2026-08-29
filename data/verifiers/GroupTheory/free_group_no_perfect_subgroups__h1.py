import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        if isinstance(witness, tuple):
            H, F = witness
            try:
                is_subgroup = all(g in F for g in H.generators)
            except Exception:
                is_subgroup = False
            
            try:
                is_perfect = H.derived_subgroup().order() == H.order()
            except Exception:
                is_perfect = False
                
            h1 = is_subgroup and is_perfect
        else:
            H = witness
            h1 = H.derived_subgroup().order() == H.order()
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple):
            H, F = witness
        else:
            H = witness
        neg_q = H.order() > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a perfect subgroup of F",
    "¬Q: H is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1