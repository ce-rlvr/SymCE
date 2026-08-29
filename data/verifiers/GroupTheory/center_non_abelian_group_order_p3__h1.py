import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness):
    # H_1: G is a non-abelian group
    try:
        # Check if it has group-like properties to avoid false positives on symbols
        if not hasattr(witness, 'order'):
            h1 = False
        else:
            h1 = bool(not witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: The order of G is p^3
    try:
        n = int(witness.order())
        p = int(round(n**(1/3)))
        h2 = bool(p**3 == n)
    except Exception:
        h2 = False

    # ¬Q: The center Z(G) does not have order exactly p
    try:
        n = int(witness.order())
        p = int(round(n**(1/3)))
        if p**3 == n:
            try:
                c_order = int(witness.center().order())
            except AttributeError:
                elements = list(witness.elements)
                c_order = sum(1 for g in elements if all(g*h == h*g for h in elements))
            neg_q = bool(c_order != p)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group",
    "H_2: The order of G is p^3",
    "¬Q: The center Z(G) does not have order exactly p"
]

N_HYP = 2
NEG_Q_INDEX = 2