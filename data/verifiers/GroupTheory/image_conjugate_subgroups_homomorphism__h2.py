import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G = witness['G']
        H = witness['H']
        A = witness['A']
        B = witness['B']
        phi = witness['phi']
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G
    try:
        h2 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
        if h2:
            G_elems = set(G.generate())
            for g in A.generate():
                if g not in G_elems:
                    h2 = False
                    break
            if h2:
                for g in B.generate():
                    if g not in G_elems:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H3: A and B are conjugate in G
    try:
        h3 = False
        if h1 and h2:
            A_elems = set(A.generate())
            B_elems = set(B.generate())
            for g in G.generate():
                conj = {g * a * ~g for a in A_elems}
                if conj == B_elems:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: The image subgroups phi(A) and phi(B) are not conjugate in H
    try:
        A_elems = set(A.generate())
        B_elems = set(B.generate())
        if callable(phi):
            phi_A = {phi(a) for a in A_elems}
            phi_B = {phi(b) for b in B_elems}
        else:
            phi_A = {phi[a] for a in A_elems}
            phi_B = {phi[b] for b in B_elems}

        H_elems = set(H.generate())
        
        if not phi_A.issubset(H_elems) or not phi_B.issubset(H_elems):
            conclusion = False
        else:
            def is_subgroup(S):
                if not S: return False
                for x in S:
                    if ~x not in S: return False
                    for y in S:
                        if x * y not in S: return False
                return True
            
            is_sg_A = is_subgroup(phi_A)
            is_sg_B = is_subgroup(phi_B)
            
            are_conj = False
            for h in H_elems:
                conj = {h * s * ~h for s in phi_A}
                if conj == phi_B:
                    are_conj = True
                    break
            
            conclusion = is_sg_A and is_sg_B and are_conj
            
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and B are subgroups of G",
    "H_3: A and B are conjugate in G",
    "¬Q: The image subgroups phi(A) and phi(B) are not conjugate in H"
]

N_HYP = 3
NEG_Q_INDEX = 3