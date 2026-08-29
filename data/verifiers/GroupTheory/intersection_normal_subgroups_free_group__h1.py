import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Klein four-group (V4) is a common counterexample for this conjecture
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic(G):
    if hasattr(G, 'is_cyclic'):
        res = G.is_cyclic
        if callable(res):
            return res()
        return res
    order = G.order()
    for g in G.generate():
        if g.order() == order:
            return True
    return False

def is_subgroup(H, G):
    for h in H.generators:
        if h not in G:
            return False
    return True

def is_normal_subgroup(H, G):
    for h in H.generators:
        for g in G.generators:
            conj = g * h * (g**-1)
            if conj not in H:
                return False
            conj_inv = (g**-1) * h * g
            if conj_inv not in H:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        F, N, M = witness
    except Exception:
        return [False, False, False]
    
    # H_1: The rank of F is strictly greater than 1
    # A group has rank > 1 if and only if it is not cyclic and not trivial.
    try:
        h1 = bool((not is_cyclic(F)) and (F.order() > 1))
    except Exception:
        h1 = False
        
    # H_2: N and M are non-trivial normal subgroups of F
    try:
        if N.order() > 1 and M.order() > 1:
            n_sub = is_subgroup(N, F)
            m_sub = is_subgroup(M, F)
            n_norm = is_normal_subgroup(N, F)
            m_norm = is_normal_subgroup(M, F)
            h2 = bool(n_sub and m_sub and n_norm and m_norm)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The intersection N \cap M is trivial
    try:
        intersection_trivial = True
        for n in N.generate():
            if getattr(n, 'is_Identity', False) or n.order() == 1:
                continue
            if n in M:
                intersection_trivial = False
                break
        neg_q = bool(intersection_trivial)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of F is strictly greater than 1",
    "H_2: N and M are non-trivial normal subgroups of F",
    "¬Q: The intersection N \\cap M is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2