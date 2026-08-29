import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness['G']
            x = witness['x']
            y = witness['y']
            g = witness.get('g', x * y)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, x, y = witness
                g = x * y
            elif len(witness) == 4:
                G, x, y, g = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: Let e be the identity element of G
    try:
        e = x**0
        h1 = bool(e in G)
    except Exception:
        h1 = False

    # H_2: Let x and y be elements of G such that x^2 = e and y^2 = e
    try:
        h2 = bool((x in G) and (y in G) and (x**2 == e) and (y**2 == e))
    except Exception:
        h2 = False

    # H_3: Let g = xy
    try:
        h3 = bool(g == x * y)
    except Exception:
        h3 = False

    # ¬Q: The element g is NOT conjugate to its inverse g^-1 in G
    try:
        g_inv = g**-1
        elements = list(G)
        is_conjugate = False
        for h in elements:
            try:
                if h * g * h**-1 == g_inv:
                    is_conjugate = True
                    break
            except Exception:
                pass
        neg_q = not is_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: e is the identity element of G",
    "H_2: x and y are elements of G such that x^2 = e and y^2 = e",
    "H_3: g = xy",
    "¬Q: g is not conjugate to its inverse g^-1 in G"
]

N_HYP = 3
NEG_Q_INDEX = 3