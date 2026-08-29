import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def get_order(grp):
    if hasattr(grp, 'order'):
        if callable(grp.order):
            return grp.order()
        return grp.order
    return len(list(grp.generate()))

def conditions(witness) -> list[bool]:
    try:
        G, d = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a solvable group
    try:
        if callable(G.is_solvable):
            h1 = bool(G.is_solvable())
        else:
            h1 = bool(G.is_solvable)
    except Exception:
        h1 = False
        
    # H_2: d >= 1
    try:
        h2 = int(d) >= 1
    except Exception:
        h2 = False
        
    # ¬Q: G^{(d-1)} is not a non-trivial abelian normal subgroup of G
    try:
        if callable(G.derived_series):
            ds = G.derived_series()
        else:
            ds = G.derived_series
            
        idx = int(d) - 1
        if idx < len(ds):
            H = ds[idx]
        else:
            H = ds[-1]
            
        is_non_trivial = (get_order(H) > 1)
        
        if callable(H.is_abelian):
            is_abelian = bool(H.is_abelian())
        else:
            is_abelian = bool(H.is_abelian)
            
        is_normal = True
        for g in G.generators:
            for h in H.generators:
                conj1 = (~g) * h * g
                conj2 = g * h * (~g)
                if not H.contains(conj1) or not H.contains(conj2):
                    is_normal = False
                    break
            if not is_normal:
                break
                
        q = is_non_trivial and is_abelian and is_normal
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: d >= 1",
    "¬Q: G^{(d-1)} is not a non-trivial abelian normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2