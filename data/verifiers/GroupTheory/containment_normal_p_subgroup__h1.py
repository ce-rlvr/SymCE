import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools
import z3
from sympy.abc import x, y, z

# Top-level setup: named object bindings
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

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(G, N):
    try:
        if hasattr(G, 'is_normal'):
            return G.is_normal(N)
    except Exception:
        pass
    try:
        if hasattr(N, 'is_normal'):
            return N.is_normal(G)
    except Exception:
        pass
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            for n in N.generators:
                if (~g * n * g) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) >= 3:
            G, P, N = witness[:3]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: P is a Sylow p-subgroup of G (for some prime p)
    h1 = False
    try:
        if is_subgroup(P, G):
            order_P = P.order()
            order_G = G.order()
            if order_P == 1:
                h1 = True
            else:
                factors = sympy.ntheory.factorint(order_P)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                    k = factors[p]
                    if order_G % (p**(k+1)) != 0:
                        h1 = True
    except Exception:
        pass

    # H2: N is a normal p-subgroup of G (for some prime q)
    h2 = False
    try:
        if is_subgroup(N, G) and is_normal(G, N):
            order_N = N.order()
            if order_N == 1:
                h2 = True
            else:
                factors = sympy.ntheory.factorint(order_N)
                if len(factors) == 1:
                    h2 = True
    except Exception:
        pass

    # ¬Q: N is NOT a subgroup of P
    neg_q = False
    try:
        neg_q = not is_subgroup(N, P)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "H_2: N is a normal p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 2
NEG_Q_INDEX = 2