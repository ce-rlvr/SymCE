import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_identity(G):
    gens = G.generators
    if not gens:
        return Permutation()
    g = gens[0]
    return g * (~g)

def is_subgroup(H, G):
    try:
        G_elements = set(G.generate())
        return all(g in G_elements for g in H.generators)
    except Exception:
        return False

def is_normal(K, G):
    try:
        if not is_subgroup(K, G):
            return False
        K_elements = set(K.generate())
        G_elements = list(G.generate())
        for g in G_elements:
            g_inv = ~g
            for k in K.generators:
                conj = g_inv * k * g
                if conj not in K_elements:
                    return False
        return True
    except Exception:
        return False

def is_characteristic(N, K):
    try:
        if not is_subgroup(K, N):
            return False
        elements = list(N.generate())
        gens = N.generators
        K_elements = set(K.generate())
        id_N = get_identity(N)
        
        for imgs in product(elements, repeat=len(gens)):
            mapping = {id_N: id_N}
            valid = True
            queue = [id_N]
            
            while queue:
                curr = queue.pop(0)
                for g, img_g in zip(gens, imgs):
                    nxt = curr * g
                    nxt_img = mapping[curr] * img_g
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        queue.append(nxt)
                if not valid:
                    break
                    
            if valid and len(set(mapping.values())) == len(elements):
                for k in K.generators:
                    if mapping[k] not in K_elements:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, K = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_subgroup(N, G) and is_characteristic(N, K)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_normal(K, G)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a characteristic subgroup of N",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1