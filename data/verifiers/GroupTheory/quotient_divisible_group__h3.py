import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Final Result: Verifier Module for Quotient of a Divisible Group
# Initial logic and parameters are validated.
# Standard processing applied.

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

def _is_abelian(g):
    if hasattr(g, 'is_abelian'):
        val = g.is_abelian
        return val() if callable(val) else val
    try:
        elements = list(g.elements)
        for a in elements:
            for b in elements:
                if a * b != b * a:
                    return False
        return True
    except Exception:
        return False

def _is_divisible(g):
    if hasattr(g, 'is_divisible'):
        val = g.is_divisible
        return val() if callable(val) else val
    try:
        elements = list(g.elements)
        return len(elements) == 1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(_is_abelian(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(_is_divisible(G))
    except Exception:
        h2 = False

    try:
        if hasattr(G, 'quotient'):
            Q_grp = G.quotient(H)
        else:
            Q_grp = G / H
        
        q_ok = bool(_is_abelian(Q_grp) and _is_divisible(Q_grp))
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is a divisible group",
    "¬Q: The quotient group G/H is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2