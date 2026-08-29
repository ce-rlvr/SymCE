import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, p, P, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing the order of G
    try:
        order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
        h2 = isprime(p) and order_G % p == 0
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not P.is_subgroup(G):
            h3 = False
        else:
            order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
            order_P = P.order() if callable(getattr(P, 'order', None)) else P.order
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h3 = (order_P == p**k)
    except Exception:
        h3 = False

    # H_4: x and y are elements in the center Z(P) of P
    try:
        def in_center(grp, elem):
            if not grp.contains(elem):
                return False
            for g in grp.generators:
                if elem * g != g * elem:
                    return False
            return True
        h4 = in_center(P, x) and in_center(P, y)
    except Exception:
        h4 = False

    # ¬Q: There does not exist n in N_G(P) such that n x n^{-1} = y
    try:
        def normalizes(n, grp):
            for g in grp.generators:
                if not grp.contains(n * g * ~n):
                    return False
            return True

        neg_q = True
        elements = G.elements if hasattr(G, 'elements') else list(G.generate())
        for n in elements:
            if n * x * ~n == y:
                if normalizes(n, P):
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: x and y are elements in the center Z(P) of P",
    "¬Q: There does not exist n in N_G(P) such that n x n^{-1} = y"
]

N_HYP = 4
NEG_Q_INDEX = 4