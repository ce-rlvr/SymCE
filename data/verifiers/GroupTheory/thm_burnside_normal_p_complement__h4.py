import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            is_sub = all(g in G for g in P.generators)
            if not is_sub:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                while temp % p == 0:
                    k += 1
                    temp //= p
                h3 = (order_P == p**k)
    except Exception:
        h3 = False

    # ¬Q: G does not have a normal p-complement
    try:
        order_G = G.order()
        order_P = P.order()
        m = order_G // order_P
        
        # A normal p-complement is a normal subgroup of order m.
        # If it exists, it must be exactly the set of all elements whose order divides m.
        N_gens = [g for g in G.elements if m % g.order() == 0]
        
        if not N_gens:
            N_order = 1
        else:
            N = PermutationGroup(N_gens)
            N_order = N.order()
            
        has_normal_p_complement = (N_order == m)
        neg_q = not has_normal_p_complement
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: G does not have a normal p-complement"
]

N_HYP = 3
NEG_Q_INDEX = 3