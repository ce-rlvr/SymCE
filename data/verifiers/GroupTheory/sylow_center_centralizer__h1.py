import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, P, p = witness
    except Exception:
        return [False, False]
        
    # H_1: P is a Sylow p-subgroup of G
    try:
        if not isprime(p):
            h1 = False
        else:
            try:
                is_sub = P.is_subgroup(G)
            except Exception:
                is_sub = True
                for g in P.generators:
                    if g not in G:
                        is_sub = False
                        break
            if not is_sub:
                h1 = False
            else:
                n = G.order()
                k = 0
                while n > 0 and n % p == 0:
                    k += 1
                    n //= p
                h1 = (P.order() == p**k)
    except Exception:
        h1 = False
        
    # ¬Q: Z(P) is not a Sylow p-subgroup of C_G(P)
    try:
        if not h1:
            neg_q = False
        else:
            try:
                cgp_order = G.centralizer(P).order()
            except Exception:
                P_gens = P.generators
                cgp_order = 0
                for g in G.elements:
                    if all(g * x == x * g for x in P_gens):
                        cgp_order += 1
                        
            try:
                zp_order = P.center().order()
            except Exception:
                P_gens = P.generators
                zp_order = 0
                for g in P.elements:
                    if all(g * x == x * g for x in P_gens):
                        zp_order += 1
                        
            m = 0
            n = cgp_order
            while n > 0 and n % p == 0:
                m += 1
                n //= p
                
            neg_q = (zp_order != p**m)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]