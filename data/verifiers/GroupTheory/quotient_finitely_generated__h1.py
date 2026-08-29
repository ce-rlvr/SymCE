import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    if isinstance(witness, dict):
        try:
            if 'is_normal_subgroup' in witness:
                h1 = bool(witness['is_normal_subgroup'])
            if 'quotient_is_finitely_generated' in witness:
                neg_q = not bool(witness['quotient_is_finitely_generated'])
            if 'is_normal_subgroup' in witness or 'quotient_is_finitely_generated' in witness:
                return [h1, neg_q]
        except Exception:
            pass

    try:
        G, N = witness
    except Exception:
        return [False, False]

    try:
        if hasattr(G, 'is_normal'):
            h1 = bool(G.is_normal(N))
        elif hasattr(N, 'is_normal_subgroup'):
            h1 = bool(N.is_normal_subgroup(G))
    except Exception:
        h1 = False

    try:
        if hasattr(G, 'quotient_is_finitely_generated'):
            neg_q = not bool(G.quotient_is_finitely_generated(N))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G/N is not finitely generated"
]

N_HYP = 1
NEG_Q_INDEX = 1