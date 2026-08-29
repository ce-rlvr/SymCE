import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, N, H, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        if not (isinstance(G, PermutationGroup) and 
                isinstance(N, PermutationGroup) and 
                isinstance(H, PermutationGroup)):
            h1 = False
        else:
            is_N_sub = N.is_subgroup(G)
            is_N_norm = N.is_normal(G)
            is_H_sub = H.is_subgroup(G)
            
            gens = list(N.generators) + list(H.generators)
            G_gen = PermutationGroup(gens)
            
            generates_G = (G_gen.order() == G.order())
            order_cond = (N.order() * H.order() == G.order())
            
            h1 = bool(is_N_sub and is_N_norm and is_H_sub and generates_G and order_cond)
    except Exception:
        h1 = False

    # H_2: n H n^{-1} = H
    try:
        if not isinstance(n, Permutation):
            h2 = False
        elif n not in G:
            h2 = False
        else:
            h2 = bool(all((n * h * ~n) in H for h in H.generators))
    except Exception:
        h2 = False

    # neg_Q: There exists h in H such that n h n^{-1} != h
    try:
        if not (isinstance(H, PermutationGroup) and isinstance(n, Permutation)):
            neg_q = False
        else:
            neg_q = bool(any((n * h * ~n) != h for h in H.generators))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: n H n^{-1} = H",
    "¬Q: There exists h in H such that n h n^{-1} != h"
]

N_HYP = 2
NEG_Q_INDEX = 2