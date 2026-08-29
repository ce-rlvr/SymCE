import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def is_subgroup(G, H):
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            return False
        if G.order() % H.order() != 0:
            return False
        for gen in H.generators:
            if gen not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(G, H):
    try:
        if not is_subgroup(G, H):
            return False
        for g in G.generators:
            for conj_g in (g, ~g):
                conj_g_inv = ~conj_g
                for h in H.generators:
                    conj = conj_g * h * conj_g_inv
                    if conj not in H:
                        return False
        return True
    except Exception:
        return False

def is_cyclic(group):
    try:
        if not isinstance(group, PermutationGroup):
            return False
        o = group.order()
        if o == 1:
            return True
        for g in group.generate():
            if g.order() == o:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2_ok = is_normal(G, N)
    except Exception:
        h2_ok = False
        
    # H_3: N is a cyclic group
    try:
        h3_ok = is_cyclic(N)
    except Exception:
        h3_ok = False
        
    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q_ok = not is_normal(G, H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a cyclic group",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3