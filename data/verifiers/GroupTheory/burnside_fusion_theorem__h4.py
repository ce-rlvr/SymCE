import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, p, P, x, y = witness
    except Exception:
        return [False] * 5

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if isinstance(P, PermutationGroup) and all(gen in G for gen in P.generators):
            order_G = G.order()
            order_P = P.order()
            k = 0
            while order_G % (p ** (k + 1)) == 0:
                k += 1
            h3 = (order_P == p ** k)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: x, y in P and there exists g in G such that g x g^-1 = y
    try:
        if x in P and y in P:
            h4 = any(g * x * ~g == y for g in G.elements)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist n in N_G(P) such that n x n^-1 = y
    try:
        N_G_P = []
        for g in G.elements:
            if all((g * gen * ~g) in P for gen in P.generators):
                N_G_P.append(g)
        
        neg_q = not any(n * x * ~n == y for n in N_G_P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: x, y in P and there exists g in G such that g x g^-1 = y",
    "¬Q: There does not exist n in N_G(P) such that n x n^-1 = y"
]

N_HYP = 4
NEG_Q_INDEX = 4