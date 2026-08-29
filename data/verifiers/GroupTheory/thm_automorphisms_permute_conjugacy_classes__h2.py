import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, C, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: C is a conjugacy class of G
    try:
        C_set = set(C)
        if not C_set:
            h2_ok = False
        else:
            c = list(C_set)[0]
            elements = list(G.generate())
            if c not in elements:
                h2_ok = False
            else:
                conj_class = {g * c * ~g for g in elements}
                h2_ok = (C_set == conj_class)
    except Exception:
        h2_ok = False
        
    # ¬Q: The image phi(C) is not a conjugacy class of G
    try:
        if isinstance(phi, dict):
            phi_C = {phi[x] for x in C_set}
        elif callable(phi):
            phi_C = {phi(x) for x in C_set}
        else:
            phi_C = {phi(x) for x in C_set}
            
        if not phi_C:
            is_conj_class = False
        else:
            d = list(phi_C)[0]
            elements = list(G.generate())
            if d not in elements:
                is_conj_class = False
            else:
                conj_class_d = {g * d * ~g for g in elements}
                is_conj_class = (phi_C == conj_class_d)
        neg_q_ok = not is_conj_class
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: C is a conjugacy class of G",
    "¬Q: The image phi(C) is not a conjugacy class of G"
]

N_HYP = 2
NEG_Q_INDEX = 2