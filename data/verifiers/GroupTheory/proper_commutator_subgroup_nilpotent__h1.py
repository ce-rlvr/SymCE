import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is not the trivial group
    try:
        h1_ok = bool(witness.order() > 1)
    except Exception:
        h1_ok = False

    # ¬Q: The commutator subgroup of G is NOT a strictly proper subgroup of G
    # Since the commutator subgroup is always a subgroup, it is not strictly proper
    # if and only if it is equal to G (i.e., G is a perfect group).
    try:
        commutator_subgroup = witness.derived_subgroup()
        neg_q_ok = bool(commutator_subgroup.order() == witness.order())
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "¬Q: The commutator subgroup of G is not a strictly proper subgroup of G (G is perfect)"
]

N_HYP = 1
NEG_Q_INDEX = 1