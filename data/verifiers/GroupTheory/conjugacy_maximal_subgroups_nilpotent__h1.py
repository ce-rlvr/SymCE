import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_maximal(G, M):
    if M.order() >= G.order():
        return False
    for g in M.generators:
        if not G.contains(g):
            return False
    m_gens = list(M.generators)
    for g in G.elements:
        if not M.contains(g):
            H = PermutationGroup(m_gens + [g])
            if H.order() != G.order():
                return False
    return True

def are_conjugate(G, M1, M2):
    if M1.order() != M2.order():
        return False
    m1_gens = list(M1.generators)
    for g in G.elements:
        conjugate_valid = True
        for h in m1_gens:
            conj = g * h * ~g
            if not M2.contains(conj):
                conjugate_valid = False
                break
        if conjugate_valid:
            return True
    return False

def not_equal(M1, M2):
    if M1.order() != M2.order():
        return True
    for h in M1.generators:
        if not M2.contains(h):
            return True
    for h in M2.generators:
        if not M1.contains(h):
            return True
    return False

def conditions(witness):
    """
    Takes a witness tuple (G, M1, M2) and checks the hypotheses and negated conclusion.
    """
    try:
        G, M1, M2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: M1 and M2 are maximal subgroups of G
    try:
        h1_ok = bool(is_maximal(G, M1) and is_maximal(G, M2))
    except Exception:
        h1_ok = False

    # H_2: M1 and M2 are conjugate in G
    try:
        h2_ok = bool(are_conjugate(G, M1, M2))
    except Exception:
        h2_ok = False

    # ¬Q: M1 != M2
    try:
        neg_q_ok = bool(not_equal(M1, M2))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M1 and M2 are maximal subgroups of G",
    "H_2: M1 and M2 are conjugate in G",
    "¬Q: M1 != M2"
]

N_HYP = 2
NEG_Q_INDEX = 2