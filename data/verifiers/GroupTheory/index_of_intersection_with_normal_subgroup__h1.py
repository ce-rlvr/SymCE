import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo
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

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_normal(G))
    except Exception:
        h2 = False
        
    # H_3: index of N in G is finite
    try:
        g_order = G.order()
        n_order = N.order()
        idx_GN = g_order / n_order
        h3 = bool(idx_GN < oo)
    except Exception:
        h3 = False
        idx_GN = None
        
    # neg_Q: The index of H cap N in H is finite and <= index of N in G
    # We negate this conclusion.
    try:
        if idx_GN is None:
            g_order = G.order()
            n_order = N.order()
            idx_GN = g_order / n_order
            
        h_order = H.order()
        
        try:
            int_elements = set(H.generate()).intersection(set(N.generate()))
            int_order = len(int_elements)
        except Exception:
            int_elements = set(H.elements).intersection(set(N.elements))
            int_order = len(int_elements)
            
        idx_H_H_int_N = h_order / int_order
        
        q = (idx_H_H_int_N < oo) and (idx_H_H_int_N <= idx_GN)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of N in G is finite",
    "not Q: The index of H cap N in H is infinite or strictly greater than the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3