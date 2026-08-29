import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.combinatorics.named_groups import AbelianGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "¬Q: The cardinality of the orbit of x does not divide the order of the group G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, X, x, action = witness
        elif len(witness) == 3:
            G, X, x = witness
            if isinstance(G, PermutationGroup):
                action = lambda g, y: g(y)
            else:
                action = lambda g, y: g * y
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    h1 = False
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            elements = list(G)
            if len(elements) > 0:
                closed = True
                for a in elements:
                    for b in elements:
                        if a * b not in elements:
                            closed = False
                            break
                    if not closed: break
                
                if closed:
                    has_id = False
                    for e in elements:
                        if all(e * a == a and a * e == a for a in elements):
                            has_id = True
                            break
                    
                    if has_id:
                        inv_ok = True
                        for a in elements:
                            has_inv = False
                            for b in elements:
                                if a * b == b * a and all((a * b) * c == c for c in elements):
                                    has_inv = True
                                    break
                            if not has_inv:
                                inv_ok = False
                                break
                        if inv_ok:
                            h1 = True
    except Exception:
        h1 = False

    # H_2: X is a set
    h2 = False
    try:
        if isinstance(X, (set, frozenset)):
            h2 = True
        elif isinstance(X, (list, tuple)):
            h2 = True
            for i in range(len(X)):
                if X[i] in X[:i]:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: x is an element of X
    h3 = False
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the orbit of x does not divide the order of the group G
    neg_q = False
    try:
        if isinstance(G, PermutationGroup):
            elements = list(G.generate())
        else:
            elements = list(G)
        
        order_G = len(elements)
        
        if callable(action):
            orbit = []
            for g in elements:
                res = action(g, x)
                if res not in orbit:
                    orbit.append(res)
            orbit_size = len(orbit)
        elif isinstance(action, dict):
            orbit = []
            for g in elements:
                res = action[(g, x)]
                if res not in orbit:
                    orbit.append(res)
            orbit_size = len(orbit)
        else:
            orbit = []
            for res in action:
                if res not in orbit:
                    orbit.append(res)
            orbit_size = len(orbit)
            
        if orbit_size > 0:
            if order_G % orbit_size != 0:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]