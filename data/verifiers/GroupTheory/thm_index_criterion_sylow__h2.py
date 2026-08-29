import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'generators') and hasattr(G, 'order')
        if h1:
            order_G = int(G.order())
            h1 = order_G > 0
    except Exception:
        h1 = False

    # H2: P is a subgroup of G such that the order of P is a power of p
    try:
        is_sub = None
        if hasattr(P, 'is_subgroup'):
            try:
                is_sub = P.is_subgroup(G)
            except Exception:
                pass
        
        if is_sub is None:
            if hasattr(P, 'generators'):
                is_sub = True
                for g in P.generators:
                    if g not in G:
                        is_sub = False
                        break
            else:
                is_sub = False
        
        is_pow = False
        if is_sub:
            order_P = int(P.order())
            try:
                p_int = int(p)
            except Exception:
                p_int = p
            
            if order_P == 1:
                is_pow = True
            elif p_int in (0, 1, -1):
                is_pow = False
            else:
                for k in range(1000):
                    if p_int**k == order_P:
                        is_pow = True
                        break
                    if abs(p_int)**k > order_P:
                        break
        h2 = bool(is_sub and is_pow)
    except Exception:
        h2 = False

    # H3: p does not divide the index of P in G
    try:
        h3 = False
        if is_sub:
            order_G = int(G.order())
            order_P = int(P.order())
            index = order_G // order_P
            try:
                p_int = int(p)
            except Exception:
                p_int = p
            
            if p_int == 0:
                h3 = True
            else:
                h3 = (index % p_int != 0)
    except Exception:
        h3 = False

    # neg_Q: P is NOT a Sylow p-subgroup of G
    try:
        is_sylow = False
        try:
            p_int = int(p)
        except Exception:
            p_int = p
            
        # A Sylow p-subgroup is only defined for primes p.
        # If p is prime, P is a Sylow p-subgroup iff it is a p-subgroup and p does not divide the index.
        if sympy.isprime(p_int):
            if is_sub and is_pow:
                order_G = int(G.order())
                order_P = int(P.order())
                index = order_G // order_P
                if index % p_int != 0:
                    is_sylow = True
        neg_q = not is_sylow
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a subgroup of G such that the order of P is a power of p",
    "H_3: p does not divide the index of P in G",
    "¬Q: P is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3