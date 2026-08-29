import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        if hasattr(H, 'is_subgroup'):
            res = H.is_subgroup(G)
            if res is not None:
                return bool(res)
    except Exception:
        pass
    try:
        for g in H.generators:
            if g not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(H, G):
    if not is_subgroup(H, G):
        return False
    try:
        for g in G.generators:
            g_inv = g**-1
            for h in H.generators:
                if (g * h * g_inv) not in H:
                    return False
        return True
    except Exception:
        return False

def check_nilpotent(N):
    try:
        if hasattr(N, 'is_nilpotent'):
            if callable(N.is_nilpotent):
                return bool(N.is_nilpotent())
            return bool(N.is_nilpotent)
        return False
    except Exception:
        return False

def is_sylow_p(P, N, p):
    if not is_subgroup(P, N):
        return False
    try:
        order_N = N.order()
        order_P = P.order()
        
        if order_P == 1:
            return order_N % p != 0
            
        temp = order_P
        while temp % p == 0:
            temp //= p
        if temp != 1:
            return False
            
        index = order_N // order_P
        if index % p == 0:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, p, P = witness
    except Exception:
        return [False] * 5
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = is_normal(N, G)
    except Exception:
        h1 = False
        
    # H_2: N is a nilpotent group
    try:
        h2 = check_nilpotent(N)
    except Exception:
        h2 = False
        
    # H_3: p is a prime number
    try:
        h3 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h3 = False
        
    # H_4: P is a Sylow p-subgroup of N
    try:
        h4 = is_sylow_p(P, N, p)
    except Exception:
        h4 = False
        
    # ¬Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal(P, G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a nilpotent group",
    "H_3: p is a prime number",
    "H_4: P is a Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4