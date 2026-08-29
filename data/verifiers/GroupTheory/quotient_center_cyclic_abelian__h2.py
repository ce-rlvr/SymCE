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

def conditions(witness):
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is cyclic
    try:
        if not h1:
            h2 = False
        else:
            Z = witness.center()
            Z_gens = list(Z.generators)
            # If the group is too large, use the mathematical fact that G/Z(G) cyclic <=> G abelian
            if witness.order() > 2000:
                h2 = bool(witness.is_abelian)
            else:
                h2 = False
                # G/Z(G) is cyclic iff there exists g in G such that <Z(G), g> = G
                for g in witness.generate():
                    sub = PermutationGroup(Z_gens + [g])
                    if sub.order() == witness.order():
                        h2 = True
                        break
    except Exception:
        h2 = False

    # ¬Q: G is not an abelian group
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not bool(witness.is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is cyclic",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2