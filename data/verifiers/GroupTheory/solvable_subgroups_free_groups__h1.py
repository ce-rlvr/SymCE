import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: H is a solvable subgroup of F
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            H, F = witness
            is_subgroup = all(g in F for g in H.generators)
            h1 = is_subgroup and bool(H.is_solvable)
        else:
            H = witness
            h1 = bool(H.is_solvable)
    except Exception:
        h1 = False

    # ¬Q: H is not a cyclic group
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            H, F = witness
        else:
            H = witness
            
        neg_q = not bool(H.is_cyclic)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a solvable subgroup of F",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1