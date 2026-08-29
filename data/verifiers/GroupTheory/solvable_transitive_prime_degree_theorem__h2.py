import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
        h1 = bool(witness.is_solvable)
    except Exception:
        h1 = False

    try:
        p = witness.degree
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        p = witness.degree
        if witness.order() % p != 0:
            c1 = False
        else:
            P = witness.sylow_subgroup(p)
            is_normal = True
            for g in witness.generators:
                for n in P.generators:
                    if not P.contains(g * n * (~g)):
                        is_normal = False
                        break
                if not is_normal:
                    break
            c1 = is_normal
        
        neg_q = not c1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: The cardinality of X is a prime number p",
    "¬Q: G does not contain a unique regular normal subgroup of order p, or G is not isomorphic to a subgroup of AGL(1, p)"
]

N_HYP = 2
NEG_Q_INDEX = 2