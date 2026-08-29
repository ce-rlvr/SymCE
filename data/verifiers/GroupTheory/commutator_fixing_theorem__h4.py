import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False] * 4 + [False]
        G, g, h, x = witness
    except Exception:
        return [False] * 4 + [False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(h1 and (g in G) and (h in G))
    except Exception:
        h2 = False

    try:
        h3 = bool(h1 and isinstance(x, (int, sympy.Integer)) and 0 <= x < G.degree)
    except Exception:
        h3 = False

    try:
        h4 = bool(h3 and h(x) == x)
    except Exception:
        h4 = False

    try:
        if not (h2 and h3):
            neg_q = False
        else:
            hx = h(x)
            ghx = g(hx)
            hinv_ghx = (~h)(ghx)
            commutator_x = (~g)(hinv_ghx)
            neg_q = bool(commutator_x != x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: g and h are elements of G",
    "H_3: x is an element of X",
    "H_4: x is fixed by h",
    "not_Q: x is not fixed by the commutator of g and h"
]

N_HYP = 4
NEG_Q_INDEX = 4