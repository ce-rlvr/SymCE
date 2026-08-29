import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from sympy import abc
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup
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

def is_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    if H.degree > G.degree:
        return False
    for gen in H.generators:
        if gen not in G:
            return False
    return True

def is_normal(N, G):
    if not is_subgroup(N, G):
        return False
    for g in G.generators:
        for n in N.generators:
            if (g * n * ~g) not in N:
                return False
    return True

def is_homomorphism(phi, G, H):
    if not isinstance(phi, dict):
        return False
    for g in G.elements:
        if g not in phi or phi[g] not in H:
            return False
    for g1 in G.generators:
        for g2 in G.generators:
            if phi[g1 * g2] != phi[g1] * phi[g2]:
                return False
    for g1 in G.elements:
        for g2 in G.elements:
            if phi[g1 * g2] != phi[g1] * phi[g2]:
                return False
    return True

def is_surjective(phi, G, H):
    if not isinstance(phi, dict):
        return False
    image = set(phi.values())
    return len(image) == H.order()

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (G, H, phi, N)
    where G and H are PermutationGroup objects,
    phi is a dictionary mapping elements of G to elements of H,
    and N is a PermutationGroup object representing a subgroup of G.
    """
    try:
        G, H, phi, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: \phi is a surjective group homomorphism from G to H
    try:
        h2_ok = isinstance(H, PermutationGroup) and is_homomorphism(phi, G, H) and is_surjective(phi, G, H)
    except Exception:
        h2_ok = False

    # H_3: N is a normal subgroup of G
    try:
        h3_ok = is_normal(N, G)
    except Exception:
        h3_ok = False

    # ¬Q: The image \phi(N) is NOT a normal subgroup of H
    try:
        if not (isinstance(H, PermutationGroup) and isinstance(phi, dict)):
            neg_q_ok = False
        else:
            image_N_elements = set(phi[n] for n in N.elements if n in phi)
            is_subgrp = True
            identity = H.identity
            if identity not in image_N_elements:
                is_subgrp = False
            else:
                for a in image_N_elements:
                    for b in image_N_elements:
                        if (a * ~b) not in image_N_elements:
                            is_subgrp = False
                            break
                    if not is_subgrp:
                        break
            
            if not is_subgrp:
                neg_q_ok = True
            else:
                is_norm = True
                for h in H.elements:
                    for n_img in image_N_elements:
                        if (h * n_img * ~h) not in image_N_elements:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                neg_q_ok = not is_norm
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: \\phi is a surjective group homomorphism from G to H",
    "H_3: N is a normal subgroup of G",
    "¬Q: The image \\phi(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3