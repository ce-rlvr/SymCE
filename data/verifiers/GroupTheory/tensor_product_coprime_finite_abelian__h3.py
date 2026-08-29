import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
    try:
        if len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    try:
        order_A = int(A.order())
        h1 = bool(getattr(A, 'is_abelian', False) and order_A >= 1)
    except Exception:
        h1 = False

    try:
        order_B = int(B.order())
        h2 = bool(getattr(B, 'is_abelian', False) and order_B >= 1)
    except Exception:
        h2 = False

    try:
        # The tensor product of finite abelian groups A and B over Z is trivial
        # if and only if gcd(|A|, |B|) == 1.
        # The conclusion states the tensor product is trivial.
        # The negated conclusion (neg_Q) is True when the tensor product is NOT trivial.
        order_A = int(A.order())
        order_B = int(B.order())
        neg_q = bool(math.gcd(order_A, order_B) > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: B is a finite abelian group",
    "¬Q: The tensor product A ⊗ B is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2