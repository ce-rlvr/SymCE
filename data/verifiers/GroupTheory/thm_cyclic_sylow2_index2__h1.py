import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: The order of G is even
    try:
        order = witness.order()
        h1 = bool(order % 2 == 0)
    except Exception:
        h1 = False

    # H_2: The Sylow 2-subgroup of G is cyclic
    try:
        s2 = witness.sylow_subgroup(2)
        h2 = bool(s2.is_cyclic)
    except Exception:
        h2 = False

    # ¬Q: G does not possess a normal subgroup of index 2
    # A finite group G has a normal subgroup of index 2 iff its abelianization G/G' has even order.
    # Therefore, G does NOT possess a normal subgroup of index 2 iff the index [G : G'] is odd.
    try:
        derived = witness.derived_subgroup()
        index = witness.order() // derived.order()
        neg_q = bool(index % 2 != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is even",
    "H_2: The Sylow 2-subgroup of G is cyclic",
    "¬Q: G does not possess a normal subgroup of index 2"
]

N_HYP = 2
NEG_Q_INDEX = 2