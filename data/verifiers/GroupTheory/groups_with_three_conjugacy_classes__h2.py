import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: G is NOT isomorphic to Z3 and G is NOT isomorphic to S3
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            order = witness.order()
            # Z3 is the unique group of order 3
            is_z3 = (order == 3)
            # S3 is the unique non-abelian group of order 6
            is_s3 = (order == 6 and not witness.is_abelian)
            
            neg_q_ok = not (is_z3 or is_s3)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not isomorphic to Z3 or S3"
]

N_HYP = 1
NEG_Q_INDEX = 1