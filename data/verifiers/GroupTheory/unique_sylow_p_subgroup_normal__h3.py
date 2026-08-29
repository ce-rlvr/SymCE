import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import isprime

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
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(G, H):
    try:
        if hasattr(G, 'is_normal'):
            return G.is_normal(H)
    except Exception:
        pass
    try:
        for g in G.generators:
            g_inv = g**-1
            for h in H.generators:
                if (g * h * g_inv) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: The number of distinct Sylow p-subgroups of G is exactly 1
    try:
        if not h1 or not h2:
            h3 = False
        else:
            try:
                order = G.order()
            except TypeError:
                order = G.order
                
            if order % p != 0:
                h3 = True
            else:
                S = G.sylow_subgroup(p)
                h3 = is_normal_subgroup(G, S)
    except Exception:
        h3 = False
        
    # ¬Q: P is not a normal subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            neg_q = True
        elif not is_subgroup(G, P):
            neg_q = True
        else:
            neg_q = not is_normal_subgroup(G, P)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: The number of distinct Sylow p-subgroups of G is exactly 1",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3