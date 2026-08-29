import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from itertools import product

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

def is_characteristic(K, N):
    if not K.is_subgroup(N):
        return False
    if K.order() == 1 or K.order() == N.order():
        return True
    if not K.is_normal(N):
        return False
        
    gens = N.generators
    elements = list(N.generate())
    identity = next(e for e in elements if e.is_Identity)
    
    gen_orders = [g.order() for g in gens]
    candidates = [[e for e in elements if e.order() == o] for o in gen_orders]
    K_elements = set(K.generate())
    
    for mapping in product(*candidates):
        map_dict = {identity: identity}
        queue = [identity]
        is_hom = True
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                nxt_val = map_dict[curr] * mapping[i]
                if nxt in map_dict:
                    if map_dict[nxt] != nxt_val:
                        is_hom = False
                        break
                else:
                    map_dict[nxt] = nxt_val
                    queue.append(nxt)
            if not is_hom:
                break
        
        if is_hom and len(set(map_dict.values())) == len(elements):
            for k in K_elements:
                if map_dict[k] not in K_elements:
                    return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(N, PermutationGroup) and isinstance(K, PermutationGroup) and N.is_subgroup(G) and is_characteristic(K, N)
    except Exception:
        h2 = False
        
    try:
        neg_q = not K.is_normal(G)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a characteristic subgroup of N (where N <= G)",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2