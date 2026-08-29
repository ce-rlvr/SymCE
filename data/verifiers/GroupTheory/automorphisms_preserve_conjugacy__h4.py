import sympy
from sympy.combinatorics import PermutationGroup
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            G, x, y, g_wit, phi = witness
        elif len(witness) == 4:
            G, x, y, phi = witness
            g_wit = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, "elements")
    except Exception:
        h1 = False

    # H2: x and y are elements of G
    try:
        h2 = (x in G) and (y in G)
    except Exception:
        h2 = False

    # H3: There exists g in G such that y = g * x * g**-1
    try:
        if g_wit is not None:
            h3 = (g_wit in G) and (y == g_wit * x * g_wit**-1)
        else:
            h3 = any((y == g * x * g**-1) for g in G.elements)
    except Exception:
        h3 = False

    # neg_Q: phi(y) != phi(g) * phi(x) * phi(g)**-1
    try:
        def check_phi(g_val):
            if isinstance(phi, dict):
                py = phi[y]
                px = phi[x]
                pg = phi[g_val]
            else:
                py = phi(y)
                px = phi(x)
                pg = phi(g_val)
            return py != pg * px * pg**-1

        if g_wit is not None:
            neg_q = check_phi(g_wit)
        else:
            neg_q = any((y == g * x * g**-1) and check_phi(g) for g in G.elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: There exists an element g in G such that y = gxg^{-1}",
    "¬Q: phi(y) != phi(g)phi(x)phi(g)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3