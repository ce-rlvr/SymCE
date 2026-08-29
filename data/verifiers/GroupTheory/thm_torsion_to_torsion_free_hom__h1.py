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
O2 = zeros(2,2)
O3 = zeros(3,3)

class AdditiveGroup:
    def __init__(self, name="Z", type_check=int):
        self.name = name
        self.identity = 0
        self.type_check = type_check

    def op(self, a, b):
        return a + b

    def inv(self, a):
        return -a

    def is_torsion_free(self):
        return True

    def elements_to_test(self):
        if self.type_check == int:
            return [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 10, -10]
        return [0.0, 1.0, -1.0, 2.5, -2.5, 3.1, -3.1]

    def __contains__(self, item):
        if self.type_check == int:
            return isinstance(item, int)
        return isinstance(item, (int, float))

    def __str__(self):
        return self.name

Z = AdditiveGroup("Z", int)
Q = AdditiveGroup("Q", float)
R = AdditiveGroup("R", float)

def get_elements(G):
    if hasattr(G, 'elements_to_test'):
        return G.elements_to_test()
    if hasattr(G, 'elements'):
        return list(G.elements)
    return []

def get_op(G):
    if hasattr(G, 'op'):
        return G.op
    return lambda a, b: a * b

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    if hasattr(G, 'identity_element'):
        return G.identity_element
    return Permutation()

def conditions(witness) -> list[bool]:
    try:
        G, H, phi_raw = witness
        if isinstance(phi_raw, dict):
            phi = lambda x: phi_raw[x]
        else:
            phi = phi_raw
    except Exception:
        return [False, False, False]

    # H_1: H is a torsion-free group
    try:
        if hasattr(H, 'is_torsion_free'):
            h1 = bool(H.is_torsion_free())
        elif hasattr(H, 'order'):
            h1 = (H.order() == 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        elements = get_elements(G)
        if not elements:
            h2 = False
        else:
            op_G = get_op(G)
            op_H = get_op(H)
            h2 = True
            for a in elements:
                pa = phi(a)
                if hasattr(H, '__contains__'):
                    try:
                        if pa not in H:
                            h2 = False
                            break
                    except Exception:
                        pass
                for b in elements:
                    pb = phi(b)
                    ab = op_G(a, b)
                    p_ab = phi(ab)
                    if p_ab != op_H(pa, pb):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: phi is NOT the trivial homomorphism
    try:
        elements = get_elements(G)
        id_H = get_identity(H)
        is_trivial = True
        if not elements:
            is_trivial = False
        else:
            for a in elements:
                if phi(a) != id_H:
                    is_trivial = False
                    break
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a torsion-free group",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2