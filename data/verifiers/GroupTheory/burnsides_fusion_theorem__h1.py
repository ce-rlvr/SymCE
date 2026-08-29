import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, P, x, y = witness
    except Exception:
        return [False, False, False, False]

    def get_elements(group):
        try:
            if hasattr(group, 'elements'):
                elems = group.elements
                if callable(elems):
                    return elems()
                return elems
            return list(group)
        except Exception:
            return []

    def get_inv(g):
        try:
            return g**-1
        except Exception:
            return ~g

    def check_H1():
        try:
            if hasattr(G, 'is_sylow_p_subgroup'):
                return G.is_sylow_p_subgroup(P)
            if hasattr(P, 'is_sylow_p_subgroup'):
                return P.is_sylow_p_subgroup(G)
            
            if hasattr(P, 'is_subgroup'):
                if not P.is_subgroup(G):
                    return False
            else:
                gens = P.generators if hasattr(P, 'generators') else get_elements(P)
                for g in gens:
                    if hasattr(G, 'contains'):
                        if not G.contains(g):
                            return False
                    else:
                        if g not in get_elements(G):
                            return False
                            
            order_P = P.order() if hasattr(P, 'order') else len(get_elements(P))
            if order_P == 1:
                return True
            
            factors = factorint(order_P)
            if len(factors) != 1:
                return False
            p = list(factors.keys())[0]
            
            order_G = G.order() if hasattr(G, 'order') else len(get_elements(G))
            if order_G == sympy.oo:
                return False
            if order_G % (p * order_P) == 0:
                return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            if hasattr(P, 'contains'):
                if not P.contains(x) or not P.contains(y):
                    return False
            else:
                elems_P = get_elements(P)
                if x not in elems_P or y not in elems_P:
                    return False
            
            gens = P.generators if hasattr(P, 'generators') else get_elements(P)
                
            for g in gens:
                if g * x != x * g:
                    return False
                if g * y != y * g:
                    return False
            return True
        except Exception:
            return False

    def check_H3():
        try:
            if hasattr(G, 'are_conjugate'):
                return G.are_conjugate(x, y)
            for g in get_elements(G):
                ginv = get_inv(g)
                if g * x * ginv == y:
                    return True
            return False
        except Exception:
            return False

    def check_neg_Q():
        try:
            if hasattr(G, 'normalizer'):
                N = G.normalizer(P)
                if hasattr(N, 'are_conjugate'):
                    return not N.are_conjugate(x, y)
                for n in get_elements(N):
                    ninv = get_inv(n)
                    if n * x * ninv == y:
                        return False
                return True
            
            gens = P.generators if hasattr(P, 'generators') else get_elements(P)
                
            for g in get_elements(G):
                ginv = get_inv(g)
                if g * x * ginv == y:
                    normalizes = True
                    for p in gens:
                        conj = g * p * ginv
                        if hasattr(P, 'contains'):
                            if not P.contains(conj):
                                normalizes = False
                                break
                        else:
                            if conj not in get_elements(P):
                                normalizes = False
                                break
                    if normalizes:
                        return False
            return True
        except Exception:
            return False

    return [check_H1(), check_H2(), check_H3(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "H_2: x and y are elements in the center of P",
    "H_3: x and y are conjugate in G",
    "¬Q: x and y are not conjugate in the normalizer N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3