import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    return list(G)

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]
        
    try:
        G_elems = get_elements(G)
    except Exception:
        return [False, False, False]

    # H_1: x and y are elements of G
    try:
        h1 = any(x == e for e in G_elems) and any(y == e for e in G_elems)
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = False
        for g in G_elems:
            if g * x * g**-1 == y:
                h2 = True
                break
    except Exception:
        h2 = False

    # ¬Q: x^{-1} and y^{-1} are not conjugate in G
    try:
        x_inv = x**-1
        y_inv = y**-1
        neg_q = True
        for g in G_elems:
            if g * x_inv * g**-1 == y_inv:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "¬Q: x^{-1} and y^{-1} are not conjugate in G"
]

N_HYP = 2
NEG_Q_INDEX = 2