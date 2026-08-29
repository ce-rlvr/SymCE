import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)
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
    G = None
    k = None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, k = witness
        else:
            G = witness
            k = None
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.elements)
            order = len(elements)
            h1 = order > 0
    except Exception:
        h1 = False

    # neg_Q: The number of pairs (x, y) in G \times G such that xy = yx is not equal to k|G|
    try:
        if k is None or not h1:
            neg_q = False
        elif not isinstance(k, (int, float, sympy.Basic)):
            neg_q = False
        else:
            commuting_pairs = 0
            for x in elements:
                for y in elements:
                    if x * y == y * x:
                        commuting_pairs += 1
            neg_q = bool(commuting_pairs != k * order)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The number of commuting pairs in G is not equal to k|G|"
]

N_HYP = 1
NEG_Q_INDEX = 1