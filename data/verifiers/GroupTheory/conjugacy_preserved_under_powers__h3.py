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
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    try:
        h2 = (x in G) and (y in G)
    except Exception:
        h2 = False

    # H_3: n is an integer
    try:
        h3 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h3 = False

    # ¬Q: x^n and y^n are not conjugate in G
    try:
        xn = x**n
        yn = y**n
        are_conj = False
        for g in G.elements:
            if g * xn * ~g == yn:
                are_conj = True
                break
        neg_q = not are_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3