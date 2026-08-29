import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, p, P, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if p <= 1:
            h2 = False
        elif not all(g in G for g in P.generators):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp_G = order_G
            while temp_G % p == 0:
                temp_G //= p
                k += 1
            h2 = (order_P == p**k)
    except Exception:
        h2 = False

    # H_3: H is a p-subgroup of G
    try:
        if p <= 1:
            h3 = False
        elif not all(g in G for g in H.generators):
            h3 = False
        else:
            order_H = H.order()
            if order_H == 1:
                h3 = True
            else:
                temp_H = order_H
                while temp_H % p == 0:
                    temp_H //= p
                h3 = (temp_H == 1)
    except Exception:
        h3 = False

    # neg_Q: H \cap N_G(P) != H \cap P
    try:
        neg_q = False
        for h in H.generate():
            if h not in P:
                in_normalizer = True
                for x in P.generators:
                    if (h * x * ~h) not in P:
                        in_normalizer = False
                        break
                if in_normalizer:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: H is a p-subgroup of G",
    "¬Q: H \\cap N_G(P) \\neq H \\cap P"
]

N_HYP = 3
NEG_Q_INDEX = 3