import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

NON_ABELIAN_SIMPLE_ORDERS = {
    60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080, 5616, 6048, 6072, 7800, 7920, 9828
}

def is_non_abelian_simple_order(n):
    if n < 60:
        return False
    return n in NON_ABELIAN_SIMPLE_ORDERS

def is_subgroup(H, G):
    for h in H.generators:
        if h not in G:
            return False
    return True

def is_maximal_normal(G, M):
    if M.order() >= G.order():
        return False
    if not is_subgroup(M, G):
        return False
    for g in G.generators:
        for m in M.generators:
            if (g * m * (g**-1)) not in M:
                return False
            
    for x in list(G.generate()):
        if x in M:
            continue
        gens = list(M.generators) + [x]
        H = PermutationGroup(gens)
        while True:
            order_before = H.order()
            for g in G.generators:
                for h in list(H.generators):
                    conj = g * h * (g**-1)
                    if conj not in H:
                        gens.append(conj)
            H = PermutationGroup(gens)
            if H.order() == order_before:
                break
        if H.order() < G.order():
            return False
    return True

def conditions(witness):
    try:
        G, M = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_maximal_normal(G, M)
    except Exception:
        h1 = False
        
    try:
        index = G.order() // M.order()
        neg_q = not is_non_abelian_simple_order(index)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal normal subgroup of G",
    "¬Q: The index of M in G is NOT equal to the order of a non-abelian simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1