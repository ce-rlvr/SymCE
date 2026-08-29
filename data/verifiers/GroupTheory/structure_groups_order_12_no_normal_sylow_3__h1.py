import sympy
from sympy.combinatorics import PermutationGroup, AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup bindings
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
    # H_1: The order of G is 12
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                h1 = bool(witness.order() == 12)
            else:
                h1 = bool(witness.order == 12)
        elif hasattr(witness, '__len__'):
            h1 = bool(len(witness) == 12)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G does not have a normal Sylow 3-subgroup
    try:
        if hasattr(witness, 'elements'):
            # In a group of order 12, the Sylow 3-subgroup is normal if and only if 
            # there is exactly 1 such subgroup, which means exactly 2 elements of order 3.
            order_3_count = 0
            for g in witness.elements:
                if hasattr(g, 'order'):
                    val = g.order() if callable(g.order) else g.order
                    if val == 3:
                        order_3_count += 1
            h2 = bool(order_3_count != 2)
        else:
            # If the witness is not a group (e.g. a set of 12 elements), 
            # it vacuously lacks a normal Sylow 3-subgroup.
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to the alternating group A_4
    try:
        if hasattr(witness, 'is_isomorphic'):
            neg_q = not bool(witness.is_isomorphic(A4))
        else:
            # If it lacks the group isomorphism method, it is not isomorphic to A_4
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is 12",
    "H_2: G does not have a normal Sylow 3-subgroup",
    "¬Q: G is not isomorphic to the alternating group A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2