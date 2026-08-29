import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            g = witness.get('g')
        else:
            G, H, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = H.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: The index of H in G is equal to 2
    try:
        h2 = G.order() == 2 * H.order()
    except Exception:
        h2 = False

    # H_3: g is an element of G
    try:
        h3 = g in G
    except Exception:
        h3 = False

    # neg_Q: The element g^2 is not in H
    try:
        neg_q = (g**2) not in H
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is equal to 2",
    "H_3: g is an element of G",
    "¬Q: The element g^2 is not in H"
]

N_HYP = 3
NEG_Q_INDEX = 3