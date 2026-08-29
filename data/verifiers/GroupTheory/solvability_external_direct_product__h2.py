import sympy
from sympy.combinatorics import DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
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
        if isinstance(witness, dict):
            H = witness['H']
            K = witness['K']
            if 'G' in witness:
                G = witness['G']
            else:
                G = DirectProduct(H, K)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                H, K, G = witness
            elif len(witness) == 2:
                H, K = witness
                G = DirectProduct(H, K)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: H is a finite solvable group
    try:
        h1 = bool(H.is_solvable)
    except Exception:
        h1 = False

    # H_2: G is the external direct product of H and K
    try:
        DP = DirectProduct(H, K)
        if G == DP:
            h2 = True
        else:
            h2 = bool(G.is_isomorphic(DP))
    except Exception:
        h2 = False

    # neg_Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite solvable group",
    "H_2: G is the external direct product of H and K",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2