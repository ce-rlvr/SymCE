import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Standard algebra objects
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
        G, N, X, action, x = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(X, (list, set, tuple)):
            G_elements = list(G.generate())
            X_set = set(X) if isinstance(X, (list, tuple)) else X
            id_acts_trivially = all(action(G.identity, y) == y for y in X)
            hom_holds = all(action(g, action(h, y)) == action(g*h, y) for g in G_elements for h in G_elements for y in X)
            closure_holds = all(action(g, y) in X_set for g in G_elements for y in X)
            h1 = id_acts_trivially and hom_holds and closure_holds
    except Exception:
        h1 = False

    # H_2: N acts trivially on X
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(X, (list, set, tuple)):
            G_elements = list(G.generate())
            G_elements_set = set(G_elements)
            N_elements = list(N.generate())
            is_subgroup = all(n in G_elements_set for n in N_elements)
            if is_subgroup:
                h2 = all(action(n, y) == y for n in N_elements for y in X)
    except Exception:
        h2 = False

    # H_3: G/N acts on X via the induced action
    try:
        h3 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(X, (list, set, tuple)):
            G_elements = list(G.generate())
            N_elements = list(N.generate())
            well_defined = True
            for g in G_elements:
                for n in N_elements:
                    gn = g * n
                    if any(action(g, y) != action(gn, y) for y in X):
                        well_defined = False
                        break
                if not well_defined:
                    break
            h3 = well_defined
    except Exception:
        h3 = False

    # H_4: x is an element of X
    try:
        h4 = False
        if isinstance(X, (list, set, tuple)):
            h4 = x in X
    except Exception:
        h4 = False

    # neg_Q: G/N or G_x/N is not a quotient group (N is not normal in G or G_x)
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(X, (list, set, tuple)):
            G_elements = list(G.generate())
            N_elements = list(N.generate())
            N_elements_set = set(N_elements)
            
            N_normal_in_G = True
            for g in G_elements:
                g_inv = ~g
                for n in N_elements:
                    if (g * n * g_inv) not in N_elements_set:
                        N_normal_in_G = False
                        break
                if not N_normal_in_G:
                    break
            
            G_x = [g for g in G_elements if action(g, x) == x]
            N_normal_in_Gx = True
            for g in G_x:
                g_inv = ~g
                for n in N_elements:
                    if (g * n * g_inv) not in N_elements_set:
                        N_normal_in_Gx = False
                        break
                if not N_normal_in_Gx:
                    break
            
            neg_q = (not N_normal_in_G) or (not N_normal_in_Gx)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N acts trivially on X",
    "H_3: G/N acts on X via the induced action",
    "H_4: x is an element of X",
    "¬Q: G/N or G_x/N is not a quotient group (N is not normal in G or G_x)"
]

N_HYP = 4
NEG_Q_INDEX = 4