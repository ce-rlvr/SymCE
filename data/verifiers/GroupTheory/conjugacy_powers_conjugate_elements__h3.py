import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import sympy.abc
import math
import itertools
import functools
import z3

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
        return [False, False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x is an element of G
    try:
        h2 = h1 and bool(x in G)
    except Exception:
        h2 = False
        
    # H_3: y is an element of G
    try:
        h3 = h1 and bool(y in G)
    except Exception:
        h3 = False
        
    # H_4: n is an integer
    try:
        h4 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h4 = False
        
    # ¬Q: x^n and y^n are not conjugate in G
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        else:
            xn = x**n
            yn = y**n
            is_conj = False
            # Check if there exists g in G such that g * xn * g^-1 == yn
            for g in G.generate():
                if g * xn * (g**-1) == yn:
                    is_conj = True
                    break
            neg_q = not is_conj
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 4
NEG_Q_INDEX = 4