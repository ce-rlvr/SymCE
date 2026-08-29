import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1) * Permutation(2, 3), Permutation(0, 2) * Permutation(1, 3)])
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
    "H_1: G is a group",
    "H_2: X is a set with at least two elements",
    "H_3: x is an element of X",
    "¬Q: Primitivity of the action is not equivalent to G_x being a maximal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_order(grp):
    try:
        return grp.order()
    except TypeError:
        return grp.order

def conditions(witness):
    try:
        if len(witness) == 3:
            G, X, x = witness
        elif len(witness) == 2:
            G, x = witness
            if hasattr(G, 'degree'):
                X = set(range(G.degree))
            else:
                X = None
        else:
            G, X, x = None, None, None
    except Exception:
        G, X, x = None, None, None

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X is a set with at least two elements
    try:
        h2 = len(X) >= 2 and set(X) == set(range(G.degree))
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # neg_Q: The action of G on X is primitive if and only if the stabilizer subgroup G_x is a maximal subgroup of G.
    try:
        is_prim = G.is_primitive()
        G_x = G.stabilizer(x)
        
        G_order = get_order(G)
        G_x_order = get_order(G_x)
        
        # Check if G_x is a maximal subgroup of G
        if G_x_order >= G_order:
            is_max = False
        else:
            is_max = True
            for g in G.generate():
                if g not in G_x:
                    K_gens = list(G_x.generators) + [g]
                    K = PermutationGroup(K_gens)
                    if get_order(K) < G_order:
                        is_max = False
                        break
                        
        # The conclusion fails if primitivity is NOT equivalent to G_x being maximal
        neg_q = (bool(is_prim) != bool(is_max))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]