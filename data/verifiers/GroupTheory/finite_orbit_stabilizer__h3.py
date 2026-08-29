import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to provide the group G, the set X, the element x, 
    and an action function action(g, y).
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            x = witness['x']
            action = witness['action']
        elif isinstance(witness, (tuple, list)):
            G = witness[0]
            X = witness[1]
            x = witness[2]
            action = witness[3]
        else:
            G = witness.G
            X = witness.X
            x = witness.x
            action = witness.action
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        elems = G.elements() if callable(getattr(G, 'elements', None)) else G.elements
        elements_list = list(elems)
        order = G.order() if callable(getattr(G, 'order', None)) else G.order
        h1 = (order == len(elements_list)) and (order > 0)
    except Exception:
        h1 = False

    # H_2: X is a set (or list/tuple representing a set)
    try:
        h2 = isinstance(X, (set, list, tuple))
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|
    try:
        elems = G.elements() if callable(getattr(G, 'elements', None)) else G.elements
        orb = []
        stab_count = 0
        for g in list(elems):
            res = action(g, x)
            if res not in orb:
                orb.append(res)
            if res == x:
                stab_count += 1
        
        order = G.order() if callable(getattr(G, 'order', None)) else G.order
        neg_q = order != len(orb) * stab_count
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3