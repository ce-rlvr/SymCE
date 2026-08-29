import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def is_group(G):
    return hasattr(G, 'elements') or hasattr(G, 'generators') or hasattr(G, 'generate')

def apply_phi(phi, x):
    if callable(phi):
        return phi(x)
    else:
        return phi[x]

def is_homomorphism(G, H, phi):
    try:
        elements_G = get_elements(G)
        elements_H = get_elements(H)
        for x in elements_G:
            px = apply_phi(phi, x)
            if px not in elements_H:
                return False
            for y in elements_G:
                py = apply_phi(phi, y)
                pxy = apply_phi(phi, x * y)
                if pxy != px * py:
                    return False
        return True
    except Exception:
        return False

def are_conjugate_subsets(G, A, B):
    try:
        elements_G = get_elements(G)
        set_B = set(B)
        for g in elements_G:
            g_inv = g**-1
            conj_A = set(g * a * g_inv for a in A)
            if conj_A == set_B:
                return True
        return False
    except Exception:
        return False

def is_subgroup(H, S):
    try:
        S = set(S)
        if not S:
            return False
        elements_H = get_elements(H)
        # Check if all elements of S are in H
        for x in S:
            if x not in elements_H:
                return False
        # Check closure and inverses
        for x in S:
            if x**-1 not in S:
                return False
            for y in S:
                if x * y not in S:
                    return False
        return True
    except Exception:
        return False

def are_conjugate_subgroups(H, S1, S2):
    try:
        if not (is_subgroup(H, S1) and is_subgroup(H, S2)):
            return False
        elements_H = get_elements(H)
        set_S2 = set(S2)
        for h in elements_H:
            h_inv = h**-1
            conj_S1 = set(h * s * h_inv for s in S1)
            if conj_S1 == set_S2:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            A = witness.get('A')
            B = witness.get('B')
        else:
            G = getattr(witness, 'G')
            H = getattr(witness, 'H')
            phi = getattr(witness, 'phi')
            A = getattr(witness, 'A')
            B = getattr(witness, 'B')
    except Exception:
        return [False, False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False
        
    # H2: phi is a group homomorphism from G to H
    try:
        h2 = is_homomorphism(G, H, phi)
    except Exception:
        h2 = False
        
    # H3: A and B are conjugate in G
    try:
        h3 = are_conjugate_subsets(G, A, B)
    except Exception:
        h3 = False
        
    # Q: The image subgroups phi(A) and phi(B) are conjugate in H
    try:
        phi_A = set(apply_phi(phi, a) for a in A)
        phi_B = set(apply_phi(phi, b) for b in B)
        q = are_conjugate_subgroups(H, phi_A, phi_B)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: A and B are conjugate in G",
    "¬Q: The image subgroups phi(A) and phi(B) are not conjugate in H (e.g., they are not valid subgroups)"
]

N_HYP = 3
NEG_Q_INDEX = 3