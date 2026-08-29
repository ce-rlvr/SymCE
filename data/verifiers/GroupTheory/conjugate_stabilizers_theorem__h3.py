import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_action(action, h, p):
    if callable(action):
        return action(h, p)
    elif isinstance(action, dict):
        return action[(h, p)]
    else:
        raise ValueError("action must be callable or dict")

def conditions(witness) -> list[bool]:
    try:
        G = witness.get('G')
        X = witness.get('X')
        x = witness.get('x')
        g = witness.get('g')
        y = witness.get('y')
        action = witness.get('action')
    except Exception:
        return [False] * 6

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements') or isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set
    try:
        h2 = hasattr(X, '__contains__') and hasattr(X, '__iter__')
    except Exception:
        h2 = False

    # H_3: x \in X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # H_4: g \in G
    try:
        h4 = g in list(G.elements)
    except Exception:
        h4 = False

    # H_5: y = g \cdot x
    try:
        h5 = (y == get_action(action, g, x))
    except Exception:
        h5 = False

    # ¬Q: Stab(y) != g Stab(x) g^{-1}
    try:
        elements = list(G.elements)
        
        stab_x = set()
        for h in elements:
            if get_action(action, h, x) == x:
                stab_x.add(h)
        
        stab_y = set()
        for h in elements:
            if get_action(action, h, y) == y:
                stab_y.add(h)
                
        g_stab_x_g_inv = set()
        try:
            g_inv = g**-1
        except Exception:
            g_inv = ~g
            
        for h in stab_x:
            g_stab_x_g_inv.add(g * h * g_inv)
            
        neg_q = (stab_y != g_stab_x_g_inv)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x \\in X",
    "H_4: g \\in G",
    "H_5: y = g \\cdot x",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5