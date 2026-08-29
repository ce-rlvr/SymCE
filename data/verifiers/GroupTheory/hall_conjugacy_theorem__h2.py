import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint, isprime
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

def is_hall_pi_subgroup(G, H, pi):
    if not isinstance(H, PermutationGroup):
        return False
    
    # Check if H is a subgroup of G
    for gen in H.generators:
        if not G.contains(gen):
            return False
            
    order_H = H.order()
    order_G = G.order()
    
    if order_G % order_H != 0:
        return False
        
    index = order_G // order_H
    
    # Check if |H| is a pi-number
    factors_H = factorint(order_H)
    for p in factors_H:
        if p not in pi:
            return False
            
    # Check if [G : H] is a pi'-number
    factors_index = factorint(index)
    for p in factors_index:
        if p in pi:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        G, pi, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: pi is a set of prime numbers
    try:
        if isinstance(pi, (set, list, tuple)):
            h2 = all(isprime(p) for p in pi)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: H and K are Hall pi-subgroups of G
    try:
        h3 = is_hall_pi_subgroup(G, H, pi) and is_hall_pi_subgroup(G, K, pi)
    except Exception:
        h3 = False
        
    # ¬Q: H and K are NOT conjugate in G
    try:
        if not (isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)):
            neg_q = False
        elif H.order() != K.order():
            neg_q = True
        else:
            H_gens = H.generators
            are_conjugate = False
            for g in G.elements:
                conjugate_gens_in_K = True
                for h in H_gens:
                    conj = g * h * ~g
                    if not K.contains(conj):
                        conjugate_gens_in_K = False
                        break
                if conjugate_gens_in_K:
                    are_conjugate = True
                    break
            neg_q = not are_conjugate
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: pi is a set of prime numbers",
    "H_3: H and K are Hall pi-subgroups of G",
    "¬Q: H and K are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3