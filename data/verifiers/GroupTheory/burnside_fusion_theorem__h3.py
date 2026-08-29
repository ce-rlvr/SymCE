import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
        G, p, P, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and (G.order() % p == 0)
    except Exception:
        h2 = False

    # H3: x and y are elements in the center Z(P) of P
    try:
        h3 = False
        if isinstance(P, PermutationGroup) and all(g in G for g in P.generators):
            if x in P and y in P:
                x_in_Z = all(x * e == e * x for e in P.generators)
                y_in_Z = all(y * e == e * y for e in P.generators)
                h3 = bool(x_in_Z and y_in_Z)
    except Exception:
        h3 = False

    # H4: There exists an element g \in G such that g x g^{-1} = y
    try:
        h4 = False
        if h1:
            for g in G.elements:
                if g * x * ~g == y:
                    h4 = True
                    break
    except Exception:
        h4 = False

    # ¬Q: For all n \in N_G(P), n x n^{-1} != y
    try:
        neg_q = True
        if h1 and isinstance(P, PermutationGroup):
            for n in G.elements:
                normalizes = all((n * g * ~n) in P for g in P.generators)
                if normalizes:
                    if n * x * ~n == y:
                        neg_q = False
                        break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: x and y are elements in the center Z(P) of P",
    "H_4: There exists an element g in G such that g x g^{-1} = y",
    "¬Q: For all n in N_G(P), n x n^{-1} != y"
]

N_HYP = 4
NEG_Q_INDEX = 4