import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = None
            
        if not isinstance(G, PermutationGroup):
            h1_ok = False
        else:
            order = int(G.order())
            if p is not None:
                h1_ok = (order == p**2)
            else:
                root = math.isqrt(order)
                h1_ok = (root * root == order)
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G = witness[0]
        else:
            G = witness
            
        if not isinstance(G, PermutationGroup):
            neg_q_ok = False
        else:
            neg_q_ok = not G.is_abelian
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a group of order p^2",
    "¬Q: G is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1