import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def has_subgroup_of_order(G, d):
    d = int(d)
    if d == 1:
        return True
    order = int(G.order())
    if d == order:
        return True
    if order % d != 0:
        return False
        
    # Sylow's First Theorem: if d is a prime power dividing |G|, 
    # then G has a subgroup of order d.
    factors = factorint(d)
    if len(factors) == 1:
        return True
        
    # The converse of Lagrange's theorem holds for nilpotent groups.
    try:
        if callable(getattr(G, 'is_nilpotent', None)) and G.is_nilpotent():
            return True
    except Exception:
        pass

    # Safeguard against excessively large groups to ensure fast execution
    if order > 100:
        raise ValueError("Group too large for exhaustive subgroup search")

    elements = list(G.generate())
    id_elem = G.identity
    
    all_subs = {frozenset([id_elem])}
    
    for g in elements:
        if g == id_elem:
            continue
        new_subs = set()
        for H in all_subs:
            if g not in H:
                sub = set(H)
                queue = [g]
                sub.add(g)
                while queue:
                    curr = queue.pop(0)
                    for x in list(sub):
                        p1 = curr * x
                        if p1 not in sub:
                            sub.add(p1)
                            queue.append(p1)
                        p2 = x * curr
                        if p2 not in sub:
                            sub.add(p2)
                            queue.append(p2)
                fs = frozenset(sub)
                if len(fs) == d:
                    return True
                if fs not in all_subs:
                    new_subs.add(fs)
        all_subs.update(new_subs)
        
    return False

def conditions(witness):
    try:
        G, d = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        order = G.order()
        h1 = (order > 0 and order < float('inf') and hasattr(G, 'generate') and hasattr(G, 'identity'))
    except Exception:
        h1 = False
        
    # H_2: d is a positive integer that divides the order of G
    try:
        if h1 and d > 0 and int(d) == d:
            h2 = (int(G.order()) % int(d) == 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: G does not contain at least one subgroup of order d
    try:
        if h1 and h2:
            neg_q = not has_subgroup_of_order(G, d)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: d is a positive integer that divides the order of G",
    "¬Q: G does not contain a subgroup of order d"
]

N_HYP = 2
NEG_Q_INDEX = 2