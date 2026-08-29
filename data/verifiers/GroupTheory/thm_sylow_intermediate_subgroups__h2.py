import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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

def count_sylow(G, P):
    """
    Counts the number of Sylow p-subgroups conjugate to P in G.
    This is equal to the index of the normalizer of P in G: [G : N_G(P)].
    """
    N_G_P_order = 0
    P_gens = P.generators
    for g in G.generate():
        normalizes = True
        for x in P_gens:
            conj = g * x * (~g)
            if not P.contains(conj):
                normalizes = False
                break
        if normalizes:
            N_G_P_order += 1
    return G.order() // N_G_P_order

def conditions(witness):
    try:
        G, P, H, p = witness
        if not isinstance(p, int) or p <= 1:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isprime(p):
            h2 = False
        elif not P.is_subgroup(G):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            while order_G % (p**(k+1)) == 0:
                k += 1
            h2 = (order_P == p**k)
    except Exception:
        h2 = False
        
    # H_3: H is a subgroup of G that contains P
    try:
        h3 = H.is_subgroup(G) and P.is_subgroup(H)
    except Exception:
        h3 = False
        
    # ¬Q: P is not a Sylow p-subgroup of H, or the number of Sylow p-subgroups of H 
    # does not divide the number of Sylow p-subgroups of G
    try:
        order_H = H.order()
        order_P = P.order()
        k = 0
        while order_H % (p**(k+1)) == 0:
            k += 1
        is_sylow_in_H = P.is_subgroup(H) and (order_P == p**k)
        
        if not is_sylow_in_H:
            neg_q = True
        else:
            n_p_G = count_sylow(G, P)
            n_p_H = count_sylow(H, P)
            neg_q = (n_p_G % n_p_H != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: H is a subgroup of G that contains P",
    "¬Q: P is not a Sylow p-subgroup of H, or the number of Sylow p-subgroups of H does not divide the number of Sylow p-subgroups of G"
]

N_HYP = 3
NEG_Q_INDEX = 3