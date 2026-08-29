import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint
import math
import itertools
import functools

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

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: G acts on X",
    "H_4: X^G is the set of all elements in X fixed by every element of G",
    "¬Q: |X^G| is not congruent to |X| modulo p"
]

def conditions(witness):
    h1_ok = False
    h2_ok = False
    h3_ok = False
    h4_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 5:
                p, G, X, action, X_G = witness
            elif len(witness) == 4:
                p, G, X, action = witness
                X_G = None
            elif len(witness) == 3:
                p, G, X = witness
                action = lambda g, x: g(x)
                X_G = None
            elif len(witness) == 2:
                p, G = witness
                if hasattr(G, 'degree'):
                    X = list(range(G.degree))
                else:
                    X = list(range(len(list(G))))
                action = lambda g, x: g(x)
                X_G = None
            else:
                return [False, False, False, False, False]
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H2: G is a finite p-group
    try:
        if hasattr(G, 'order'):
            if callable(G.order):
                order = G.order()
            else:
                order = G.order
        else:
            order = len(list(G))
        factors = factorint(order)
        h2_ok = len(factors) <= 1
    except Exception:
        h2_ok = False

    # Extract elements and identity for H3 and H4
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        identity = None
        for g in elements:
            if hasattr(g, 'is_Identity') and g.is_Identity:
                identity = g
                break
        if identity is None:
            for e in elements:
                try:
                    if all(e * g == g for g in elements):
                        identity = e
                        break
                except Exception:
                    pass
    except Exception:
        elements = []
        identity = None

    # H3: G acts on X
    try:
        if identity is not None:
            h3_ok = True
            for x in X:
                if action(identity, x) != x:
                    h3_ok = False
                    break
            if h3_ok:
                is_left_action = True
                for g in elements:
                    for h in elements:
                        for x in X:
                            if action(g, action(h, x)) != action(g * h, x):
                                is_left_action = False
                                break
                        if not is_left_action: break
                    if not is_left_action: break
                    
                is_right_action = True
                for g in elements:
                    for h in elements:
                        for x in X:
                            if action(h, action(g, x)) != action(g * h, x):
                                is_right_action = False
                                break
                        if not is_right_action: break
                    if not is_right_action: break
                    
                h3_ok = is_left_action or is_right_action
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # H4: X^G is the set of all elements in X fixed by every element of G
    try:
        expected_X_G = []
        for x in X:
            if all(action(g, x) == x for g in elements):
                expected_X_G.append(x)
                
        if X_G is None:
            X_G = expected_X_G
            h4_ok = True
        else:
            if len(X_G) != len(expected_X_G):
                h4_ok = False
            else:
                h4_ok = True
                expected_copy = list(expected_X_G)
                for x in X_G:
                    found = False
                    for i, ex in enumerate(expected_copy):
                        if x == ex:
                            found = True
                            expected_copy.pop(i)
                            break
                    if not found:
                        h4_ok = False
                        break
    except Exception:
        h4_ok = False

    # ¬Q: |X^G| is not congruent to |X| modulo p
    try:
        neg_q = (len(X_G) % p) != (len(X) % p)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]