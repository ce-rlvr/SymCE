import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from itertools import product

# Top-level setup: named object bindings
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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_elements(grp):
    if hasattr(grp, 'elements'):
        return list(grp.elements)
    return list(grp.generate())

def group_intersection_order(G1, G2):
    elements1 = set(get_elements(G1))
    elements2 = set(get_elements(G2))
    return len(elements1.intersection(elements2))

def is_normal_subgroup(G, S):
    try:
        for s in S.generators:
            if s not in G:
                return False
    except Exception:
        return False
        
    if S.order() == 1:
        return True
        
    for g in G.generators:
        for s in S.generators:
            if (g * s * ~g) not in S:
                return False
    return True

def mixed_commutator_subgroup(G, N, H):
    gens = []
    id_el = G.identity
    elements_N = get_elements(N)
    elements_H = get_elements(H)
    for n in elements_N:
        for h in elements_H:
            c = n * h * ~n * ~h
            if c != id_el and c not in gens:
                gens.append(c)
    if not gens:
        gens = [id_el]
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            n_is_sub = all(n in G for n in N.generators)
            h2 = n_is_sub and is_normal_subgroup(G, N)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2:
            h_is_sub = all(h in G for h in H.generators)
            if h_is_sub and group_intersection_order(N, H) == 1 and N.order() * H.order() == G.order():
                h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            comm_subgroup = mixed_commutator_subgroup(G, N, H)
            neg_q = not is_normal_subgroup(G, comm_subgroup)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: The mixed commutator subgroup of N and H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3