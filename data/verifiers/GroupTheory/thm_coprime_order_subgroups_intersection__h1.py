import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import sympy.abc

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

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, K = witness
        elif len(witness) == 2:
            H, K = witness
            degree = max(getattr(H, 'degree', 1), getattr(K, 'degree', 1))
            G = SymmetricGroup(degree)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(H.is_subgroup(G) and H.order() != sympy.oo)
    except Exception:
        h1 = False

    try:
        h2 = bool(K.is_subgroup(G) and K.order() != sympy.oo)
    except Exception:
        h2 = False

    try:
        h3 = bool(math.gcd(int(H.order()), int(K.order())) == 1)
    except Exception:
        h3 = False

    try:
        if hasattr(H, 'intersect'):
            int_group = H.intersect(K)
            neg_q = bool(int_group.order() > 1)
        else:
            if H.order() > 5000 or K.order() > 5000:
                neg_q = False
            else:
                h_elems = set(H.generate())
                k_elems = set(K.generate())
                intersection = h_elems.intersection(k_elems)
                neg_q = bool(intersection != {H.identity})
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite subgroup of G",
    "H_2: K is a finite subgroup of G",
    "H_3: The greatest common divisor of |H| and |K| is 1",
    "¬Q: The intersection H \\cap K is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3