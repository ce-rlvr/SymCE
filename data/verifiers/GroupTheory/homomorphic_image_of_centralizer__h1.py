import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    return list(group)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            phi = witness['phi']
            S = list(witness['S'])
        else:
            G, H, phi, S_iter = witness
            S = list(S_iter)
    except Exception:
        return [False, False, False]

    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
    except Exception:
        return [False, False, False]

    if callable(phi):
        phi_func = phi
    else:
        phi_func = lambda x: phi[x]

    # H_1: phi is a group homomorphism from G to H
    try:
        h1_ok = True
        for g in G_elems:
            try:
                val = phi_func(g)
                if val not in H_elems:
                    h1_ok = False
                    break
            except Exception:
                h1_ok = False
                break
        
        if h1_ok:
            for g1 in G_elems:
                for g2 in G_elems:
                    if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: S is a subset of G
    try:
        h2_ok = True
        for s in S:
            if s not in G_elems:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # ¬Q: phi(C_G(S)) is not contained in C_H(phi(S))
    try:
        C_G_S = []
        for g in G_elems:
            if all(g * s == s * g for s in S):
                C_G_S.append(g)
                
        phi_C_G_S = []
        for g in C_G_S:
            val = phi_func(g)
            if val not in phi_C_G_S:
                phi_C_G_S.append(val)
                
        phi_S = []
        for s in S:
            val = phi_func(s)
            if val not in phi_S:
                phi_S.append(val)
                
        C_H_phi_S = []
        for h in H_elems:
            if all(h * y == y * h for y in phi_S):
                C_H_phi_S.append(h)
                
        neg_q_ok = False
        for x in phi_C_G_S:
            if x not in C_H_phi_S:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: S is a subset of G",
    "¬Q: phi(C_G(S)) is not contained in C_H(phi(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2