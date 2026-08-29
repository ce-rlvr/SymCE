import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Assume the order of G is exactly 255.
    try:
        h1_ok = bool(witness.order() == 255)
    except Exception:
        h1_ok = False

    # ¬Q: G does not have a unique, normal Sylow 17-subgroup.
    # By Sylow's theorems, a Sylow 17-subgroup is unique iff it is normal.
    # Since 17 is prime, any Sylow 17-subgroup has exactly 16 elements of order 17.
    # Thus, the Sylow 17-subgroup is unique iff the group has exactly 16 elements of order 17.
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        elif hasattr(witness, 'generate'):
            elements = list(witness.generate())
        else:
            elements = []
            
        if not elements:
            neg_q_ok = False
        else:
            count_17 = sum(1 for g in elements if g.order() == 17)
            neg_q_ok = bool(count_17 != 16)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G has order exactly 255",
    "¬Q: G does not have a unique, normal Sylow 17-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1