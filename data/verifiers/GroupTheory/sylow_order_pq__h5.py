import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint, isprime
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
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of G is p * q
    try:
        order = witness.order()
        factors = factorint(order)
        h2 = sum(factors.values()) == 2
    except Exception:
        h2 = False

    # H_3: p and q are prime numbers
    try:
        order = witness.order()
        factors = factorint(order)
        h3 = all(isprime(k) for k in factors.keys()) and order > 1
    except Exception:
        h3 = False

    # H_4: p is strictly less than q
    try:
        order = witness.order()
        factors = factorint(order)
        h4 = len(factors) == 2
    except Exception:
        h4 = False

    # ¬Q: G does not have a unique normal Sylow p-subgroup, a unique normal Sylow q-subgroup, or is not cyclic
    try:
        order = witness.order()
        factors = factorint(order)
        if len(factors) != 2 or sum(factors.values()) != 2:
            neg_q = False
        else:
            primes = sorted(list(factors.keys()))
            p = primes[0]
            q = primes[1]
            
            count_p = 0
            count_q = 0
            is_cyclic = False
            
            for g in witness.elements:
                o = g.order()
                if o == p:
                    count_p += 1
                elif o == q:
                    count_q += 1
                elif o == order:
                    is_cyclic = True
                    
            # A Sylow p-subgroup of order p is unique (and thus normal) iff there are exactly p-1 elements of order p
            p_normal = (count_p == p - 1)
            q_normal = (count_q == q - 1)
            
            Q = p_normal and q_normal and is_cyclic
            neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p * q",
    "H_3: p and q are prime numbers",
    "H_4: p is strictly less than q",
    "¬Q: G fails to have unique normal Sylow p- and q-subgroups, or is not cyclic"
]

N_HYP = 4
NEG_Q_INDEX = 4