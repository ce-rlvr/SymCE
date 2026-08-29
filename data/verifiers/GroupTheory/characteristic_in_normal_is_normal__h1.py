import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

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
V4 = DihedralGroup(2)

def is_characteristic(K, N):
    try:
        if not K.is_subgroup(N):
            return False
    except Exception:
        return False

    try:
        elems = list(N.generate())
        gens = N.generators
        K_elems = set(K.generate())
        N_order = len(elems)
        N_id = next(e for e in elems if e.order() == 1)
    except Exception:
        return False
        
    valid_images = [[e for e in elems if e.order() == g.order()] for g in gens]
    
    for img in itertools.product(*valid_images):
        try:
            if img:
                if PermutationGroup(*img).order() != N_order:
                    continue
            else:
                if N_order != 1:
                    continue
        except Exception:
            continue
            
        mapping = {N_id: N_id}
        queue = [N_id]
        
        is_hom = True
        
        while queue:
            curr = queue.pop(0)
            for i, g in enumerate(gens):
                nxt = curr * g
                nxt_img = mapping[curr] * img[i]
                if nxt in mapping:
                    if mapping[nxt] != nxt_img:
                        is_hom = False
                        break
                else:
                    mapping[nxt] = nxt_img
                    queue.append(nxt)
            if not is_hom:
                break
                
        if is_hom and len(mapping) == N_order:
            for k_elem in K_elems:
                if mapping[k_elem] not in K_elems:
                    return False
                    
    return True

def conditions(witness):
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_characteristic(K, N)
    except Exception:
        h2 = False
        
    try:
        neg_q = not (K.is_subgroup(G) and K.is_normal(G))
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: K is a characteristic subgroup of N",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2