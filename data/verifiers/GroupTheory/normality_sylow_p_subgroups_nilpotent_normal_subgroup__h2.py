import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        return all(g in G for g in H.generators)
    except Exception:
        return False

def is_normal(P, G):
    try:
        if hasattr(P, 'is_normal'):
            return P.is_normal(G)
    except Exception:
        pass
    try:
        for g in G.generators:
            for h in P.generators:
                if g * h * ~g not in P:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, p, P = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(P, PermutationGroup) and 
              is_subgroup(N, G) and 
              is_subgroup(P, G))
    except Exception:
        h1 = False
        
    # H_2: N is a nilpotent group
    try:
        h2 = N.is_nilpotent() if callable(N.is_nilpotent) else N.is_nilpotent
    except Exception:
        h2 = False
        
    # H_3: p is a prime number
    try:
        h3 = sympy.isprime(p)
    except Exception:
        h3 = False
        
    # H_4: P is a Sylow p-subgroup of N
    try:
        if not is_subgroup(P, N):
            h4 = False
        else:
            order_N = N.order() if callable(N.order) else N.order
            order_P = P.order() if callable(P.order) else P.order
            k = 0
            while order_N % (p**(k+1)) == 0:
                k += 1
            h4 = (order_P == p**k)
    except Exception:
        h4 = False
        
    # ¬Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal(P, G)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a nilpotent group",
    "H_3: p is a prime number",
    "H_4: P is a Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4