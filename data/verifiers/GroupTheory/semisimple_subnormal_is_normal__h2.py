import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def normal_closure(H, N):
    if H.order() == 1:
        return H
    gens = list(H.generators)
    N_gens = list(N.generators)
    group = PermutationGroup(gens)
    while True:
        added = False
        for g in list(group.generators):
            for n in N_gens:
                conj = n * g * ~n
                if not group.contains(conj):
                    gens.append(conj)
                    group = PermutationGroup(gens)
                    added = True
        if not added:
            break
    return group

def is_subnormal(H, G):
    if H.order() == 1:
        return True
    if not all(G.contains(g) for g in H.generators):
        return False
    current = G
    while True:
        next_group = normal_closure(H, current)
        if next_group.order() == H.order():
            return True
        if next_group.order() == current.order():
            return False
        current = next_group

def is_normal(H, G):
    if not all(G.contains(g) for g in H.generators):
        return False
    for g in H.generators:
        for n in G.generators:
            if not H.contains(n * g * ~n):
                return False
    return True

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H_2: H is a subnormal subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and is_subnormal(H, G)
    except Exception:
        h2 = False
        
    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q = not is_normal(H, G)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subnormal subgroup of G",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2