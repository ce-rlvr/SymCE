import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
        h1_ok = (witness.is_abelian is False)
    except Exception:
        h1_ok = False

    try:
        order_G = witness.order()
        center_G = witness.center()
        order_Z = center_G.order()
        if order_G % order_Z != 0:
            neg_q_ok = False
        else:
            index = order_G // order_Z
            neg_q_ok = bool(isprime(index))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not an abelian group",
    "not Q: The index of Z(G) in G is a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1