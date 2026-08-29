import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
import math
import itertools
import functools

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

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False, False]
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: P is a subgroup of G
    try:
        h2 = isinstance(P, PermutationGroup) and all(g in G for g in P.generators)
    except Exception:
        h2 = False
        
    # H_3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False
        
    # ¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)
    try:
        if not isinstance(p, int) or p <= 1:
            neg_q = False
        else:
            P_gens = P.generators
            
            z_p_order = 0
            for g in P.generate():
                commutes = True
                for h in P_gens:
                    if g * h != h * g:
                        commutes = False
                        break
                if commutes:
                    z_p_order += 1
                    
            c_g_p_order = 0
            for g in G.generate():
                commutes = True
                for h in P_gens:
                    if g * h != h * g:
                        commutes = False
                        break
                if commutes:
                    c_g_p_order += 1
                    
            is_p_group = True
            temp = z_p_order
            if temp <= 0:
                is_p_group = False
            else:
                while temp % p == 0 and temp > 1:
                    temp //= p
                if temp != 1:
                    is_p_group = False
                    
            if c_g_p_order % z_p_order != 0:
                is_sylow = False
            else:
                index = c_g_p_order // z_p_order
                if index % p == 0:
                    is_sylow = False
                else:
                    is_sylow = is_p_group
                    
            neg_q = not is_sylow
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a subgroup of G",
    "H_3: p is a prime number",
    "¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3