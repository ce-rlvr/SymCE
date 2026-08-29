import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def is_normal_subgroup(G, H):
    try:
        for h in H.generators:
            if not G.contains(h):
                return False
        for g in G.generators:
            for h in H.generators:
                if not H.contains(~g * h * g):
                    return False
                if not H.contains(g * h * ~g):
                    return False
        return True
    except Exception:
        return False

def mutual_commutator_subgroup(H, K):
    h_elems = list(H.generate_dimino())
    k_elems = list(K.generate_dimino())
    gens = []
    for h in h_elems:
        for k in k_elems:
            comm = (~h) * (~k) * h * k
            gens.append(comm)
    if not gens:
        return PermutationGroup([Permutation()])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_normal_subgroup(G, H)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal_subgroup(G, K)
    except Exception:
        h2 = False
        
    try:
        HK_comm = mutual_commutator_subgroup(H, K)
        q = is_normal_subgroup(G, HK_comm)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a normal subgroup of G",
    "H_2: K is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2