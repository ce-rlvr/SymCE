import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def get_action(action, g, x):
    if callable(action):
        return action(g, x)
    elif isinstance(action, dict):
        if (g, x) in action:
            return action[(g, x)]
        elif g in action and isinstance(action[g], dict) and x in action[g]:
            return action[g][x]
    raise ValueError("Action not found")

def conditions(witness):
    """
    witness is expected to be a tuple: (G, X, action)
    where:
      - G is a SymPy PermutationGroup
      - X is an iterable representing the set
      - action is a callable action(g, x) or a dictionary mapping (g, x) to an element in X
    """
    try:
        G, X, action = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is an abelian group
    try:
        if hasattr(G, 'is_abelian'):
            h1 = bool(G.is_abelian)
            elements = list(G.elements)
            identity = G.identity
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a non-empty set
    try:
        X_list = []
        for x in X:
            if x not in X_list:
                X_list.append(x)
        h2 = len(X_list) > 0
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = True
        if h1 and h2:
            # Check closure
            for g in elements:
                for x in X_list:
                    res = get_action(action, g, x)
                    if res not in X_list:
                        h3 = False
                        break
                if not h3: break
            
            # Check identity
            if h3:
                for x in X_list:
                    if get_action(action, identity, x) != x:
                        h3 = False
                        break
                        
            # Check compatibility
            if h3:
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for x in X_list:
                            res1 = get_action(action, gh, x)
                            res2 = get_action(action, g, get_action(action, h, x))
                            res3 = get_action(action, h, get_action(action, g, x))
                            # Allow both left and right action conventions
                            if res1 != res2 and res1 != res3:
                                h3 = False
                                break
                        if not h3: break
                    if not h3: break
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: The action of G on X is transitive
    try:
        h4 = True
        if h1 and h2 and h3:
            for x in X_list:
                orbit = []
                for g in elements:
                    res = get_action(action, g, x)
                    if res not in orbit:
                        orbit.append(res)
                if len(orbit) != len(X_list) or not all(y in orbit for y in X_list):
                    h4 = False
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    # ¬Q: The action of G on X is not regular (i.e., there is a non-trivial stabilizer)
    try:
        neg_q = False
        if h1 and h2 and h3:
            for x in X_list:
                for g in elements:
                    if g != identity:
                        if get_action(action, g, x) == x:
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: X is a non-empty set",
    "H_3: G acts on X",
    "H_4: The action of G on X is transitive",
    "¬Q: The action of G on X is not regular"
]

N_HYP = 4
NEG_Q_INDEX = 4