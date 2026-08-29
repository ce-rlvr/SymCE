import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                X = list(range(G.degree))
                action = lambda g, i: g(i)
            elif len(witness) == 4:
                G, X, action, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elms = G.elements
            elements = list(elms()) if callable(elms) else list(elms)
        else:
            elements = list(G)
            
    except Exception:
        return [False, False, False, False]

    try:
        if not X:
            h1 = False
        else:
            orbit = set()
            u = X[0]
            for g in elements:
                val = action(g, u)
                if val not in X:
                    h1 = False
                    break
                orbit.add(val)
            else:
                h1 = (set(orbit) == set(X))
    except Exception:
        h1 = False

    try:
        h2 = x in X
    except Exception:
        h2 = False

    try:
        _ = action(elements[0], X[0])
        h3 = True
    except Exception:
        h3 = False

    try:
        G_x = [g for g in elements if action(g, x) == x]
        
        orbits_Gx = set()
        for y in X:
            orbit = frozenset(action(h, y) for h in G_x)
            orbits_Gx.add(orbit)
        num_orbits_Gx = len(orbits_Gx)
        
        orbits_G_XxX = set()
        for u in X:
            for v in X:
                orbit = frozenset((action(g, u), action(g, v)) for g in elements)
                orbits_G_XxX.add(orbit)
        num_orbits_G_XxX = len(orbits_G_XxX)
        
        neg_q = (num_orbits_Gx != num_orbits_G_XxX)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: G is a group acting transitively on a set X",
    r"H_2: x is an element of X",
    r"H_3: G acts on the Cartesian product X \times X via the diagonal action",
    r"¬Q: The number of orbits of G_x on X is NOT equal to the number of orbits of G on X \times X"
]

N_HYP = 3
NEG_Q_INDEX = 3