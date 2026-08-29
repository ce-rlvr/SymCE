import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros, Matrix

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
        G, g, h = witness
    except Exception:
        return [False] * 7

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or getattr(G, 'is_group', False) or hasattr(G, 'elements') or isinstance(G, (list, set, tuple))
    except Exception:
        h1 = False

    # H_2: g is an element of G
    try:
        if isinstance(G, (list, set, tuple)):
            h2 = g in G
        else:
            h2 = g in G.elements if hasattr(G, 'elements') else g in G
    except Exception:
        h2 = False

    # H_3: g and h commute (gh = hg)
    try:
        h3 = bool(g * h == h * g)
    except Exception:
        h3 = False

    # H_4: the order of g is a finite integer m
    try:
        if hasattr(g, 'order'):
            m = int(g.order())
        else:
            # Fallback for matrices or other objects without an order method
            m = -1
            identity = g ** 0
            for k in range(1, 1000):
                if g ** k == identity:
                    m = k
                    break
        h4 = (m > 0)
    except Exception:
        h4 = False
        m = -1

    # H_5: the order of h is a finite integer n
    try:
        if hasattr(h, 'order'):
            n = int(h.order())
        else:
            n = -1
            identity = h ** 0
            for k in range(1, 1000):
                if h ** k == identity:
                    n = k
                    break
        h5 = (n > 0)
    except Exception:
        h5 = False
        n = -1

    # H_6: gcd(m, n) = 1
    try:
        h6 = bool(math.gcd(m, n) == 1)
    except Exception:
        h6 = False

    # ¬Q: The order of the product gh is NOT exactly m * n
    try:
        gh = g * h
        if hasattr(gh, 'order'):
            gh_order = int(gh.order())
        else:
            gh_order = -1
            identity = gh ** 0
            for k in range(1, 2000):
                if gh ** k == identity:
                    gh_order = k
                    break
        neg_q = bool(gh_order != m * n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: g and h commute (gh = hg)",
    "H_4: the order of g is a finite integer m",
    "H_5: the order of h is a finite integer n",
    "H_6: gcd(m, n) = 1",
    "¬Q: The order of the product gh is NOT exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6