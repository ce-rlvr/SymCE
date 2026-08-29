import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H, M = witness
    except Exception:
        return [False, False]
        
    def is_normal_subgroup(sub, grp):
        if not sub.is_subgroup(grp):
            return False
        for g in grp.generators:
            for s in sub.generators:
                try:
                    g_inv = ~g
                except Exception:
                    g_inv = g**-1
                if (g * s * g_inv) not in sub:
                    return False
        return True

    # H_1: M is a subgroup of N
    try:
        h1 = bool(M.is_subgroup(N))
    except Exception:
        h1 = False
        
    # neg_Q: M is a normal subgroup of G iff M is a normal subgroup of N and hMh^{-1} = M for all h \in H
    try:
        m_normal_G = is_normal_subgroup(M, G)
        m_normal_N = is_normal_subgroup(M, N)
        
        H_elements = H.generators if hasattr(H, 'generators') else H
        M_elements = M.generators if hasattr(M, 'generators') else M
        
        h_normalizes_M = True
        for h in H_elements:
            for m in M_elements:
                try:
                    h_inv = ~h
                except Exception:
                    h_inv = h**-1
                if (h * m * h_inv) not in M:
                    h_normalizes_M = False
                    break
            if not h_normalizes_M:
                break
                
        rhs = m_normal_N and h_normalizes_M
        
        q = (m_normal_G == rhs)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a subgroup of N",
    "¬Q: M is normal in G is NOT equivalent to (M is normal in N and normalized by H)"
]

N_HYP = 1
NEG_Q_INDEX = 1