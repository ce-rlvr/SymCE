import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
    # H_1: G is a non-abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            if callable(witness.is_abelian):
                is_ab = witness.is_abelian()
            else:
                is_ab = witness.is_abelian
            h1_ok = (is_ab == False)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The center Z(G) is not the trivial subgroup
    try:
        if hasattr(witness, 'center'):
            if callable(witness.center):
                c = witness.center()
            else:
                c = witness.center
            
            if hasattr(c, 'order'):
                if callable(c.order):
                    neg_q_ok = c.order() > 1
                else:
                    neg_q_ok = c.order > 1
            else:
                neg_q_ok = len(list(c)) > 1
        else:
            elements = list(witness.elements)
            center_size = sum(1 for g in elements if all(g * h == h * g for h in elements))
            neg_q_ok = center_size > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1
