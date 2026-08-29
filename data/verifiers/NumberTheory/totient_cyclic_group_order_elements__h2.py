import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
import math
import itertools
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, d, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite cyclic group
    try:
        order = G.order()
        if order > 2000:
            h1 = False
        else:
            elements = list(G.elements) if hasattr(G, 'elements') else list(G.generate())
            h1 = any(g.order() == order for g in elements)
    except Exception:
        h1 = False

    # H_2: d is a positive integer
    try:
        h2 = int(d) == d and d > 0
    except Exception:
        h2 = False

    # H_3: d divides n
    try:
        h3 = int(n) == n and n % d == 0
    except Exception:
        h3 = False

    # ¬Q: The number of elements in G of exact order d is not equal to \phi(d)
    try:
        elements = list(G.elements) if hasattr(G, 'elements') else list(G.generate())
        elements_of_order_d = sum(1 for g in elements if g.order() == d)
        neg_q = elements_of_order_d != totient(d)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: d is a positive integer",
    "H_3: d divides n",
    "¬Q: The number of elements in G of exact order d is not equal to phi(d)"
]

N_HYP = 3
NEG_Q_INDEX = 3