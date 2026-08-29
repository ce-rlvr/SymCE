import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def is_subgroup(H, G):
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if (g * n * g_inv) not in N:
                    return False
        return True
    except Exception:
        return False

def get_multiplicity(p, n):
    count = 0
    while n % p == 0 and n > 0:
        count += 1
        n //= p
    return count

def conditions(witness):
    try:
        G, N, H, p = witness
    except Exception:
        return [False] * 6 + [False]
    
    # H_1: G, N, H are permutation groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = is_normal(N, G)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False

    # H_4: G is the semidirect product of N and H (|G| = |N| * |H|)
    try:
        h4 = (G.order() == N.order() * H.order())
    except Exception:
        h4 = False

    # H_5: p is a prime number
    try:
        h5 = isprime(p)
    except Exception:
        h5 = False

    # H_6: p divides the order of H
    try:
        h6 = (H.order() % p == 0)
    except Exception:
        h6 = False

    # ¬Q: Sylow p-subgroup of G is not isomorphic to Sylow p-subgroup of H
    # Since H is a subgroup of G, if their Sylow p-subgroups have the same order,
    # the Sylow p-subgroup of H is also a Sylow p-subgroup of G, hence they are isomorphic.
    # If they have different orders, they cannot be isomorphic.
    try:
        g_sylow_order = p ** get_multiplicity(p, G.order())
        h_sylow_order = p ** get_multiplicity(p, H.order())
        neg_q = (g_sylow_order != h_sylow_order)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, H are permutation groups",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G is the semidirect product of N and H (|G| = |N| * |H|)",
    "H_5: p is a prime number",
    "H_6: p divides the order of H",
    "¬Q: Sylow p-subgroup of G is not isomorphic to Sylow p-subgroup of H"
]

N_HYP = 6
NEG_Q_INDEX = 6