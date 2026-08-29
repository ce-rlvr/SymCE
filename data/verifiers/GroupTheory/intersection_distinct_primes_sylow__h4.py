import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint
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
        G, p, q, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are distinct primes
    try:
        h2 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            is_sub = all(G.contains(g) for g in P.generators)
            if not is_sub:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                k = factorint(order_G).get(p, 0)
                h3 = bool(order_P == p**k)
    except Exception:
        h3 = False

    # ¬Q: The intersection P \cap Q is not the trivial subgroup {1}
    try:
        if hasattr(Q, "contains"):
            def q_contains(g): return Q.contains(g)
        else:
            def q_contains(g): return g in Q
            
        common_elements = []
        for g in P.elements:
            if q_contains(g):
                common_elements.append(g)
                if len(common_elements) > 1:
                    break
                    
        if len(common_elements) == 1 and common_elements[0].is_Identity:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct primes",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {1}"
]

N_HYP = 3
NEG_Q_INDEX = 3