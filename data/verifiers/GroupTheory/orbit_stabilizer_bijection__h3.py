import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        G, X, x, action = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple, sympy.Set))
    except Exception:
        h2 = False
        
    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False
        
    # ¬Q: The map g*Stab_G(x) |-> g.x is not a bijection
    try:
        # Compute Stab_G(x)
        stab = set()
        for g in G.elements:
            if callable(action):
                val = action(g, x)
            else:
                val = action[(g, x)]
                
            if val == x:
                stab.add(g)
                
        # Construct the relation R defined by g*Stab_G(x) |-> g.x
        R = set()
        for g in G.elements:
            coset = frozenset(g * h for h in stab)
            if callable(action):
                val = action(g, x)
            else:
                val = action[(g, x)]
            R.add((coset, val))
            
        # Projections of the relation
        C = {coset for coset, val in R}
        Orb = {val for coset, val in R}
        
        # A relation is a bijection iff it is a well-defined function and injective
        # (Surjectivity is guaranteed by construction since Orb is the image)
        is_function = (len(R) == len(C))
        is_injective = (len(R) == len(Orb))
        is_bijection = is_function and is_injective
        
        neg_q = not is_bijection
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "¬Q: The map g*Stab_G(x) |-> g.x is not a bijection"
]

N_HYP = 3
NEG_Q_INDEX = 3