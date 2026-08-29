import math
import sympy
from sympy import oo
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N is a normal subgroup of G",
    "¬Q: The index of H intersection N in H is not finite or not <= index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = hasattr(G, 'order') or hasattr(G, 'elements') or hasattr(G, 'generators')
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = H.is_subgroup(G)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: N is a normal subgroup of G
    try:
        if hasattr(N, 'is_normal'):
            h3 = N.is_normal(G)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: The index of H intersection N in H is finite and <= index of N in G is FALSE
    try:
        if hasattr(H, 'intersect'):
            H_int_N = H.intersect(N)
        elif hasattr(H, 'intersection'):
            H_int_N = H.intersection(N)
        else:
            H_int_N = None
            
        if H_int_N is not None:
            def get_index(grp, subgrp):
                if hasattr(grp, 'index') and callable(grp.index):
                    try:
                        return grp.index(subgrp)
                    except Exception:
                        pass
                o_g = grp.order() if callable(grp.order) else grp.order
                o_s = subgrp.order() if callable(subgrp.order) else subgrp.order
                
                if o_s == 0:
                    return oo
                if o_g == oo and o_s == oo:
                    return oo
                return sympy.Rational(o_g, o_s)
                
            idx_H = get_index(H, H_int_N)
            idx_G = get_index(G, N)
            
            def is_fin(val):
                if val == oo:
                    return False
                try:
                    fval = float(val)
                    if math.isinf(fval) or math.isnan(fval):
                        return False
                    return True
                except Exception:
                    return False
                    
            is_finite = is_fin(idx_H)
            is_le = False
            try:
                is_le = bool(idx_H <= idx_G)
            except Exception:
                pass
                
            neg_q = not (is_finite and is_le)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]