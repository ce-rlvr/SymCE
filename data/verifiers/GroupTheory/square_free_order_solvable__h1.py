import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import factorint

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
    # H_1: The order of G is a square-free integer
    try:
        order = witness.order()
        if order <= 0:
            h1_ok = False
        else:
            factors = factorint(order)
            h1_ok = all(v == 1 for v in factors.values())
    except Exception:
        h1_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not witness.is_solvable
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is a square-free integer",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1