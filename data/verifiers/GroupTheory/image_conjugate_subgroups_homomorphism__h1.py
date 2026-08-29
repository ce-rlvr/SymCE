import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            A = witness.get('A')
            B = witness.get('B')
        else:
            G = witness.G
            H = witness.H
            phi = witness.phi
            A = witness.A
            B = witness.B
    except Exception:
        return [False, False, False, False]

    # H_1: phi is a group homomorphism from G to H
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        if callable(phi):
            phi_map = {g: phi(g) for g in G_elements}
        elif isinstance(phi, dict):
            phi_map = phi
        else:
            phi_map = dict(phi)
            
        h1 = True
        if set(phi_map.keys()) != set(G_elements):
            h1 = False
        if h1:
            for v in phi_map.values():
                if v not in H_elements:
                    h1 = False
                    break
        if h1:
            for x in G_elements:
                for y in G_elements:
                    if phi_map[x * y] != phi_map[x] * phi_map[y]:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: A and B are subgroups of G
    try:
        if hasattr(A, 'is_subgroup'):
            h2_A = A.is_subgroup(G)
            A_elems = set(A.elements)
        else:
            A_elems = set(A)
            if not A_elems:
                h2_A = False
            else:
                h2_A = A_elems.issubset(set(G.elements))
                if h2_A:
                    for x in A_elems:
                        if ~x not in A_elems:
                            h2_A = False
                            break
                        for y in A_elems:
                            if x * y not in A_elems:
                                h2_A = False
                                break
    except Exception:
        h2_A = False

    try:
        if hasattr(B, 'is_subgroup'):
            h2_B = B.is_subgroup(G)
            B_elems = set(B.elements)
        else:
            B_elems = set(B)
            if not B_elems:
                h2_B = False
            else:
                h2_B = B_elems.issubset(set(G.elements))
                if h2_B:
                    for x in B_elems:
                        if ~x not in B_elems:
                            h2_B = False
                            break
                        for y in B_elems:
                            if x * y not in B_elems:
                                h2_B = False
                                break
    except Exception:
        h2_B = False

    h2 = h2_A and h2_B

    # H_3: A and B are conjugate in G
    try:
        h3 = False
        if h2:
            for g in G.elements:
                g_inv = ~g
                conj_A = {g * a * g_inv for a in A_elems}
                if conj_A == B_elems:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: phi(A) and phi(B) are not conjugate in H
    try:
        phi_A = {phi_map[a] for a in A_elems}
        phi_B = {phi_map[b] for b in B_elems}
        
        neg_q = True
        for h in H.elements:
            h_inv = ~h
            conj_phi_A = {h * x * h_inv for x in phi_A}
            if conj_phi_A == phi_B:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: A and B are subgroups of G",
    "H_3: A and B are conjugate in G",
    "¬Q: phi(A) and phi(B) are not conjugate in H"
]

N_HYP = 3
NEG_Q_INDEX = 3