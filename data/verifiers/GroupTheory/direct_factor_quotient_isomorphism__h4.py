import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_order(G):
    try:
        if callable(G.order):
            return G.order()
        return G.order
    except Exception:
        return 0

def is_subgroup(H, G):
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        return all(G.contains(h) for h in H.generators)
    except Exception:
        return False

def is_normal(G, H):
    try:
        if not is_subgroup(H, G):
            return False
        for g in G.generators:
            for h in H.generators:
                if not H.contains(g * h * ~g):
                    return False
        return True
    except Exception:
        return False

def intersection_trivial(G, H, K):
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(K, PermutationGroup):
            return False
        count = 0
        for h in H.generate():
            if K.contains(h):
                count += 1
                if count > 1:
                    return False
        return count == 1
    except Exception:
        return False

def neg_q_check(G, H, K):
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup) or not isinstance(K, PermutationGroup):
            return False
            
        if get_order(G) != get_order(H) * get_order(K):
            return True
            
        if not is_normal(G, H):
            return True
            
        reps = []
        for g in G.generate():
            is_new = True
            for r in reps:
                if H.contains(~r * g):
                    is_new = False
                    break
            if is_new:
                reps.append(g)
                
        n = len(reps)
        def coset_index(g):
            for i, r in enumerate(reps):
                if H.contains(~r * g):
                    return i
            return -1
            
        perms = []
        for i in range(n):
            p = []
            for j in range(n):
                p.append(coset_index(reps[i] * reps[j]))
            perms.append(Permutation(p))
            
        GH_group = PermutationGroup(perms)
        return not GH_group.is_isomorphic(K)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 5
        G, H, K = witness
    except Exception:
        return [False] * 5
        
    h1 = False
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        pass
        
    h2 = is_normal(G, H)
    h3 = is_normal(G, K)
    h4 = intersection_trivial(G, H, K)
    neg_q = neg_q_check(G, H, K)
    
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "H_4: The intersection of H and K contains only the identity element",
    "¬Q: The quotient group G/H is not isomorphic to K"
]

N_HYP = 4
NEG_Q_INDEX = 4