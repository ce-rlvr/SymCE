import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False
        
    # ¬Q: The set product HN is NOT a subgroup of G
    try:
        def get_elements(grp):
            if hasattr(grp, 'generate'):
                return set(grp.generate())
            elif hasattr(grp, 'elements'):
                return set(grp.elements)
            else:
                return set(grp)
                
        H_elems = get_elements(H)
        N_elems = get_elements(N)
        
        # Set product HN
        HN = {h * n for h in H_elems for n in N_elems}
        
        # Check if HN is a subgroup (must be non-empty and closed under inversion and multiplication)
        is_subgroup = True
        if not HN:
            is_subgroup = False
        else:
            for a in HN:
                if ~a not in HN:
                    is_subgroup = False
                    break
                for b in HN:
                    if a * b not in HN:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "¬Q: HN is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2