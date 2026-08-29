import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

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
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or (hasattr(G, 'elements') and hasattr(G, 'contains'))
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = False
        if h1 and G.contains(x) and G.contains(y):
            for g in G.elements:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g**-1
                if g * x * inv_g == y or inv_g * x * g == y:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # neg_Q: C_G(x) is NOT isomorphic to C_G(y)
    try:
        neg_q = False
        if h1:
            cent_x = [g for g in G.elements if g * x == x * g]
            cent_y = [g for g in G.elements if g * y == y * g]
            
            if isinstance(G, PermutationGroup):
                Cx = PermutationGroup(*cent_x)
                Cy = PermutationGroup(*cent_y)
                neg_q = not Cx.is_isomorphic(Cy)
            else:
                if len(cent_x) != len(cent_y):
                    neg_q = True
                else:
                    try:
                        orders_x = sorted([g.order() for g in cent_x])
                        orders_y = sorted([g.order() for g in cent_y])
                        if orders_x != orders_y:
                            neg_q = True
                        else:
                            neg_q = False
                    except Exception:
                        neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "¬Q: C_G(x) is not isomorphic to C_G(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2