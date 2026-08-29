import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from itertools import combinations

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_nonabelian_simple(S):
    try:
        if S.is_abelian: 
            return False
        if S.derived_subgroup().order() != S.order(): 
            return False
        # Known orders of non-abelian simple groups up to ~10000
        known_orders = {60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080, 5616, 6048, 7920, 9828}
        if S.order() in known_orders:
            return True
        return False
    except Exception:
        return False

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if not G.contains(h):
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    if not is_subgroup(N, G): 
        return False
    try:
        for g in G.generators:
            for n in N.generators:
                if not N.contains(~g * n * g):
                    return False
        return True
    except Exception:
        return False

def is_internal_direct_product(N, C):
    try:
        if not C:
            return N.order() == 1
        
        for S in C:
            if not is_subgroup(S, N):
                return False
                
        C_gens = []
        for S in C:
            C_gens.extend(S.generators)
        H = PermutationGroup(C_gens)
        if H.order() != N.order():
            return False
            
        for S in C:
            if not is_normal(S, N):
                return False
                
        for i, S in enumerate(C):
            other_gens = []
            for j, other_S in enumerate(C):
                if i != j:
                    other_gens.extend(other_S.generators)
            if other_gens:
                Other = PermutationGroup(other_gens)
                S_Other = PermutationGroup(S.generators + Other.generators)
                # If S and Other are normal subgroups, their intersection is trivial 
                # if and only if the order of their product equals the product of their orders.
                if S_Other.order() != S.order() * Other.order():
                    return False
        return True
    except Exception:
        return False

def check_conclusion(S_list, G, N):
    try:
        n = len(S_list)
        for r in range(n + 1):
            for indices in combinations(range(n), r):
                C = [S_list[i] for i in indices]
                if is_internal_direct_product(N, C):
                    return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            S_list = witness.get('S_list', [])
            G = witness.get('G', None)
            N = witness.get('N', None)
        else:
            S_list, G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: S_1, S_2, ..., S_n is a finite collection of non-abelian simple groups
    try:
        h1 = isinstance(S_list, (list, tuple, set)) and len(S_list) >= 1
        if h1:
            for S in S_list:
                if not is_nonabelian_simple(S):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = is_normal(N, G)
    except Exception:
        h2 = False

    # ¬Q: N is not isomorphic to the direct product of a subcollection of the groups S_i, 
    # or does not correspond to the internal direct product of those specific factors within G
    try:
        neg_q = not check_conclusion(S_list, G, N)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_1, S_2, ..., S_n is a finite collection of non-abelian simple groups",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not isomorphic to the direct product of a subcollection of the groups S_i, or does not correspond to the internal direct product of those specific factors within G"
]

N_HYP = 2
NEG_Q_INDEX = 2