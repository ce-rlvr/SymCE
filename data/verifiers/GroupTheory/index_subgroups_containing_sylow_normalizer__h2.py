import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            H = witness.get('H')
        else:
            G, p, P, H = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        elif not all(gen in G for gen in P.generators):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            if not isinstance(p, (int, sympy.Integer)) or not sympy.isprime(p):
                h2 = False
            else:
                k = 0
                temp = order_G
                while temp % p == 0:
                    k += 1
                    temp //= p
                h2 = (order_P == p**k)
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            h3 = False
        else:
            h3 = all(gen in G for gen in H.generators)
    except Exception:
        h3 = False

    # H_4: The normalizer N_G(P) is a subgroup of H
    try:
        h4 = True
        for g in G.generate():
            normalizes = True
            for x in P.generators:
                if (g * x * ~g) not in P:
                    normalizes = False
                    break
            if normalizes:
                if g not in H:
                    h4 = False
                    break
    except Exception:
        h4 = False

    # neg_Q: The index of H in G is not congruent to 1 modulo p
    try:
        if G.order() % H.order() != 0:
            neg_q = False
        else:
            index = G.order() // H.order()
            neg_q = (index % p != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: The normalizer N_G(P) is a subgroup of H",
    "neg_Q: The index of H in G is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4