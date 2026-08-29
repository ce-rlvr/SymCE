import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The restricted action of H on X is transitive",
    "H_3: x is an element of X",
    "¬Q: G cannot be factored as G = H G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, X, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = H.is_subgroup(G)
        else:
            h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H_2: The restricted action of H on X is transitive
    try:
        if not X:
            h2 = False
        else:
            elem = list(X)[0]
            orbit = set(H.orbit(elem))
            h2 = (set(X) == orbit)
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = (x in X)
    except Exception:
        h3 = False

    # ¬Q: G cannot be factored as G = H G_x
    try:
        G_x = G.stabilizer(x)
        H_x = H.stabilizer(x)
        # The size of the set H G_x is |H| * |G_x| / |H \cap G_x|
        # H_x is exactly the intersection of H and G_x
        size_HGx = (H.order() * G_x.order()) // H_x.order()
        neg_q = (G.order() != size_HGx)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]