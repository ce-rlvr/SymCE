import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    # H_1: Let n be an integer such that n >= 5
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            h1 = n >= 5
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The commutator subgroup A_n' is NOT equal to A_n
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            if n >= 1:
                G = AlternatingGroup(n)
                D = G.derived_subgroup()
                # Since D is always a subgroup of G, they are equal iff their orders are equal.
                # The conclusion fails (neg_q is True) if they are not equal.
                neg_q = D.order() != G.order()
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 5",
    "¬Q: The commutator subgroup A_n' is not equal to A_n"
]

N_HYP = 1
NEG_Q_INDEX = 1