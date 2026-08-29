import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: x and y are elements of G
    try:
        elements = list(G.elements)
        h2_ok = (x in elements) and (y in elements)
    except Exception:
        h2_ok = False

    # H_3: x and y commute
    try:
        h3_ok = bool(x * y == y * x)
    except Exception:
        h3_ok = False

    # neg_Q: The conclusion fails
    try:
        elements = list(G.elements)
        
        C_G_x = set(g for g in elements if g * x == x * g)
        C_G_y = set(g for g in elements if g * y == y * g)
        xy = x * y
        C_G_xy = set(g for g in elements if g * xy == xy * g)
        
        intersection = C_G_x.intersection(C_G_y)
        
        cl_xy = set(g * xy * (g**-1) for g in elements)
        
        if len(intersection) == 0:
            conclusion = False
        else:
            index = len(elements) // len(intersection)
            conclusion = (C_G_xy == intersection) and (len(cl_xy) == index)
            
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x and y are elements of G",
    "H_3: x and y commute",
    "¬Q: C_G(xy) is not C_G(x) intersection C_G(y) or size of conjugacy class of xy is not the index"
]

N_HYP = 3
NEG_Q_INDEX = 3