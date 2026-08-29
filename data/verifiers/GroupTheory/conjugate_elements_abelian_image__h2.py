import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    # H_1: G and H are groups
    try:
        G = witness['G']
        H = witness['H']
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements')
    except Exception:
        h1 = False

    # H_2: H is an abelian group
    try:
        H = witness['H']
        h2 = bool(H.is_abelian)
    except Exception:
        h2 = False

    # H_3: x and y are elements of G such that x and y are conjugate in G
    try:
        G = witness['G']
        x = witness['x']
        y = witness['y']
        h3 = False
        elements = list(G.elements)
        if x in elements and y in elements:
            for g in elements:
                if g * x * (g**-1) == y:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: f(x) != f(y)
    try:
        f = witness['f']
        x = witness['x']
        y = witness['y']
        if callable(f):
            fx = f(x)
            fy = f(y)
        else:
            fx = f[x]
            fy = f[y]
        neg_q = bool(fx != fy)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is an abelian group",
    "H_3: x and y are elements of G such that x and y are conjugate in G",
    "¬Q: f(x) != f(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3