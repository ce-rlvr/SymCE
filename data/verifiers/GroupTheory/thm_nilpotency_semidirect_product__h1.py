import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def is_subgroup(G, H):
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(G, N):
    try:
        if not is_subgroup(G, N):
            return False
        for g in G.generators:
            for n in N.generators:
                if (g**-1 * n * g) not in N:
                    return False
                if (g * n * g**-1) not in N:
                    return False
        return True
    except Exception:
        return False

def is_semidirect_product(G, N, H):
    try:
        if not isinstance(G, PermutationGroup): return False
        if not isinstance(N, PermutationGroup): return False
        if not isinstance(H, PermutationGroup): return False
        if not is_subgroup(G, N): return False
        if not is_subgroup(G, H): return False
        if not is_normal(G, N): return False
        if G.order() != N.order() * H.order(): return False
        
        identity = H.identity
        for h in H.generate():
            if h == identity:
                continue
            if h in N:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        N, H, G = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a finite group
    try:
        h1_ok = isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: G is the semidirect product of N and H
    try:
        h2_ok = is_semidirect_product(G, N, H)
    except Exception:
        h2_ok = False
        
    # ¬Q: G is nilpotent if and only if the semidirect product is a direct product and both N and H are nilpotent groups
    try:
        g_nilp = bool(G.is_nilpotent)
        h_norm = is_normal(G, H)  # H being normal in G makes the semidirect product a direct product
        n_nilp = bool(N.is_nilpotent)
        h_nilp = bool(H.is_nilpotent)
        
        rhs = h_norm and n_nilp and h_nilp
        q_ok = (g_nilp == rhs)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: G is the semidirect product of N and H",
    "¬Q: The equivalence between G being nilpotent and (G is a direct product of nilpotent N and H) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2