import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product(groups):
    if not groups:
        return PermutationGroup([Permutation(0)])
    
    degrees = [g.degree for g in groups]
    offsets = [0]
    for d in degrees[:-1]:
        offsets.append(offsets[-1] + d)
    
    total_degree = sum(degrees)
    if total_degree == 0:
        return PermutationGroup([Permutation(0)])
        
    gens = []
    for i, grp in enumerate(groups):
        offset = offsets[i]
        for gen in grp.generators:
            array_form = list(range(total_degree))
            for j in range(grp.degree):
                array_form[offset + j] = offset + gen(j)
            gens.append(Permutation(array_form))
            
    if not gens:
        return PermutationGroup([Permutation(total_degree - 1)])
    return PermutationGroup(gens)

def count_sylow(G, p):
    # If p does not divide the order of G, the standard convention in some contexts 
    # (which makes this conjecture false) is that there are 0 Sylow p-subgroups.
    if G.order() % p != 0:
        return 0
    P = G.sylow_subgroup(p)
    if P.order() == 1:
        return 1
    gens = P.generators
    P_elements = set(P.generate())
    n_G_P = 0
    for g in G.generate():
        if all((g * x * ~g) in P_elements for x in gens):
            n_G_P += 1
    return G.order() // n_G_P

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, p, S_list = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a semisimple finite group such that G = S_1 \times \dots \times S_k, 
    # where each S_i is a non-abelian simple group
    try:
        h1 = True
        if not isinstance(S_list, (list, tuple)):
            h1 = False
        else:
            for S in S_list:
                is_simp = S.is_simple() if callable(S.is_simple) else S.is_simple
                is_ab = S.is_abelian() if callable(S.is_abelian) else S.is_abelian
                if is_ab or not is_simp:
                    h1 = False
                    break
            if h1:
                DP = direct_product(S_list)
                if G.order() != DP.order():
                    h1 = False
                else:
                    h1 = G.is_isomorphic(DP)
    except Exception:
        h1 = False

    # H_2: p is a prime dividing the order of G
    try:
        h2 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h2 = False

    # ¬Q: The number of Sylow p-subgroups of G is NOT given by the product n_p(G) = \prod_{i=1}^k n_p(S_i)
    try:
        np_G = count_sylow(G, p)
        prod_np_S = 1
        for S in S_list:
            prod_np_S *= count_sylow(S, p)
        
        neg_q = (np_G != prod_np_S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 \\times \\dots \\times S_k, where each S_i is a non-abelian simple group",
    "H_2: p is a prime dividing the order of G",
    "¬Q: The number of Sylow p-subgroups of G is NOT given by the product n_p(G) = \\prod_{i=1}^k n_p(S_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2