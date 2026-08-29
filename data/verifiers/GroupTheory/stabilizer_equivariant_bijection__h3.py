import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
    try:
        G, X, Y, action_X, action_Y, x, phi = witness
    except Exception:
        return [False, False, False, False]

    def apply_action(action, g, elem):
        if callable(action):
            return action(g, elem)
        else:
            return action[(g, elem)]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: X and Y are sets equipped with actions by G
    try:
        h2 = True
        if not isinstance(X, (list, set, tuple)) or not isinstance(Y, (list, set, tuple)):
            h2 = False
        elif not h1 or G.order() > 100:
            h2 = False
        else:
            if hasattr(G, 'elements'):
                elements_G = list(G.elements)
            else:
                elements_G = list(G.generate())
            id_G = G.identity
            
            # Check action_X
            for g in elements_G:
                for elem in X:
                    if apply_action(action_X, g, elem) not in X:
                        h2 = False
                        break
                if not h2: break
            if h2:
                for elem in X:
                    if apply_action(action_X, id_G, elem) != elem:
                        h2 = False
                        break
            if h2:
                is_left = True
                is_right = True
                for g in elements_G:
                    for h in elements_G:
                        for elem in X:
                            gh_elem = apply_action(action_X, g * h, elem)
                            if gh_elem != apply_action(action_X, g, apply_action(action_X, h, elem)):
                                is_left = False
                            if gh_elem != apply_action(action_X, h, apply_action(action_X, g, elem)):
                                is_right = False
                if not (is_left or is_right):
                    h2 = False
            
            # Check action_Y
            if h2:
                for g in elements_G:
                    for elem in Y:
                        if apply_action(action_Y, g, elem) not in Y:
                            h2 = False
                            break
                    if not h2: break
            if h2:
                for elem in Y:
                    if apply_action(action_Y, id_G, elem) != elem:
                        h2 = False
                        break
            if h2:
                is_left = True
                is_right = True
                for g in elements_G:
                    for h in elements_G:
                        for elem in Y:
                            gh_elem = apply_action(action_Y, g * h, elem)
                            if gh_elem != apply_action(action_Y, g, apply_action(action_Y, h, elem)):
                                is_left = False
                            if gh_elem != apply_action(action_Y, h, apply_action(action_Y, g, elem)):
                                is_right = False
                if not (is_left or is_right):
                    h2 = False
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # neg_Q: The point stabilizer G_x is NOT equal to the point stabilizer G_{\phi(x)}
    try:
        if callable(phi):
            phi_x = phi(x)
        else:
            phi_x = phi[x]
            
        if phi_x not in Y:
            neg_q = False
        else:
            G_x = set()
            G_phi_x = set()
            if hasattr(G, 'elements'):
                elements_G = list(G.elements)
            else:
                elements_G = list(G.generate())
                
            for g in elements_G:
                if apply_action(action_X, g, x) == x:
                    G_x.add(g)
                if apply_action(action_Y, g, phi_x) == phi_x:
                    G_phi_x.add(g)
            neg_q = G_x != G_phi_x
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are sets equipped with actions by G",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the point stabilizer G_{\phi(x)}"
]

N_HYP = 3
NEG_Q_INDEX = 3