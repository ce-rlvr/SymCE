import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, H, x, y, f = witness
    except Exception:
        return [False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x and y are elements of G
    try:
        h2 = (x in G.elements) and (y in G.elements)
    except Exception:
        h2 = False

    # neg_Q: f(x) = f(y) iff x^{-1}y \in ker(f) is FALSE
    try:
        # Normalize f to a dictionary mapping
        if isinstance(f, dict):
            f_map = f
        elif callable(f):
            f_map = {g: f(g) for g in G.elements}
        elif isinstance(f, (list, tuple)):
            f_map = dict(f)
        else:
            f_map = None

        # Validate that f is a well-defined function from G to H
        if f_map is None:
            neg_q = False
        elif not all(g in f_map for g in G.elements):
            neg_q = False
        elif not all(f_map[g] in H.elements for g in G.elements):
            neg_q = False
        else:
            e_H = H.identity
            ker_f = {g for g in G.elements if f_map[g] == e_H}
            
            x_inv_y = (~x) * y
            
            cond1 = (f_map[x] == f_map[y])
            cond2 = (x_inv_y in ker_f)
            
            # The conclusion fails if the two conditions are not equivalent
            neg_q = bool(cond1 != cond2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: x and y are elements of G",
    "¬Q: f(x) = f(y) is not equivalent to x^{-1}y in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2