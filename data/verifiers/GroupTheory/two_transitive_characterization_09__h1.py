import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness objects
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

def apply(g, x):
    """Apply transformation g to element x robustly."""
    if hasattr(g, "__call__"):
        try:
            return g(x)
        except Exception:
            pass
    if isinstance(x, tuple):
        return tuple(apply(g, item) for item in x)
    if isinstance(x, list):
        return [apply(g, item) for item in x]
    if isinstance(g, dict):
        return g.get(x, x)
    if hasattr(g, "__getitem__"):
        try:
            return g[x]
        except Exception:
            return x
    return x

def get_elements(witness):
    if hasattr(witness, "generate"):
        elements = []
        for i, g in enumerate(witness.generate()):
            if i >= 2000:  # Prevent timeout for very large groups
                break
            elements.append(g)
        return elements
    elif isinstance(witness, (list, set, tuple)):
        return list(witness)
    else:
        raise ValueError("Cannot get elements from witness")

def parse_witness(witness):
    """Extract the set X and the transformations G from the witness."""
    if isinstance(witness, tuple) and len(witness) == 2:
        X, G_obj = witness
        X_unique = []
        for x in X:
            if x not in X_unique:
                X_unique.append(x)
        return X_unique, get_elements(G_obj)
    elif hasattr(witness, "degree"):
        X = list(range(witness.degree))
        return X, get_elements(witness)
    elif isinstance(witness, list):
        elements = get_elements(witness)
        if elements and hasattr(elements[0], "size"):
            degree = max([p.size for p in elements])
            X = list(range(degree))
            return X, elements
    raise ValueError("Cannot parse witness")

def acts_on(X, G):
    for g in G:
        for x in X:
            y = apply(g, x)
            if y not in X:
                return False
    return True

def is_transitive(X, G):
    if not X:
        return True
    for start in X:
        reachable_list = [start]
        queue = [start]
        while queue:
            curr = queue.pop(0)
            for g in G:
                nxt = apply(g, curr)
                if nxt in X and nxt not in reachable_list:
                    reachable_list.append(nxt)
                    queue.append(nxt)
        for x in X:
            if x not in reachable_list:
                return False
    return True

def is_2_transitive(X, G):
    if len(X) < 2:
        return True
    pairs = [(x, y) for x in X for y in X if x != y]
    if not pairs:
        return True
    for start_pair in pairs:
        reachable_list = [start_pair]
        queue = [start_pair]
        while queue:
            curr = queue.pop(0)
            for g in G:
                nxt = (apply(g, curr[0]), apply(g, curr[1]))
                if nxt in pairs and nxt not in reachable_list:
                    reachable_list.append(nxt)
                    queue.append(nxt)
        for p in pairs:
            if p not in reachable_list:
                return False
    return True

def stabilizer_transitive_on_complement(X, G):
    for x in X:
        G_x = [g for g in G if apply(g, x) == x]
        comp = [y for y in X if y != x]
        if not comp:
            continue
        
        for start in comp:
            reachable_list = [start]
            queue = [start]
            while queue:
                curr = queue.pop(0)
                for g in G_x:
                    nxt = apply(g, curr)
                    if nxt in comp and nxt not in reachable_list:
                        reachable_list.append(nxt)
                        queue.append(nxt)
            for y in comp:
                if y not in reachable_list:
                    return False
    return True

def conditions(witness):
    try:
        X, G = parse_witness(witness)
    except Exception:
        return [False, False, False]
    
    try:
        h1 = len(X) >= 2
    except Exception:
        h1 = False
        
    try:
        h2 = acts_on(X, G)
    except Exception:
        h2 = False
        
    try:
        lhs = is_2_transitive(X, G)
        rhs = is_transitive(X, G) and stabilizer_transitive_on_complement(X, G)
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set with |X| >= 2",
    "H_2: G acts on X",
    "¬Q: G acts 2-transitively on X is NOT equivalent to (G acts transitively on X and for any x in X, G_x acts transitively on X \\ {x})"
]

N_HYP = 2
NEG_Q_INDEX = 2