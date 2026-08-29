import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    # H_1: H is a finitely generated subgroup of G
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
            h1_ok = bool(hasattr(H, 'is_subgroup') and H.is_subgroup(G) and hasattr(H, 'generators'))
        else:
            H = witness
            # If G is not explicitly provided, we verify H is a finitely generated group
            h1_ok = bool(isinstance(H, PermutationGroup) and hasattr(H, 'generators'))
    except Exception:
        h1_ok = False

    # ¬Q: H is not a cyclic group
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            _, H = witness
        else:
            H = witness
        neg_q_ok = not bool(H.is_cyclic)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a finitely generated subgroup of G",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1