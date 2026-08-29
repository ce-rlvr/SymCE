import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, isprime
from sympy.abc import x, y, z
import z3
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        n = witness.order()
        f = factorint(n)
        h2 = sum(f.values()) == 2
    except Exception:
        h2 = False

    try:
        # If the order is a product of two primes (sum of multiplicities is 2),
        # then p and q are prime numbers.
        h3 = h2
    except Exception:
        h3 = False

    try:
        n = witness.order()
        f = factorint(n)
        if sum(f.values()) == 2:
            primes = list(f.keys())
            if len(primes) == 1:
                p = q = primes[0]
                h4 = (q - 1) % p != 0
            else:
                p1, p2 = primes
                # Check if there is ANY assignment of p, q to the two prime factors
                # such that p does not divide q - 1.
                h4 = ((p2 - 1) % p1 != 0) or ((p1 - 1) % p2 != 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        # The conclusion requires G to be isomorphic to the cyclic group of order pq
        # (which implies it has unique normal Sylow p and q subgroups).
        # The conclusion fails if G is not cyclic.
        neg_q = not witness.is_cyclic
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is p * q",
    "H_3: p and q are prime numbers",
    "H_4: p does not divide q - 1",
    "¬Q: G is not isomorphic to the cyclic group of order pq"
]

N_HYP = 4
NEG_Q_INDEX = 4