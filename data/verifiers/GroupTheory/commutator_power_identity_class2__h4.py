import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = False
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
        elif hasattr(G, 'generators') or hasattr(G, 'elements'):
            h1 = True
        elif isinstance(G, (list, tuple, set)):
            h1 = True
    except Exception:
        h1 = False

    # H_2: G is nilpotent of class at most 2
    try:
        h2 = False
        if hasattr(G, 'nilpotency_class'):
            class_val = G.nilpotency_class
            if callable(class_val):
                class_val = class_val()
            h2 = (class_val <= 2)
        else:
            # Fallback: check if all commutators are central
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            h2 = True
            for a in elements:
                for b in elements:
                    c_ab = (a**-1) * (b**-1) * a * b
                    for c in elements:
                        if c_ab * c != c * c_ab:
                            h2 = False
                            break
                    if not h2:
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: x and y are elements of G
    try:
        h3 = False
        if hasattr(G, 'contains'):
            h3 = bool(G.contains(x) and G.contains(y))
        elif hasattr(G, '__contains__'):
            h3 = bool(x in G and y in G)
        else:
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            h3 = bool(x in elements and y in elements)
    except Exception:
        h3 = False

    # neg_Q: (xy)^n != x^n y^n [y, x]^{n(n-1)/2}
    try:
        lhs = (x * y)**n
        power = n * (n - 1) // 2
        comm_yx = (y**-1) * (x**-1) * y * x
        rhs = (x**n) * (y**n) * (comm_yx**power)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: G is nilpotent of class at most 2", "H_3: x and y are elements of G", "not Q: conclusion fails"]
N_HYP = 3
NEG_Q_INDEX = 3