import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi, B = witness
    except Exception:
        return [False, False, False]
        
    try:
        G_elems = set(G.elements) if hasattr(G, 'elements') else set(G)
        H_elems = set(H.elements) if hasattr(H, 'elements') else set(H)
        B_elems = set(B.elements) if hasattr(B, 'elements') else set(B)
    except Exception:
        return [False, False, False]

    # H_1: phi is a group homomorphism from G to H
    try:
        if callable(phi):
            phi_map = {g: phi(g) for g in G_elems}
        else:
            phi_map = phi
            
        if not all(g in phi_map for g in G_elems):
            h1 = False
        elif not all(v in H_elems for v in phi_map.values()):
            h1 = False
        else:
            h1 = True
            for g1 in G_elems:
                for g2 in G_elems:
                    if phi_map[g1 * g2] != phi_map[g1] * phi_map[g2]:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: B is a subgroup of H
    try:
        if not B_elems.issubset(H_elems):
            h2 = False
        elif not B_elems:
            h2 = False
        else:
            h2 = True
            for b1 in B_elems:
                if b1**-1 not in B_elems:
                    h2 = False
                    break
                for b2 in B_elems:
                    if b1 * b2 not in B_elems:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: phi(phi^-1(B)) is not equal to B \cap phi(G)
    try:
        phi_inv_B = {g for g in G_elems if phi_map[g] in B_elems}
        phi_phi_inv_B = {phi_map[g] for g in phi_inv_B}
        phi_G = {phi_map[g] for g in G_elems}
        B_cap_phi_G = B_elems.intersection(phi_G)
        
        neg_q = (phi_phi_inv_B != B_cap_phi_G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: B is a subgroup of H",
    "¬Q: phi(phi^-1(B)) is not equal to B intersection phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2