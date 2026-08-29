import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
from sympy import S, oo
import math
import itertools
import functools

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

def is_cyclic(G):
    if G == 'Z' or G is S.Integers:
        return True
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators) == 1
    try:
        if hasattr(G, 'is_cyclic'):
            return G.is_cyclic
        if hasattr(G, 'is_Cyclic'):
            return G.is_Cyclic
        order = G.order()
        for g in G.elements:
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def group_order(G):
    if G == 'Z' or G is S.Integers:
        return oo
    if type(G).__name__ == 'FreeGroup':
        return oo
    try:
        return G.order()
    except Exception:
        return None

def num_generators(G):
    if G == 'Z' or G is S.Integers:
        return 2
    if type(G).__name__ == 'FreeGroup':
        if len(G.generators) == 1:
            return 2
        return None
    try:
        order = G.order()
        count = 0
        for g in G.elements:
            if g.order() == order:
                count += 1
        return count
    except Exception:
        return None

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = group_order(G)
    except Exception:
        return [False, False, False]

    # H_1: G is a cyclic group
    try:
        h1 = is_cyclic(G)
    except Exception:
        h1 = False

    # H_2: the order of G is n
    try:
        h2 = (group_order(G) == n)
    except Exception:
        h2 = False

    # ¬Q: The number of generators of G is not phi(n)
    try:
        gen_count = num_generators(G)
        if gen_count is None:
            neg_q = False
        else:
            if n == oo:
                neg_q = True
            else:
                phi_n = totient(n)
                neg_q = (gen_count != phi_n)
    except Exception:
        neg_q = True if gen_count is not None else False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: the order of G is n",
    "¬Q: The number of generators of G is not phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2