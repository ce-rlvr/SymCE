import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def is_subgroup(H, N):
    try:
        if hasattr(H, 'is_subgroup'):
            return bool(H.is_subgroup(N))
    except Exception:
        pass
    try:
        for g in H.generators:
            if g not in N:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a cyclic group
    try:
        h2 = False
        if getattr(N, 'is_group', False) or isinstance(N, PermutationGroup):
            is_cyc = None
            if hasattr(N, 'is_cyclic'):
                val = N.is_cyclic
                if callable(val):
                    val = val()
                if isinstance(val, bool):
                    is_cyc = val
            
            if is_cyc is not None:
                h2 = is_cyc
            else:
                order_attr = N.order
                order = order_attr() if callable(order_attr) else order_attr
                if order == 1:
                    h2 = True
                else:
                    for g in N.elements:
                        g_order_attr = g.order
                        g_order = g_order_attr() if callable(g_order_attr) else g_order_attr
                        if g_order == order:
                            h2 = True
                            break
    except Exception:
        h2 = False
        
    # H3: H is a subgroup of N
    try:
        h3 = False
        if getattr(H, 'is_group', False) or isinstance(H, PermutationGroup):
            h3 = is_subgroup(H, N)
    except Exception:
        h3 = False
        
    # neg_Q: H is NOT a normal subgroup of G
    try:
        if not (getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)):
            neg_q = False
        elif not (getattr(H, 'is_group', False) or isinstance(H, PermutationGroup)):
            neg_q = False
        else:
            neg_q = not is_normal_subgroup(H, G)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a cyclic group",
    "H_3: H is a subgroup of N",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3