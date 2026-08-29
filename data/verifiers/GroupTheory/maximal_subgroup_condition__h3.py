import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(G, H):
    for h in H.generators:
        if h not in G:
            return False
    return True

def is_normal(G, N):
    if not is_subgroup(G, N): 
        return False
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
    return True

def trivial_intersection(N, H):
    if N.order() < H.order():
        A, B = N, H
    else:
        A, B = H, N
    for a in A.generate():
        if a.is_Identity: 
            continue
        if a in B: 
            return False
    return True

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a group that is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        h1_ok = False
        if is_subgroup(G, N) and is_subgroup(G, H) and is_normal(G, N):
            if G.order() == N.order() * H.order():
                if trivial_intersection(N, H):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H2: N is an abelian group
    try:
        h2_ok = bool(N.is_abelian)
    except Exception:
        h2_ok = False

    # neg_Q: H is not a maximal subgroup of G
    try:
        neg_q_ok = False
        if H.order() == G.order():
            neg_q_ok = True
        else:
            for g in G.generate():
                if g not in H:
                    K_gens = list(H.generators) + [g]
                    K = PermutationGroup(*K_gens)
                    if K.order() < G.order():
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: N is an abelian group",
    "¬Q: H is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2