import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = (
            hasattr(witness, 'order') and 
            hasattr(witness, 'generators') and 
            hasattr(witness, 'sylow_subgroup')
        )
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            order = witness.order()
            factors = factorint(order)
            h2 = (len(factors) == 3 and all(v == 1 for v in factors.values()))
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            order = witness.order()
            factors = factorint(order)
            r = max(factors.keys())
            P = witness.sylow_subgroup(r)
            
            is_normal = True
            for g in witness.generators:
                for h in P.generators:
                    if (g * h * ~g) not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a valid permutation group",
    "H_2: The order of G is pqr where p < q < r are primes",
    "¬Q: The Sylow r-subgroup of G is not normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2