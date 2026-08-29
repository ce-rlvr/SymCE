import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def get_order(obj):
    if hasattr(obj, 'order'):
        if callable(obj.order):
            return obj.order()
        return obj.order
    return len(obj)

def conditions(witness) -> list[bool]:
    try:
        G, p, P, n_p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number dividing the order of G
    try:
        if not isprime(p):
            h1 = False
        else:
            ord_G = get_order(G)
            h1 = bool(ord_G % p == 0)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if hasattr(P, 'is_subgroup'):
            if callable(P.is_subgroup):
                is_sub = P.is_subgroup(G)
            else:
                is_sub = P.is_subgroup
        else:
            is_sub = True
            
        ord_G = get_order(G)
        ord_P = get_order(P)
        
        if ord_G == 0:
            h2 = False
        else:
            k = 0
            temp_G = ord_G
            while temp_G % p == 0:
                temp_G //= p
                k += 1
            h2 = bool(is_sub and (ord_P == p**k))
    except Exception:
        h2 = False

    # H_3: n_p is the number of Sylow p-subgroups of G
    try:
        ord_G = get_order(G)
        if ord_G == 0:
            h3 = False
        else:
            k = 0
            temp_G = ord_G
            while temp_G % p == 0:
                temp_G //= p
                k += 1
            target_order = p**k

            if hasattr(G, 'sylow_p_subgroups'):
                if callable(G.sylow_p_subgroups):
                    actual_n_p = len(G.sylow_p_subgroups(p))
                else:
                    actual_n_p = len(G.sylow_p_subgroups)
            elif hasattr(G, 'subgroups'):
                if callable(G.subgroups):
                    subs = G.subgroups()
                else:
                    subs = G.subgroups
                actual_n_p = sum(1 for H in subs if get_order(H) == target_order)
            else:
                # Fallback for standard SymPy PermutationGroup
                if hasattr(G, 'normalizer'):
                    if callable(G.normalizer):
                        N = G.normalizer(P)
                    else:
                        N = G.normalizer
                else:
                    N = P
                actual_n_p = ord_G // get_order(N)
            
            h3 = bool(n_p == actual_n_p)
    except Exception:
        h3 = False

    # ¬Q: The index of the normalizer N_G(P) in G is not equal to n_p
    try:
        if hasattr(G, 'normalizer'):
            if callable(G.normalizer):
                N = G.normalizer(P)
            else:
                N = G.normalizer
        else:
            N = P
            
        ord_G = get_order(G)
        ord_N = get_order(N)
        index = ord_G // ord_N
        neg_q = bool(index != n_p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: n_p is the number of Sylow p-subgroups of G",
    "¬Q: The index of the normalizer N_G(P) in G is not equal to n_p"
]

N_HYP = 3
NEG_Q_INDEX = 3