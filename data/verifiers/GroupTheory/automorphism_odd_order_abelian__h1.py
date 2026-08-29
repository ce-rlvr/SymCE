import sympy
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
        h1 = True
        if hasattr(witness, 'order'):
            h1 = witness.order() < float('inf')
    except Exception:
        h1 = False

    try:
        h2 = witness.order() % 2 != 0
    except Exception:
        h2 = False

    try:
        elements = list(witness.generate())
        is_bijection = len(set(x**2 for x in elements)) == len(elements)
        is_homomorphism = all((x*y)**2 == (x**2)*(y**2) for x in elements for y in elements)
        neg_q = not (is_bijection and is_homomorphism)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is finite",
    "H_2: The order of G is an odd integer",
    "¬Q: The map f(x) = 2x (or x^2) is not a group automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2