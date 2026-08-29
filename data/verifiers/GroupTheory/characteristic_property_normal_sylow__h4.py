import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(G, PermutationGroup):
            h3 = False
        else:
            is_sub = all(g in G for g in P.generators)
            g_order = G.order()
            p_order = P.order()
            
            expected_p_order = 1
            temp = g_order
            if isinstance(p, (int, sympy.Integer)) and p > 1:
                while temp % p == 0:
                    expected_p_order *= p
                    temp //= p
            
            h3 = is_sub and (p_order == expected_p_order)
    except Exception:
        h3 = False

    # ¬Q: P is not a characteristic subgroup of G
    # For Sylow p-subgroups, being characteristic is equivalent to being normal.
    # If P is not normal, it is definitely not characteristic.
    try:
        if not isinstance(P, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            is_norm = True
            for g in G.generators:
                g_inv = ~g
                for h in P.generators:
                    if (g * h * g_inv) not in P:
                        is_norm = False
                        break
                if not is_norm:
                    break
            neg_q = not is_norm
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3