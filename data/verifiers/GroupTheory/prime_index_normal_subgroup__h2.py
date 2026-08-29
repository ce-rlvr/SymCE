import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    # H_1: G is a finite solvable group
    try:
        solvable = witness.is_solvable
        if callable(solvable):
            h1 = bool(solvable())
        else:
            h1 = bool(solvable)
    except Exception:
        h1 = False

    # ¬Q: G does not contain a normal subgroup of prime index
    try:
        # A finite group G has a normal subgroup of prime index if and only if 
        # its derived subgroup G' is a proper subgroup of G (i.e., G' != G).
        derived = witness.derived_subgroup()
        
        order_derived = derived.order() if callable(derived.order) else derived.order
        order_witness = witness.order() if callable(witness.order) else witness.order
        
        has_prime_index_normal = (order_derived < order_witness)
        neg_q = not has_prime_index_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "¬Q: G does not contain a normal subgroup of prime index"
]

N_HYP = 1
NEG_Q_INDEX = 1