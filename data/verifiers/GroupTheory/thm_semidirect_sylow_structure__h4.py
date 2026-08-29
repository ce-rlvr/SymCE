import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy import isprime
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(sub, grp):
    try:
        return sub.is_subgroup(grp)
    except Exception:
        try:
            for gen in sub.generators:
                if gen not in grp:
                    return False
            return True
        except Exception:
            return False

def is_normal_subgroup(sub, grp):
    if not is_subgroup(sub, grp):
        return False
    try:
        return sub.is_normal(grp)
    except Exception:
        try:
            for g in grp.generators:
                g_inv = ~g
                for h in sub.generators:
                    if (g * h * g_inv) not in sub:
                        return False
            return True
        except Exception:
            return False

def get_order(g):
    try:
        try:
            if callable(g.order):
                return g.order()
            return g.order
        except Exception:
            return len(list(g.elements))
    except Exception:
        return 0

def conditions(witness):
    try:
        G = witness['G']
        N = witness['N']
        H = witness['H']
        p = witness['p']
        P_N = witness['P_N']
        P_H = witness['P_H']
    except Exception:
        return [False, False, False, False]

    # H1: G = N \rtimes H is a finite semidirect product
    try:
        if not (is_subgroup(N, G) and is_subgroup(H, G)):
            h1 = False
        else:
            cond3 = is_normal_subgroup(N, G)
            try:
                inter_order = get_order(N.intersect(H))
            except Exception:
                s1 = set(N.elements)
                s2 = set(H.elements)
                inter_order = len(s1.intersection(s2))
            cond4 = inter_order == 1
            cond5 = get_order(G) == get_order(N) * get_order(H)
            h1 = cond3 and cond4 and cond5
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H3: P_N is a normal Sylow p-subgroup of N
    try:
        if not is_subgroup(P_N, N):
            h3 = False
        else:
            cond1 = is_normal_subgroup(P_N, N)
            
            ord_PN = get_order(P_N)
            ord_N = get_order(N)
            
            temp = ord_PN
            is_power = True
            if temp < 1:
                is_power = False
            else:
                while temp > 1:
                    if temp % p != 0:
                        is_power = False
                        break
                    temp //= p
                    
            is_maximal = (ord_N // ord_PN) % p != 0
            
            h3 = cond1 and is_power and is_maximal
    except Exception:
        h3 = False

    # neg_Q: P_N \rtimes P_H is NOT a Sylow p-subgroup of G
    try:
        if not is_subgroup(P_H, H):
            concl = False
        else:
            try:
                inter_order = get_order(P_N.intersect(P_H))
            except Exception:
                s1 = set(P_N.elements)
                s2 = set(P_H.elements)
                inter_order = len(s1.intersection(s2))
                
            if inter_order != 1:
                concl = False
            else:
                ord_prod = get_order(P_N) * get_order(P_H)
                ord_G = get_order(G)
                sylow_order = 1
                temp = ord_G
                while temp % p == 0:
                    sylow_order *= p
                    temp //= p
                    
                if ord_prod == sylow_order:
                    concl = True
                else:
                    concl = False
        neg_q = not concl
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G = N ⋊ H is a finite semidirect product",
    "H_2: p is a prime number",
    "H_3: P_N is a normal Sylow p-subgroup of N",
    "¬Q: P_N ⋊ P_H is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3