import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
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
        p, G, X = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.ntheory.isprime(p)
    except Exception:
        h1 = False

    # H_2: G is a finite p-group
    try:
        if not hasattr(G, 'order'):
            h2 = False
        else:
            order = G.order()
            if order == 1:
                h2 = True
            else:
                factors = sympy.ntheory.primefactors(order)
                h2 = (len(factors) == 1 and factors[0] == p)
    except Exception:
        h2 = False

    # H_3: X is a finite set
    try:
        h3 = isinstance(X, (set, list, tuple))
        _ = len(X)
        _ = iter(X)
    except Exception:
        h3 = False

    # neg_Q: |X| \not\equiv |X^G| \pmod p
    try:
        fixed_points = []
        for x in X:
            is_fixed = True
            for g in G.generators:
                if g(x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                fixed_points.append(x)
        
        neg_q = (len(X) % p) != (len(fixed_points) % p)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: X is a finite set",
    "¬Q: |X| is not congruent to |X^G| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3