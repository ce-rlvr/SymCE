import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, X, action, x, g, y = witness
    except Exception:
        return [False] * 6

    G_elements = []
    e = None

    # H1: G is a group
    try:
        G_elements = list(G)
        e = G.identity
        h1 = True
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        X_list = list(X)
        h2 = True
    except Exception:
        h2 = False
        X_list = []

    # H3: G acts on X
    try:
        if not h1 or not h2:
            h3 = False
        else:
            h3 = True
            # Identity acts as identity
            for elem in X_list:
                if action(e, elem) != elem:
                    h3 = False
                    break
            # Compatibility (left action)
            if h3:
                for g1 in G_elements:
                    for g2 in G_elements:
                        for elem in X_list:
                            if action(g1 * g2, elem) != action(g1, action(g2, elem)):
                                h3 = False
                                break
                        if not h3: break
                    if not h3: break
            # Closure
            if h3:
                for g_elem in G_elements:
                    for elem in X_list:
                        if action(g_elem, elem) not in X_list:
                            h3 = False
                            break
                    if not h3: break
    except Exception:
        h3 = False

    # H4: x \in X
    try:
        h4 = x in X_list
    except Exception:
        h4 = False

    # H5: y = g \cdot x
    try:
        h5 = (y == action(g, x))
    except Exception:
        h5 = False

    # neg_Q: Stab(y) != g Stab(x) g^{-1}
    try:
        if not h1:
            neg_q = False
        else:
            stab_x = set()
            for h in G_elements:
                if action(h, x) == x:
                    stab_x.add(h)

            stab_y = set()
            for h in G_elements:
                if action(h, y) == y:
                    stab_y.add(h)

            g_stab_x_ginv = set()
            g_inv = g**-1
            for h in stab_x:
                g_stab_x_ginv.add(g * h * g_inv)

            neg_q = (stab_y != g_stab_x_ginv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "H_4: x in X",
    "H_5: y = g \\cdot x",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5