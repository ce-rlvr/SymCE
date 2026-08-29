import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a group, N is a normal subgroup of G
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not isinstance(N, PermutationGroup):
            h1 = False
        elif not N.is_subgroup(G):
            h1 = False
        elif not N.is_normal(G):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: The quotient group G/N is a cyclic group
    try:
        if h1:
            h2 = False
            target_order = G.order()
            n_gens = list(N.generators)
            # G/N is cyclic iff there exists g in G such that <N, g> = G
            for g in G.elements:
                H_g = PermutationGroup(*(n_gens + [g]))
                if H_g.order() == target_order:
                    h2 = True
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The derived subgroup G' is NOT cyclic OR G' is NOT contained in N
    try:
        if h1:
            G_prime = G.derived_subgroup()
            
            gp_order = G_prime.order()
            gp_is_cyclic = False
            for g in G_prime.elements:
                if g.order() == gp_order:
                    gp_is_cyclic = True
                    break
            
            gp_in_N = G_prime.is_subgroup(N)
            
            neg_q = not (gp_is_cyclic and gp_in_N)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N is a normal subgroup of G",
    "H_2: The quotient group G/N is a cyclic group",
    "¬Q: The derived subgroup G' is not cyclic or not contained in N"
]

N_HYP = 2
NEG_Q_INDEX = 2