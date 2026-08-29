import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def in_G(G, x):
    try:
        if hasattr(G, 'contains'):
            return G.contains(x)
    except Exception:
        pass
    try:
        if hasattr(G, 'elements'):
            return x in list(G.elements)
    except Exception:
        pass
    try:
        return x in G
    except Exception:
        return False

def are_conjugate(G, x, y):
    try:
        elements = G.elements if hasattr(G, 'elements') else G
        for g in elements:
            try:
                ginv = g**-1
            except Exception:
                try:
                    ginv = g.inv()
                except Exception:
                    try:
                        ginv = ~g
                    except Exception:
                        continue
            
            try:
                if g * x * ginv == y: return True
            except Exception:
                pass
            try:
                if ginv * x * g == y: return True
            except Exception:
                pass
        return False
    except Exception:
        return False

def is_integer(n):
    if isinstance(n, int):
        return True
    try:
        if hasattr(n, 'is_integer') and n.is_integer:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        
        # Heuristic to unpack (G, x, y, n) or (x, y, G, n)
        if is_integer(witness[3]):
            if hasattr(witness[0], 'elements') or isinstance(witness[0], (list, set, tuple)):
                G, x, y, n = witness
            elif hasattr(witness[2], 'elements') or isinstance(witness[2], (list, set, tuple)):
                x, y, G, n = witness
            else:
                G, x, y, n = witness
        else:
            G, x, y, n = witness
            
    except Exception:
        return [False, False, False, False]
    
    # H_1: x and y are elements of G
    try:
        h1 = bool(in_G(G, x) and in_G(G, y))
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = bool(are_conjugate(G, x, y))
    except Exception:
        h2 = False

    # H_3: n is an integer
    try:
        h3 = bool(is_integer(n))
    except Exception:
        h3 = False

    # ¬Q: x^n and y^n are NOT conjugate in G
    try:
        xn = x**n
        yn = y**n
        neg_q = not are_conjugate(G, xn, yn)
    except Exception:
        # If x^n or y^n is undefined (e.g., negative power of non-invertible element),
        # the conclusion "x^n and y^n are conjugate" is false.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "H_3: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3