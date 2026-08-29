import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def are_conjugate(G, a, b):
    try:
        elements = G.elements
    except AttributeError:
        elements = G
        
    for g in elements:
        is_conj = False
        # Try permutation inverse syntax
        try:
            if g * a * ~g == b:
                is_conj = True
        except Exception:
            pass
            
        # Try general/matrix inverse syntax
        if not is_conj:
            try:
                if g * a * (g**-1) == b:
                    is_conj = True
            except Exception:
                pass
                
        if is_conj:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
            n = witness.get('n')
        else:
            G, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: x and y are elements of G
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(x) and G.contains(y))
        else:
            try:
                elements = G.elements
            except AttributeError:
                elements = G
            h1 = bool((x in elements) and (y in elements))
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = bool(are_conjugate(G, x, y))
    except Exception:
        h2 = False

    # H_3: n is an integer
    try:
        h3 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h3 = False

    # ¬Q: x^n and y^n are NOT conjugate in G
    try:
        xn = x**n
        yn = y**n
        neg_q = not are_conjugate(G, xn, yn)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "H_3: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3