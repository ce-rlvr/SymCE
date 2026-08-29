import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # H_1: G is a simple group
    try:
        if hasattr(witness, 'is_simple') and witness.is_simple is not None:
            h1_ok = bool(witness.is_simple)
        else:
            # A group is simple if its only normal subgroups are the trivial group and itself.
            h1_ok = len(witness.normal_subgroups()) == 2
    except Exception:
        h1_ok = False

    # ¬Q: The center Z(G) is not the trivial subgroup
    try:
        center = witness.center()
        if hasattr(center, 'order'):
            order_val = center.order
            if callable(order_val):
                neg_q_ok = order_val() > 1
            else:
                neg_q_ok = order_val > 1
        else:
            neg_q_ok = len(center) > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1