import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The missing hypothesis is that G is a group (allowing G to be a monoid).
    
    Expected witness format: (X, G, x)
    - X: an iterable representing the finite set.
    - G: an iterable of transformations on X (e.g., dicts mapping X -> X, or callable permutations).
    - x: an element of X.
    """
    try:
        if len(witness) == 3:
            X, G, x = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: X is a finite set
    try:
        X_list = list(set(X))
        h1 = len(X_list) > 0
    except Exception:
        h1 = False

    # H_2: G acts on X
    try:
        h2 = True
        raw_G_list = []
        for g in list(G):
            if isinstance(g, dict):
                raw_G_list.append(g)
            elif callable(g):
                d = {}
                for y in X_list:
                    try:
                        res = g(y)
                    except Exception:
                        res = y
                    d[y] = res
                raw_G_list.append(d)
            else:
                raw_G_list.append(g)
                
        # Deduplicate to form a proper set of transformations
        G_list = []
        for g in raw_G_list:
            if g not in G_list:
                G_list.append(g)
                
        if not G_list:
            h2 = False
        else:
            X_set = set(X_list)
            # Verify all elements are valid functions X -> X
            for g in G_list:
                if not isinstance(g, dict):
                    h2 = False
                    break
                if set(g.keys()) != X_set:
                    h2 = False
                    break
                if not all(v in X_set for v in g.values()):
                    h2 = False
                    break
            
            if h2:
                # Check for identity element
                id_func = {y: y for y in X_list}
                if id_func not in G_list:
                    h2 = False
                
                # Check for closure under composition
                if h2:
                    for g in G_list:
                        for h in G_list:
                            comp = {y: g[h[y]] for y in X_list}
                            if comp not in G_list:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: x \in X
    try:
        h3 = x in X_list
    except Exception:
        h3 = False

    # ¬Q: |G| != |Orb(x)| * |Stab(x)|
    try:
        orb = set(g[x] for g in G_list)
        stab = [g for g in G_list if g[x] == x]
        neg_q = len(G_list) != len(orb) * len(stab)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: G acts on X",
    "H_3: x in X",
    "¬Q: |G| != |Orb(x)| * |Stab(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3