import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.combinatorics as comb
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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G, p, P, N = witness['G'], witness['p'], witness['P'], witness['N']
        else:
            if isinstance(witness[0], int):
                p, P, G, N = witness
            elif isinstance(witness[1], int):
                G, p, P, N = witness
            else:
                G, p, P, N = witness
    except Exception:
        return [False] * 5

    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    try:
        h2 = False
        if hasattr(P, 'is_sylow'):
            h2 = P.is_sylow(G, p)
        elif hasattr(G, 'is_sylow'):
            h2 = G.is_sylow(P, p)
        else:
            if isinstance(P, list):
                P = comb.PermutationGroup(P)
            is_sub = all(g in G for g in P.generators)
            order_G = G.order()
            order_P = P.order()
            
            is_p_group = False
            if order_P > 0:
                temp = order_P
                while temp % p == 0:
                    temp //= p
                is_p_group = (temp == 1)
                
            is_highest = (order_G % order_P == 0) and ((order_G // order_P) % p != 0)
            h2 = is_sub and is_p_group and is_highest
    except Exception:
        h2 = False

    try:
        h3 = False
        if hasattr(N, 'is_normal'):
            try:
                h3 = N.is_normal(G)
            except TypeError:
                h3 = N.is_normal()
        elif hasattr(G, 'is_normal'):
            h3 = G.is_normal(N)
        else:
            if isinstance(N, list):
                N = comb.PermutationGroup(N)
            is_sub_N = all(g in G for g in N.generators)
            is_normal = True
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N or (~g * n * g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h3 = is_sub_N and is_normal
    except Exception:
        h3 = False

    try:
        h4 = False
        index = None
        if hasattr(G, 'index'):
            index = G.index(N)
        elif hasattr(N, 'index_in'):
            index = N.index_in(G)
        else:
            order_G = G.order()
            order_N = N.order()
            if order_G % order_N == 0:
                index = order_G // order_N
                
        if index is not None and index >= 1:
            temp = index
            while temp % p == 0 and temp > 1:
                temp //= p
            h4 = (temp == 1)
    except Exception:
        h4 = False

    try:
        neg_q = False
        if hasattr(G, 'equals_product'):
            neg_q = not G.equals_product(P, N)
        elif hasattr(P, 'product_equals'):
            neg_q = not P.product_equals(N, G)
        else:
            order_G = G.order()
            order_P = P.order()
            order_N = N.order()
            
            try:
                int_order = P.intersection(N).order()
            except Exception:
                if order_P < order_N:
                    int_order = sum(1 for x in P.elements if x in N)
                else:
                    int_order = sum(1 for x in N.elements if x in P)
                    
            order_PN = (order_P * order_N) // int_order
            
            is_P_sub = all(g in G for g in P.generators)
            is_N_sub = all(g in G for g in N.generators)
            
            if not (is_P_sub and is_N_sub):
                neg_q = True
            else:
                neg_q = (order_G != order_PN)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: N is a normal subgroup of G",
    "H_4: The index of N in G is a power of p",
    "¬Q: G != PN"
]

N_HYP = 4
NEG_Q_INDEX = 4