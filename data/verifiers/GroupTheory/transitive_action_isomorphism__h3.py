import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        X = witness['X']
        x = witness['x']
        action = witness.get('action', lambda g, p: g(p))
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1_ok = hasattr(G, 'elements') and hasattr(G, 'identity')
    except Exception:
        h1_ok = False

    # H2: X is a set and G acts on X
    try:
        X_set = set(X)
        h2_ok = True
        
        # check closure
        for g in G.elements:
            for p in X_set:
                if action(g, p) not in X_set:
                    h2_ok = False
                    break
            if not h2_ok:
                break
        
        if h2_ok:
            # check identity
            id_g = G.identity
            for p in X_set:
                if action(id_g, p) != p:
                    h2_ok = False
                    break
                    
        if h2_ok:
            # check compatibility (allow either left or right action conventions)
            is_left = True
            is_right = True
            for g in G.elements:
                for h in G.elements:
                    gh = g * h
                    for p in X_set:
                        if action(g, action(h, p)) != action(gh, p):
                            is_left = False
                        if action(h, action(g, p)) != action(gh, p):
                            is_right = False
            if not (is_left or is_right):
                h2_ok = False
    except Exception:
        h2_ok = False

    # H3: x \in X
    try:
        h3_ok = x in X_set
    except Exception:
        h3_ok = False

    # H4: H = Stab(x)
    try:
        stab_elements = {g for g in G.elements if action(g, x) == x}
        if 'H' in witness:
            H = witness['H']
            if hasattr(H, 'elements'):
                h4_ok = set(H.elements) == stab_elements
            else:
                h4_ok = set(H) == stab_elements
        else:
            h4_ok = True
    except Exception:
        h4_ok = False

    # neg_Q: The map phi(gH) = g*x is not an isomorphism
    # Since phi is always injective, it is an isomorphism iff it is surjective.
    # The image of phi is exactly the orbit of x.
    try:
        orbit = {action(g, x) for g in G.elements}
        neg_q = orbit != X_set
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x in X",
    "H_4: H = Stab(x)",
    "¬Q: The map phi(gH) = g*x is not an isomorphism"
]

N_HYP = 4
NEG_Q_INDEX = 4