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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(X):
    if hasattr(X, 'elements'):
        return list(X.elements)
    elif hasattr(X, 'generate'):
        return list(X.generate())
    else:
        return list(X)

def is_subset(X, G):
    try:
        X_elems = get_elements(X)
        for x in X_elems:
            if not G.contains(x):
                return False
        return True
    except Exception:
        return False

def is_subgroup(X, G):
    try:
        if not is_subset(X, G):
            return False
        X_elems = get_elements(X)
        if not X_elems:
            return False
        if G.identity not in X_elems:
            return False
        for x in X_elems:
            for y in X_elems:
                if x*y not in X_elems:
                    return False
        for x in X_elems:
            if x**-1 not in X_elems:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, H, A, B, C, D = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        def is_group(obj):
            if isinstance(obj, PermutationGroup):
                return True
            if hasattr(obj, 'is_group') and obj.is_group:
                return True
            return False
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    # H_2: B and D are subgroups of H
    try:
        h2 = is_subgroup(B, H) and is_subgroup(D, H)
    except Exception:
        h2 = False

    # neg_Q: The intersection of the subgroups A x B and C x D in G x H is exactly (A ∩ C) x (B ∩ D)
    try:
        try:
            A_elems = get_elements(A)
            B_elems = get_elements(B)
            C_elems = get_elements(C)
            D_elems = get_elements(D)
        except Exception:
            neg_q = True
        else:
            A_is_sub = is_subgroup(A, G)
            B_is_sub = is_subgroup(B, H)
            C_is_sub = is_subgroup(C, G)
            D_is_sub = is_subgroup(D, H)
            
            AxB_is_sub = A_is_sub and B_is_sub
            CxD_is_sub = C_is_sub and D_is_sub
            
            AxB = set(itertools.product(A_elems, B_elems))
            CxD = set(itertools.product(C_elems, D_elems))
            
            intersection = AxB.intersection(CxD)
            
            A_cap_C = set(A_elems).intersection(set(C_elems))
            B_cap_D = set(B_elems).intersection(set(D_elems))
            
            expected_intersection = set(itertools.product(A_cap_C, B_cap_D))
            
            intersection_eq = (intersection == expected_intersection)
            
            conclusion = AxB_is_sub and CxD_is_sub and intersection_eq
            neg_q = not conclusion
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: B and D are subgroups of H",
    "¬Q: A x B or C x D is not a subgroup of G x H, or their intersection is not (A ∩ C) x (B ∩ D)"
]

N_HYP = 2
NEG_Q_INDEX = 2