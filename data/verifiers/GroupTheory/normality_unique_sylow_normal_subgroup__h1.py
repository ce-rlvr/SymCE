import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(G, N):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g) not in N:
                    return False
                if (~g * n * g) not in N:
                    return False
        return True
    except Exception:
        return False

def is_sylow_p_subgroup(N, P, p):
    try:
        if p <= 1:
            return False
        if not is_subgroup(P, N):
            return False
        
        try:
            order_N = N.order()
        except TypeError:
            order_N = N.order
            
        try:
            order_P = P.order()
        except TypeError:
            order_P = P.order
            
        k = 0
        temp = order_N
        while temp % p == 0 and temp > 0:
            k += 1
            temp //= p
            
        return order_P == p**k
    except Exception:
        return False

def is_unique_sylow(N, P, p):
    try:
        if not is_sylow_p_subgroup(N, P, p):
            return False
        # In finite groups, a Sylow p-subgroup is unique if and only if it is normal
        return is_normal(N, P)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = is_normal(G, N)
    except Exception:
        h2 = False
        
    # H_3: P is the unique Sylow p-subgroup of N
    try:
        h3 = is_unique_sylow(N, P, p)
    except Exception:
        h3 = False
        
    # ¬Q: P is NOT a normal subgroup of G
    try:
        neg_q = not is_normal(G, P)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a normal subgroup of G",
    "H_3: P is the unique Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3