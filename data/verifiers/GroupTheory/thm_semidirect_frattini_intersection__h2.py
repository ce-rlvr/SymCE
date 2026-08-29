import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def frattini(G: PermutationGroup) -> PermutationGroup:
    """Computes the Frattini subgroup of a finite permutation group."""
    max_subs = G.maximal_subgroups()
    if not max_subs:
        return G
    
    # The Frattini subgroup is the intersection of all maximal subgroups.
    elements = set(list(max_subs[0].generate()))
    for M in max_subs[1:]:
        elements = elements.intersection(list(M.generate()))
        
    return PermutationGroup(list(elements))

def intersection(G1: PermutationGroup, G2: PermutationGroup) -> PermutationGroup:
    """Computes the intersection of two permutation groups."""
    e1 = set(list(G1.generate()))
    e2 = set(list(G2.generate()))
    common = list(e1 & e2)
    return PermutationGroup(common)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group (and H is a subgroup of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: Φ(G) is the Frattini subgroup of G
    try:
        phi_G = frattini(G)
        h2 = True
    except Exception:
        h2 = False

    # H_3: Φ(H) is the Frattini subgroup of H
    try:
        phi_H = frattini(H)
        h3 = True
    except Exception:
        h3 = False

    # ¬Q: The intersection H ∩ Φ(G) is NOT a subgroup of Φ(H)
    try:
        int_H_phi_G = intersection(H, phi_G)
        neg_q = not int_H_phi_G.is_subgroup(phi_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Φ(G) is the Frattini subgroup of G",
    "H_3: Φ(H) is the Frattini subgroup of H",
    "¬Q: H ∩ Φ(G) is not a subgroup of Φ(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3