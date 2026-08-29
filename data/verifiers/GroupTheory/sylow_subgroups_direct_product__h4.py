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

def is_sylow_p_subgroup(sub, grp, p):
    try:
        if not hasattr(sub, 'generators') or not hasattr(grp, 'generators'):
            return False
        if not hasattr(sub, 'order') or not hasattr(grp, 'order'):
            return False
            
        # Check if sub is a subgroup of grp by verifying all generators are in grp
        for g in sub.generators:
            if g not in grp:
                return False
        
        order_grp = int(grp.order())
        order_sub = int(sub.order())
        
        # Sylow p-subgroup conditions:
        # 1. order_sub must divide order_grp
        if order_grp % order_sub != 0:
            return False
            
        # 2. The index of sub in grp must not be divisible by p
        if (order_grp // order_sub) % p == 0:
            return False
            
        # 3. order_sub must be a power of p
        temp = order_sub
        while temp % p == 0 and temp > 1:
            temp = temp // p
        if temp != 1:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, p, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G and H are finite groups
    try:
        h1 = hasattr(G, 'order') and hasattr(H, 'order') and hasattr(G, 'generators') and hasattr(H, 'generators')
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        h3 = is_sylow_p_subgroup(P, G, p)
    except Exception:
        h3 = False
        
    # ¬Q: P x Q is not a Sylow p-subgroup of G x H
    # Given P is a Sylow p-subgroup of G, P x Q is a Sylow p-subgroup of G x H 
    # if and only if Q is a Sylow p-subgroup of H.
    try:
        neg_q = not is_sylow_p_subgroup(Q, H, p)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P x Q is not a Sylow p-subgroup of G x H"
]

N_HYP = 3
NEG_Q_INDEX = 3