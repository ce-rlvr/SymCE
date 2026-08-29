import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product(G1, G2):
    try:
        res = G1 * G2
        if isinstance(res, PermutationGroup):
            return res
    except Exception:
        pass
    gens = []
    d1 = G1.degree
    d2 = G2.degree
    if d1 == 0: d1 = 1
    if d2 == 0: d2 = 1
    for g in G1.generators:
        arr = list(g.array_form)
        arr += list(range(len(arr), d1))
        p = arr + list(range(d1, d1 + d2))
        gens.append(Permutation(p))
    for g in G2.generators:
        arr = list(g.array_form)
        arr += list(range(len(arr), d2))
        p = list(range(d1)) + [x + d1 for x in arr]
        gens.append(Permutation(p))
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def quotient_group(G, N):
    if G.order() == N.order():
        return PermutationGroup([Permutation(0)])
    reps = G.coset_transversal(N)
    gens = []
    for g in G.generators:
        perm = []
        for i, c in enumerate(reps):
            cg = c * g
            for j, r in enumerate(reps):
                if (cg * ~r) in N:
                    perm.append(j)
                    break
        gens.append(Permutation(perm))
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(N1.is_subgroup(G1) and N1.is_normal(G1))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(N2.is_subgroup(G2) and N2.is_normal(G2))
    except Exception:
        h2 = False
        
    try:
        G1xG2 = direct_product(G1, G2)
        N1xN2 = direct_product(N1, N2)
        
        if not N1xN2.is_subgroup(G1xG2):
            neg_q = True
        elif not N1xN2.is_normal(G1xG2):
            neg_q = True
        else:
            Q_prod = quotient_group(G1xG2, N1xN2)
            Q1 = quotient_group(G1, N1)
            Q2 = quotient_group(G2, N2)
            Q1xQ2 = direct_product(Q1, Q2)
            
            if not Q_prod.is_isomorphic(Q1xQ2):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N_1 is a normal subgroup of G_1",
    "H_2: N_2 is a normal subgroup of G_2",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient group is not isomorphic to (G_1/N_1) x (G_2/N_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2