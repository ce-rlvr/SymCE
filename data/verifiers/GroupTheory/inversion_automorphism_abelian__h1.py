import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    try:
        # H_1: The map phi(x) = x^-1 satisfies phi(xy) = phi(x)phi(y) for all x, y in G
        elements = list(witness.elements)
        h1_ok = True
        for x in elements:
            for y in elements:
                if (x * y)**-1 != (x**-1) * (y**-1):
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    try:
        # neg_Q: The group G is not abelian
        neg_q_ok = not witness.is_abelian
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The map phi(x) = x^-1 satisfies phi(xy) = phi(x)phi(y) for all x, y in G",
    "¬Q: The group G is not abelian"
]

N_HYP = 1
NEG_Q_INDEX = 1