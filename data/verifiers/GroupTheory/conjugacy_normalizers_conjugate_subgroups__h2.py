import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_elements(X):
    if hasattr(X, 'elements'):
        return set(X.elements)
    if isinstance(X, Permutation):
        return {X}
    try:
        return set(X)
    except TypeError:
        return {X}

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H and K are conjugate in G
    try:
        H_elems = get_elements(H)
        K_elems = get_elements(K)
        G_elems = set(G.elements)
        
        if not H_elems.issubset(G_elems) or not K_elems.issubset(G_elems):
            h2 = False
        else:
            h2 = False
            if len(H_elems) == len(K_elems):
                for g in G_elems:
                    if set(g * h * ~g for h in H_elems) == K_elems:
                        h2 = True
                        break
    except Exception:
        h2 = False
        
    # neg_Q: N_G(H) is not conjugate to N_G(K) in G
    try:
        H_elems = get_elements(H)
        K_elems = get_elements(K)
        G_elems = set(G.elements)
        
        N_H = set()
        for g in G_elems:
            if set(g * h * ~g for h in H_elems) == H_elems:
                N_H.add(g)
        
        N_K = set()
        for g in G_elems:
            if set(g * k * ~g for k in K_elems) == K_elems:
                N_K.add(g)
                
        q = False
        if len(N_H) == len(N_K):
            for g in G_elems:
                if set(g * x * ~g for x in N_H) == N_K:
                    q = True
                    break
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H and K are conjugate in G",
    "¬Q: N_G(H) is not conjugate to N_G(K) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2