import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        x = witness['x']
        f = witness['f']
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = x in G
    except Exception:
        h2 = False

    try:
        x_inv = x**-1
        if callable(f):
            f_x_inv = f(x_inv)
            f_x = f(x)
        else:
            f_x_inv = f[x_inv]
            f_x = f[x]
        
        neg_q = bool(f_x_inv != f_x**-1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: x is an element of G",
    "¬Q: f(x^-1) != (f(x))^-1"
]

N_HYP = 2
NEG_Q_INDEX = 2