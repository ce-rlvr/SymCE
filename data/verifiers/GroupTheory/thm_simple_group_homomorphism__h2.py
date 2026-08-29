import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # Setup for subsequent checks
    try:
        if not h1:
            raise ValueError
        elements_G = list(G.generate())
        elements_H = list(H.generate())
        
        id_G = elements_G[0] * (elements_G[0]**-1) if elements_G else None
        id_H = elements_H[0] * (elements_H[0]**-1) if elements_H else None
        
        if callable(phi):
            phi_dict = {g: phi(g) for g in elements_G}
        elif isinstance(phi, dict):
            phi_dict = phi
        else:
            phi_dict = None
    except Exception:
        phi_dict = None
        id_G = None
        id_H = None
        elements_G = []
        elements_H = []

    # H_2: ϕ: G → H is a group homomorphism
    try:
        h2 = False
        if h1 and phi_dict is not None:
            if set(phi_dict.keys()) == set(elements_G):
                if set(phi_dict.values()).issubset(set(elements_H)):
                    h2 = True
                    for x in elements_G:
                        for y in elements_G:
                            if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: ϕ is not the trivial homomorphism
    try:
        h3 = False
        if h2:
            for x in elements_G:
                if phi_dict[x] != id_H:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: ϕ is not injective (which implies G is not isomorphic to ϕ(G))
    try:
        neg_q = False
        if h2:
            for x in elements_G:
                if x != id_G and phi_dict[x] == id_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: ϕ: G → H is a group homomorphism",
    "H_3: ϕ is not the trivial homomorphism",
    "¬Q: ϕ is not injective or G is not isomorphic to ϕ(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3