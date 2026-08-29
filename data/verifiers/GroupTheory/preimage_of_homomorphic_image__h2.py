import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

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

def conditions(witness):
    try:
        G, H, A, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups, phi is a map from G to H
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            G_elems = set(G.elements)
            H_elems = set(H.elements)
            if callable(phi):
                try:
                    phi_dict = {g: phi(g) for g in G_elems}
                except Exception:
                    phi_dict = None
            elif isinstance(phi, dict):
                phi_dict = phi
            else:
                phi_dict = None
            
            if phi_dict is not None:
                if set(phi_dict.keys()) == G_elems:
                    if all(v in H_elems for v in phi_dict.values()):
                        h1 = True
    except Exception:
        h1 = False

    # H_2: A is a subgroup of G
    try:
        h2 = isinstance(A, PermutationGroup) and A.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: preimage of phi(A) != A * ker(phi)
    try:
        if callable(phi):
            phi_dict = {g: phi(g) for g in G.elements}
        else:
            phi_dict = phi
            
        H_elems = list(H.elements)
        # Find the identity element of H
        e_H = next(g for g in H_elems if g * g == g)
        
        ker_phi = {g for g in G.elements if phi_dict[g] == e_H}
        A_ker = {a * k for a in A.elements for k in ker_phi}
        phi_A = {phi_dict[a] for a in A.elements}
        preimage = {g for g in G.elements if phi_dict[g] in phi_A}
        
        neg_q = (preimage != A_ker)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and phi maps G to H",
    "H_2: A is a subgroup of G",
    "¬Q: The preimage phi^{-1}(phi(A)) is not equal to the product A ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2