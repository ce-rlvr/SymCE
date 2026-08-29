import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_composition_series(S, G):
    try:
        if not S: 
            return False
        if S[0].order() != G.order(): 
            return False
        try:
            if not S[0].is_subgroup(G) or not G.is_subgroup(S[0]):
                return False
        except Exception:
            return False
            
        if S[-1].order() != 1:
            return False
            
        for i in range(len(S) - 1):
            K = S[i]
            H = S[i+1]
            if not H.is_subgroup(K): 
                return False
            
            # Check normality
            is_norm = True
            for k in K.generators:
                for h in H.generators:
                    if (k * h * ~k) not in H:
                        is_norm = False
                        break
                if not is_norm: 
                    break
            if not is_norm: 
                return False
            
            if H.order() == K.order(): 
                return False
            
            # Check maximal normal
            idx = K.order() // H.order()
            if isprime(idx):
                continue
                
            maximal = True
            for N in K.normal_subgroups():
                if H.order() < N.order() < K.order():
                    if H.is_subgroup(N):
                        maximal = False
                        break
            if not maximal:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, S1, S2 = witness
        elif len(witness) == 2:
            S1, S2 = witness
            G = S1[0]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = is_composition_series(S1, G) and is_composition_series(S2, G)
    except Exception:
        h1 = False
        
    try:
        if len(S1) != len(S2):
            neg_q = True
        else:
            factors1 = sorted([S1[i].order() // S1[i+1].order() for i in range(len(S1)-1)])
            factors2 = sorted([S2[i].order() // S2[i+1].order() for i in range(len(S2)-1)])
            neg_q = (factors1 != factors2)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S_1 and S_2 are composition series of G",
    "¬Q: S_1 and S_2 have different lengths or non-isomorphic composition factors"
]

N_HYP = 1
NEG_Q_INDEX = 1