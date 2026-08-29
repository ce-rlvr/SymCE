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
V4 = PermutationGroup([Permutation(0, 1) * Permutation(2, 3), Permutation(0, 2) * Permutation(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_normal_subgroup(G, H):
    for h in H.generators:
        if not G.contains(h):
            return False
            
    for g in G.generators:
        g_inv = ~g
        for h in H.generators:
            if not H.contains(g * h * g_inv):
                return False
            if not H.contains(g_inv * h * g):
                return False
    return True

def intersect_groups(M, N):
    M_elements = list(M.generate())
    common = []
    for m in M_elements:
        if N.contains(m):
            common.append(m)
    if not common:
        return None
    return PermutationGroup(common)

def check_G_equals_MN(G, M, N):
    for m in M.generators:
        if not G.contains(m):
            return False
    for n in N.generators:
        if not G.contains(n):
            return False
            
    M_cap_N = intersect_groups(M, N)
    if M_cap_N is None:
        return False
        
    mn_size = (M.order() * N.order()) // M_cap_N.order()
    return G.order() == mn_size

def get_quotient_group(G, N):
    G_elements = list(G.generate())
    cosets = []
    coset_reps = []
    
    for g in G_elements:
        found = False
        for rep in coset_reps:
            if N.contains(~rep * g):
                found = True
                break
        if not found:
            coset_reps.append(g)
            
    n_cosets = len(coset_reps)
    table = [[0] * n_cosets for _ in range(n_cosets)]
    
    for i in range(n_cosets):
        for j in range(n_cosets):
            prod = coset_reps[i] * coset_reps[j]
            found = False
            for k, rep in enumerate(coset_reps):
                if N.contains(~rep * prod):
                    table[i][j] = k
                    found = True
                    break
            if not found:
                return None
                
    for row in table:
        if len(set(row)) != n_cosets:
            return None
            
    perms = [Permutation(row) for row in table]
    P = PermutationGroup(perms)
    if P.order() != n_cosets:
        return None
    return P

def direct_product(G1, G2):
    if G1 is None or G2 is None:
        return None
    
    deg1 = G1.degree
    deg2 = G2.degree
    
    if deg1 == 0 and deg2 == 0:
        return PermutationGroup([Permutation(0)])
    if deg1 == 0:
        return G2
    if deg2 == 0:
        return G1

    perms = []
    for p in G1.generators:
        arr = p.array_form
        arr = arr + list(range(len(arr), deg1))
        arr = arr + list(range(deg1, deg1 + deg2))
        perms.append(Permutation(arr))
        
    for p in G2.generators:
        arr = p.array_form
        arr = arr + list(range(len(arr), deg2))
        arr = list(range(deg1)) + [x + deg1 for x in arr]
        perms.append(Permutation(arr))
        
    if not perms:
        return PermutationGroup([Permutation(0)])
        
    return PermutationGroup(perms)

def check_neg_Q(G, M, N):
    M_cap_N = intersect_groups(M, N)
    if M_cap_N is None:
        return False
        
    LHS = get_quotient_group(G, M_cap_N)
    if LHS is None:
        return False
        
    G_M = get_quotient_group(G, M)
    G_N = get_quotient_group(G, N)
    
    if G_M is None or G_N is None:
        return False
        
    RHS = direct_product(G_M, G_N)
    if RHS is None:
        return False
        
    return not LHS.is_isomorphic(RHS)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, M, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_normal_subgroup(G, M)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal_subgroup(G, N)
    except Exception:
        h2 = False
        
    try:
        h3 = check_G_equals_MN(G, M, N)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(G, M, N)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is a normal subgroup of G",
    "H_2: N is a normal subgroup of G",
    "H_3: G = MN",
    "¬Q: G/(M \\cap N) is not isomorphic to (G/M) \\times (G/N)"
]

N_HYP = 3
NEG_Q_INDEX = 3