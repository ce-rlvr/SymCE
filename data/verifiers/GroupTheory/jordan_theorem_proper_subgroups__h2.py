import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and all(h in G for h in H.generators)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            g_elements = list(G.generate())
            h_elements = list(H.generate())
            union_elements = set()
            for g in g_elements:
                g_inv = ~g
                for h in h_elements:
                    union_elements.add(g * h * g_inv)
            
            neg_q = len(union_elements) == len(g_elements)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "¬Q: The union of conjugates of H is not strictly contained in G"
]

N_HYP = 1
NEG_Q_INDEX = 1