import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finitely presented group and H is a subgroup",
    "H_2: The index of H in G is finite",
    "¬Q: H is not finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness (expected to be a tuple (G, H)), checks if it is a valid counterexample.
    Returns a list of booleans corresponding to CONDITION_LABELS.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finitely presented group and H is a subgroup
    h1_ok = False
    try:
        g_fp = False
        if hasattr(G, 'is_finitely_presented'):
            attr = getattr(G, 'is_finitely_presented')
            g_fp = bool(attr() if callable(attr) else attr)
        else:
            from sympy.combinatorics.fp_groups import FpGroup
            from sympy.combinatorics.perm_groups import PermutationGroup
            if isinstance(G, (FpGroup, PermutationGroup)):
                g_fp = True
        
        h_sub = False
        if hasattr(H, 'is_subgroup'):
            attr = getattr(H, 'is_subgroup')
            h_sub = bool(attr(G) if callable(attr) else attr)
        elif hasattr(G, 'has_subgroup'):
            attr = getattr(G, 'has_subgroup')
            h_sub = bool(attr(H) if callable(attr) else attr)
        else:
            from sympy.combinatorics.fp_groups import FpGroup, FpSubgroup
            from sympy.combinatorics.perm_groups import PermutationGroup
            if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                h_sub = H.is_subgroup(G)
            elif isinstance(G, FpGroup) and isinstance(H, FpSubgroup):
                h_sub = (H.parent == G)
            elif hasattr(H, 'parent'):
                h_sub = (H.parent == G)
        
        h1_ok = bool(g_fp and h_sub)
    except Exception:
        h1_ok = False

    # H_2: The index of H in G is finite
    h2_ok = False
    try:
        if hasattr(G, 'index'):
            attr = getattr(G, 'index')
            idx = attr(H) if callable(attr) else attr
            h2_ok = (idx is not None and idx != float('inf') and idx != sympy.oo)
        elif hasattr(H, 'index_in'):
            attr = getattr(H, 'index_in')
            idx = attr(G) if callable(attr) else attr
            h2_ok = (idx is not None and idx != float('inf') and idx != sympy.oo)
        elif hasattr(H, 'index'):
            attr = getattr(H, 'index')
            idx = attr(G) if callable(attr) else attr
            h2_ok = (idx is not None and idx != float('inf') and idx != sympy.oo)
        else:
            from sympy.combinatorics.perm_groups import PermutationGroup
            from sympy.combinatorics.fp_groups import FpGroup, FpSubgroup
            if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                h2_ok = True
            elif isinstance(G, FpGroup) and isinstance(H, FpSubgroup):
                C = G.coset_table(H.generators, max_cosets=5000)
                h2_ok = (C is not None)
            elif hasattr(G, 'order') and hasattr(H, 'order'):
                g_ord_attr = getattr(G, 'order')
                g_ord = g_ord_attr() if callable(g_ord_attr) else g_ord_attr
                if g_ord != float('inf') and g_ord != sympy.oo:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: H is not finitely presented
    neg_q = False
    try:
        h_fp = True
        if hasattr(H, 'is_finitely_presented'):
            attr = getattr(H, 'is_finitely_presented')
            h_fp = bool(attr() if callable(attr) else attr)
        else:
            from sympy.combinatorics.fp_groups import FpGroup, FpSubgroup
            from sympy.combinatorics.perm_groups import PermutationGroup
            if isinstance(H, PermutationGroup):
                h_fp = True
            elif isinstance(H, FpSubgroup):
                h_fp = True
            elif isinstance(H, FpGroup):
                h_fp = True
        neg_q = not h_fp
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]