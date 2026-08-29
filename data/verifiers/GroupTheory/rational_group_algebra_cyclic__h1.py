import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

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
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q_ok = False
        else:
            n = witness.order()
            is_cyclic = False
            for g in witness.elements:
                if g.order() == n:
                    is_cyclic = True
                    break
            neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is the field of rational numbers",
    "¬Q: The group algebra of G over Q is not isomorphic to the direct product of cyclotomic fields"
]

N_HYP = 1
NEG_Q_INDEX = 1