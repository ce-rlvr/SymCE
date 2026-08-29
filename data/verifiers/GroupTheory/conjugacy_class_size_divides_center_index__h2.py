import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = x in G
    except Exception:
        h2_ok = False

    try:
        orbit = set()
        queue = [x]
        orbit.add(x)
        gens = G.generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                conj = g * curr * ~g
                if conj not in orbit:
                    orbit.add(conj)
                    queue.append(conj)
        
        conj_class_size = len(orbit)
        center = G.center()
        index_center = G.order() // center.order()
        neg_q_ok = (index_center % conj_class_size) != 0
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of x does not divide the index of Z(G) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2