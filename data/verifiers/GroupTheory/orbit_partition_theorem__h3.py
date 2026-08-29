import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        G, X, action = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple)) and len(X) > 0
    except Exception:
        h2 = False

    # H3: action is a function G x X -> X
    try:
        if callable(action):
            act = action
        elif isinstance(action, dict):
            act = lambda g, x: action[(g, x)]
        else:
            act = None
            
        if act is not None:
            h3 = True
            elements_G = list(G.elements) if hasattr(G, 'elements') else list(G)
            elements_X = []
            for x in X:
                if x not in elements_X:
                    elements_X.append(x)
            for g in elements_G:
                for x in elements_X:
                    y = act(g, x)
                    if y not in elements_X:
                        h3 = False
                        break
                if not h3:
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: \sim is NOT an equivalence relation
    try:
        if callable(action):
            act = action
        elif isinstance(action, dict):
            act = lambda g, x: action[(g, x)]
        else:
            return [h1, h2, h3, False]

        elements_G = list(G.elements) if hasattr(G, 'elements') else list(G)
        elements_X = []
        for x in X:
            if x not in elements_X:
                elements_X.append(x)
        
        sim = {i: set() for i in range(len(elements_X))}
        for i, x in enumerate(elements_X):
            for g in elements_G:
                y = act(g, x)
                try:
                    j = elements_X.index(y)
                    sim[i].add(j)
                except ValueError:
                    pass
                    
        is_equiv = True
        # Reflexive
        for i in range(len(elements_X)):
            if i not in sim[i]:
                is_equiv = False
                break
                
        # Symmetric
        if is_equiv:
            for i in range(len(elements_X)):
                for j in sim[i]:
                    if i not in sim[j]:
                        is_equiv = False
                        break
                if not is_equiv:
                    break
                    
        # Transitive
        if is_equiv:
            for i in range(len(elements_X)):
                for j in sim[i]:
                    for k in sim[j]:
                        if k not in sim[i]:
                            is_equiv = False
                            break
                    if not is_equiv:
                        break
                if not is_equiv:
                    break
                    
        neg_q = not is_equiv
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: A relation ~ is defined via an operation G x X -> X",
    "¬Q: ~ is not an equivalence relation"
]

N_HYP = 3
NEG_Q_INDEX = 3