import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
            x = witness.get('x')
            H = witness.get('H')
        else:
            G, X, action, x, H = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'elements')
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
        X_set = set(X)
    except Exception:
        h2 = False

    # H3: G acts transitively on X
    h3 = False
    try:
        if h1 and h2 and X_set:
            elements = list(G.elements)
            a = list(X_set)[0]
            orbit_a = set()
            for g in elements:
                orbit_a.add(action(g, a))
            
            id_g = next((g for g in elements if g * g == g), None)
            
            if orbit_a == X_set and id_g is not None:
                valid_id = True
                for y in X_set:
                    if action(id_g, y) != y:
                        valid_id = False
                        break
                if valid_id:
                    is_left = True
                    is_right = True
                    for g in elements:
                        for h in elements:
                            gh = g * h
                            for y in X_set:
                                if is_left and action(g, action(h, y)) != action(gh, y):
                                    is_left = False
                                if is_right and action(h, action(g, y)) != action(gh, y):
                                    is_right = False
                            if not is_left and not is_right:
                                break
                        if not is_left and not is_right:
                            break
                    h3 = is_left or is_right
    except Exception:
        h3 = False

    # H4: H = Stab(x)
    h4 = False
    try:
        if h1:
            elements = list(G.elements)
            stab_x = set()
            for g in elements:
                if action(g, x) == x:
                    stab_x.add(g)
            
            if isinstance(H, PermutationGroup) or hasattr(H, 'elements'):
                H_set = set(H.elements)
            else:
                H_set = set(H)
                
            h4 = (H_set == stab_x)
    except Exception:
        h4 = False

    # neg_Q: The map phi(gH) = g.x is NOT a G-set isomorphism to X
    neg_q = False
    try:
        if h1 and h2:
            elements = list(G.elements)
            orbit_x = set()
            for g in elements:
                orbit_x.add(action(g, x))
            
            # The map phi is a bijection to X iff orbit_x == X_set
            if orbit_x != X_set:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts transitively on X",
    "H_4: H = Stab(x)",
    "¬Q: The map phi(gH) = g.x is not a G-set isomorphism from G/H to X"
]

N_HYP = 4
NEG_Q_INDEX = 4