import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools
import z3

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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: P is a normal Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            is_sub = all(G.contains(g) for g in P.generators)
            
            order_G = G.order()
            order_P = P.order()
            
            k = 0
            temp = order_G
            if isinstance(p, (int, sympy.Integer)) and p > 1:
                while temp % p == 0:
                    k += 1
                    temp //= p
                is_sylow = (order_P == p**k)
            else:
                is_sylow = False
                
            is_normal = True
            if is_sub and is_sylow:
                for g in G.generators:
                    for h in P.generators:
                        if not P.contains(g * h * (~g)):
                            is_normal = False
                            break
                        if not P.contains((~g) * h * g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            h3 = bool(is_sub and is_sylow and is_normal)
    except Exception:
        h3 = False

    # Negated Conclusion: G is NOT solvable
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a normal Sylow p-subgroup of G",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3