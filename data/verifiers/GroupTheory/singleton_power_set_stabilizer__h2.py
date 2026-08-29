import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = DihedralGroup(2) # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    The witness can be a tuple (G, X, action, x) or (G, X, x) where action defaults to g(y).
    """
    try:
        if len(witness) == 4:
            G, X, action, x = witness
        elif len(witness) == 3:
            G, X, x = witness
            action = lambda g, y: g(y)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        elements = list(G.elements)
        identity = G.identity
        
        h1_ok = True
        # Check identity acts trivially
        for y in X:
            if action(identity, y) != y:
                h1_ok = False
                break
                
        # Check closure of the action
        if h1_ok:
            for g in elements:
                for y in X:
                    found = False
                    for item in X:
                        if action(g, y) == item:
                            found = True
                            break
                    if not found:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
                    
        # Check compatibility (left or right action)
        if h1_ok:
            is_left = True
            is_right = True
            for g1 in elements:
                for g2 in elements:
                    for y in X:
                        a12 = action(g1 * g2, y)
                        if a12 != action(g1, action(g2, y)):
                            is_left = False
                        if a12 != action(g2, action(g1, y)):
                            is_right = False
            h1_ok = is_left or is_right
    except Exception:
        h1_ok = False

    # H_2: G acts on P(X) via the induced action
    # This is a definitional property that holds if H1 holds.
    h2_ok = h1_ok

    # H_3: x is an element of X
    try:
        h3_ok = False
        for y in X:
            if x == y:
                h3_ok = True
                break
    except Exception:
        h3_ok = False

    # ¬Q: The stabilizer of the singleton set {x} in the action on P(X) 
    # is NOT equal to the stabilizer of x in the action on X.
    try:
        stab_singleton = []
        stab_x = []
        for g in elements:
            # Action on the singleton set {x}
            S = [x]
            g_S = [action(g, s) for s in S]
            
            # Check if g_S equals S as sets
            is_equal = True
            for item in g_S:
                found = False
                for s in S:
                    if item == s:
                        found = True
                        break
                if not found:
                    is_equal = False
                    break
            for s in S:
                found = False
                for item in g_S:
                    if s == item:
                        found = True
                        break
                if not found:
                    is_equal = False
                    break
                    
            if is_equal:
                stab_singleton.append(g)
            
            # Action on the element x
            if action(g, x) == x:
                stab_x.append(g)
                
        neg_q = False
        if len(stab_singleton) != len(stab_x):
            neg_q = True
        else:
            for g in stab_singleton:
                if g not in stab_x:
                    neg_q = True
                    break
            for g in stab_x:
                if g not in stab_singleton:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G acts on P(X) via the induced action",
    "H_3: x is an element of X",
    "¬Q: The stabilizer of {x} in P(X) is not equal to the stabilizer of x in X"
]

N_HYP = 3
NEG_Q_INDEX = 3