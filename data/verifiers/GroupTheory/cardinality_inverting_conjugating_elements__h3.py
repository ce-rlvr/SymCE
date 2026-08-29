import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, x = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'is_group')
    except Exception:
        h1 = False

    try:
        h2 = x in list(G.elements)
    except Exception:
        h2 = False

    try:
        x_inv = x**-1
        S = [g for g in G.elements if g * x * g**-1 == x_inv]
        h3 = isinstance(S, list)
    except Exception:
        h3 = False

    try:
        C_G_x = [g for g in G.elements if g * x * g**-1 == x]
        neg_q = (len(S) != 0) and (len(S) != len(C_G_x))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "H_3: S = {g in G | gxg^-1 = x^-1}",
    "¬Q: The cardinality of S is neither 0 nor |C_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3