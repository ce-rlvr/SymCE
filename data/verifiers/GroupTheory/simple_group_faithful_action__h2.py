import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
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

def is_normal_subgroup(G, K):
    try:
        if K.order() > G.order():
            return False
        if G.order() % K.order() != 0:
            return False
        for gen in K.generators:
            if gen not in G:
                return False
        for g in G.generators:
            g_inv = ~g
            for k in K.generators:
                conj = g * k * g_inv
                if conj not in K:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, K = None, None
        if hasattr(witness, 'domain') and hasattr(witness, 'kernel'):
            G = witness.domain
            K = witness.kernel()
            valid_action = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[1], 'domain') and hasattr(witness[1], 'kernel'):
                G = witness[0]
                K = witness[1].kernel()
                valid_action = (G == witness[1].domain)
            else:
                G, K = witness
                valid_action = is_normal_subgroup(G, K)
        else:
            valid_action = False
            
        if not valid_action or G is None or K is None:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H1: G is a simple group
    try:
        h1 = False
        if hasattr(G, 'is_simple'):
            is_simp = G.is_simple
            if callable(is_simp):
                h1 = bool(is_simp())
            else:
                h1 = bool(is_simp)
        if G.order() == 1:
            h1 = False
    except Exception:
        h1 = False

    # H2: The action of G on X is not the trivial action
    try:
        h2 = bool(K.order() < G.order())
    except Exception:
        h2 = False

    # neg_Q: The action of G on X is NOT faithful (kernel is not trivial)
    try:
        neg_q = bool(K.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "H_2: The action of G on X is not the trivial action",
    "¬Q: The action of G on X is not faithful (kernel is not trivial)"
]

N_HYP = 2
NEG_Q_INDEX = 2