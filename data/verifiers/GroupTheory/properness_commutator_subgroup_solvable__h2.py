import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            solvable = witness.is_solvable
            if callable(solvable):
                solvable = solvable()
            h2 = bool(solvable)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            order_G = witness.order
            if callable(order_G):
                order_G = order_G()
                
            derived = witness.derived_subgroup
            if callable(derived):
                derived = derived()
                
            order_derived = derived.order
            if callable(order_derived):
                order_derived = order_derived()
                
            neg_q = bool(order_derived == order_G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is a solvable group",
    "¬Q: The commutator subgroup G' is not a proper subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2