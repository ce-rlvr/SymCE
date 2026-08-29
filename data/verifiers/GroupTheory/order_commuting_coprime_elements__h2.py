import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
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
        G, g, h, m, n = witness
    except Exception:
        return [False] * 7

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'is_group') or hasattr(G, 'generators') or hasattr(G, 'elements')
    except Exception:
        h1 = False

    # H_2: h is an element of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(h))
        else:
            h2 = bool(h in G)
    except Exception:
        h2 = False

    # H_3: g and h commute (gh = hg)
    try:
        h3 = bool(g * h == h * g)
    except Exception:
        h3 = False

    # H_4: the order of g is a finite integer m
    try:
        if not isinstance(m, int):
            h4 = False
        else:
            order_attr = getattr(g, 'order', None)
            if callable(order_attr):
                h4 = bool(order_attr() == m)
            elif order_attr is not None:
                h4 = bool(order_attr == m)
            else:
                h4 = False
    except Exception:
        h4 = False

    # H_5: the order of h is a finite integer n
    try:
        if not isinstance(n, int):
            h5 = False
        else:
            order_attr = getattr(h, 'order', None)
            if callable(order_attr):
                h5 = bool(order_attr() == n)
            elif order_attr is not None:
                h5 = bool(order_attr == n)
            else:
                h5 = False
    except Exception:
        h5 = False

    # H_6: gcd(m, n) = 1
    try:
        h6 = bool(math.gcd(m, n) == 1)
    except Exception:
        h6 = False

    # ¬Q: The order of the product gh is not exactly m * n
    try:
        gh = g * h
        order_attr = getattr(gh, 'order', None)
        if callable(order_attr):
            gh_order = order_attr()
        elif order_attr is not None:
            gh_order = order_attr
        else:
            gh_order = None
        
        if gh_order is not None:
            neg_q = bool(gh_order != m * n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: h is an element of G",
    "H_3: g and h commute (gh = hg)",
    "H_4: the order of g is a finite integer m",
    "H_5: the order of h is a finite integer n",
    "H_6: gcd(m, n) = 1",
    "¬Q: The order of the product gh is not exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6