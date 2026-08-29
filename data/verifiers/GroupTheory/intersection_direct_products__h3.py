import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

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

def is_group(G):
    try:
        if isinstance(G, PermutationGroup):
            return True
        elements = set(list(G))
        if not elements:
            return False
        for e1 in elements:
            for e2 in elements:
                if e1 * e2 not in elements:
                    return False
        for e in elements:
            if e**-1 not in elements:
                return False
        return True
    except Exception:
        return False

def is_subgroup(sub, group):
    try:
        elements = set(list(sub))
        if not elements:
            return False
        for e in elements:
            if e not in group:
                return False
        for e1 in elements:
            for e2 in elements:
                if e1 * e2 not in elements:
                    return False
        for e in elements:
            if e**-1 not in elements:
                return False
        return True
    except Exception:
        return False

def cartesian_product(X, Y):
    return set(itertools.product(list(X), list(Y)))

def is_subgroup_pairs(pairs, G, H):
    if not pairs:
        return False
    pairs = set(pairs)
    for (g, h) in pairs:
        if g not in G or h not in H:
            return False
    for (g1, h1) in pairs:
        for (g2, h2) in pairs:
            if (g1*g2, h1*h2) not in pairs:
                return False
    for (g, h) in pairs:
        if (g**-1, h**-1) not in pairs:
            return False
    return True

def conditions(witness):
    try:
        G, H, A, C, B, D = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False
        
    try:
        h2 = is_subgroup(A, G) and is_subgroup(C, G)
    except Exception:
        h2 = False
        
    try:
        AxB = cartesian_product(A, B)
        CxD = cartesian_product(C, D)
        
        axb_is_sub = is_subgroup_pairs(AxB, G, H)
        cxd_is_sub = is_subgroup_pairs(CxD, G, H)
        
        A_elems = set(list(A))
        C_elems = set(list(C))
        B_elems = set(list(B))
        D_elems = set(list(D))
        
        A_cap_C = A_elems.intersection(C_elems)
        B_cap_D = B_elems.intersection(D_elems)
        
        LHS = AxB.intersection(CxD)
        RHS = cartesian_product(A_cap_C, B_cap_D)
        
        intersection_eq = (LHS == RHS)
        
        q = axb_is_sub and cxd_is_sub and intersection_eq
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and C are subgroups of G",
    "¬Q: A x B or C x D is not a subgroup of G x H, or their intersection is not (A ∩ C) x (B ∩ D)"
]

N_HYP = 2
NEG_Q_INDEX = 2