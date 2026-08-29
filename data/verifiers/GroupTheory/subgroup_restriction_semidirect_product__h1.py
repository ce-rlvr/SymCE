import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def is_subgroup_list(subset, group_elems):
    if not subset:
        return False
    for s in subset:
        if s not in group_elems:
            return False
    for a in subset:
        for b in subset:
            if a * b not in subset:
                return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            H = witness['H']
            K = witness['K']
        elif len(witness) == 4:
            G, N, H, K = witness
        elif len(witness) == 5:
            G, N, H, K, phi = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        K_elems = get_elements(K)
        H_elems = get_elements(H)
        h1_ok = is_subgroup_list(K_elems, H_elems)
    except Exception:
        h1_ok = False

    try:
        N_elems = get_elements(N)
        K_elems = get_elements(K)
        G_elems = get_elements(G)
        
        NK_list = []
        for n in N_elems:
            for k in K_elems:
                nk = n * k
                if nk not in NK_list:
                    NK_list.append(nk)
                    
        nk_is_subgroup = is_subgroup_list(NK_list, G_elems)
        size_match = (len(NK_list) == len(N_elems) * len(K_elems))
        
        normalizes_N = True
        for k in K_elems:
            try:
                k_inv = k**-1
            except Exception:
                k_inv = ~k
            for n in N_elems:
                if k * n * k_inv not in N_elems:
                    normalizes_N = False
                    break
            if not normalizes_N:
                break
                
        n_is_subgroup = is_subgroup_list(N_elems, G_elems)
        k_is_subgroup = is_subgroup_list(K_elems, G_elems)
        
        q_ok = n_is_subgroup and k_is_subgroup and normalizes_N and nk_is_subgroup and size_match
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: K is a subgroup of H",
    "¬Q: N x K is not a subgroup of G or is not isomorphic to N rtimes K"
]

N_HYP = 1
NEG_Q_INDEX = 1