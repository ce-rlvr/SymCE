import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (G, X, x, y) assuming a natural action g(pt),
    or (G, X, action, x, y) providing a custom action function.
    """
    try:
        if len(witness) == 4:
            G, X, x, y = witness
            action = lambda g, pt: g(pt)
        elif len(witness) == 5:
            G, X, action, x, y = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup) or hasattr(G, 'generate') or hasattr(G, 'elements'):
            h1 = True
        elif isinstance(G, (list, tuple, set)) and len(G) > 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = hasattr(X, '__contains__') and hasattr(X, '__iter__')
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # H4: y is an element of X
    try:
        h4 = y in X
    except Exception:
        h4 = False

    # neg_Q: For all g in G, Stab_G(y) != g * Stab_G(x) * g^{-1}
    try:
        if hasattr(G, 'generate'):
            raw_elements = list(G.generate())
        elif hasattr(G, 'elements'):
            raw_elements = list(G.elements)
        else:
            raw_elements = list(G)
            
        # Ensure unique elements
        elements = []
        for e in raw_elements:
            if e not in elements:
                elements.append(e)
                
        stab_x = []
        for h in elements:
            if action(h, x) == x:
                stab_x.append(h)
                
        stab_y = []
        for h in elements:
            if action(h, y) == y:
                stab_y.append(h)
                
        neg_q = True
        for g in elements:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
                
            conj_stab_x = []
            for h in stab_x:
                conj_stab_x.append(g * h * g_inv)
                
            # Check if conj_stab_x and stab_y contain the same elements
            if len(conj_stab_x) == len(stab_y):
                all_in = True
                for item in conj_stab_x:
                    if item not in stab_y:
                        all_in = False
                        break
                if all_in:
                    # Found a g such that Stab_G(y) == g * Stab_G(x) * g^{-1}
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "H_4: y is an element of X",
    "¬Q: For all g in G, Stab_G(y) != g * Stab_G(x) * g^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4