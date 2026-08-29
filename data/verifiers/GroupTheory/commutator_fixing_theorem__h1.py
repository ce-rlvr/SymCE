import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: Standard algebra objects
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

def extract_all(witness):
    """Extracts G, X, g, h, x, and optionally action from the witness."""
    if isinstance(witness, dict):
        return (witness.get('G'), witness.get('X'), witness.get('g'), 
                witness.get('h'), witness.get('x'), witness.get('action'))
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            return witness + (None,)
        elif len(witness) >= 6:
            return witness[:6]
    return (getattr(witness, 'G', None), getattr(witness, 'X', None),
            getattr(witness, 'g', None), getattr(witness, 'h', None),
            getattr(witness, 'x', None), getattr(witness, 'action', None))

def apply_action(action, g, x):
    """Applies the group action of g on x."""
    if action is not None:
        return action(g, x)
    try:
        return g(x)
    except Exception:
        pass
    try:
        return g * x
    except Exception:
        pass
    try:
        return x * g
    except Exception:
        pass
    raise ValueError("No valid action found")

def conditions(witness) -> list[bool]:
    try:
        G, X, g, h, x, action = extract_all(witness)
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: g and h are elements of G
    try:
        h1 = (g in G) and (h in G)
    except Exception:
        h1 = False

    # H_2: x is an element of X
    try:
        h2 = (x in X)
    except Exception:
        h2 = False

    # H_3: x is fixed by g
    try:
        h3 = bool(apply_action(action, g, x) == x)
    except Exception:
        h3 = False

    # H_4: x is fixed by h
    try:
        h4 = bool(apply_action(action, h, x) == x)
    except Exception:
        h4 = False

    # ¬Q: x is not fixed by the commutator of g and h
    try:
        try:
            g_inv = g**-1
        except Exception:
            try:
                g_inv = g.inv()
            except Exception:
                g_inv = ~g
                
        try:
            h_inv = h**-1
        except Exception:
            try:
                h_inv = h.inv()
            except Exception:
                h_inv = ~h
                
        comm = g_inv * h_inv * g * h
        neg_q = bool(apply_action(action, comm, x) != x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: g and h are elements of G",
    "H_2: x is an element of X",
    "H_3: x is fixed by g",
    "H_4: x is fixed by h",
    "¬Q: x is not fixed by the commutator of g and h"
]

N_HYP = 4
NEG_Q_INDEX = 4