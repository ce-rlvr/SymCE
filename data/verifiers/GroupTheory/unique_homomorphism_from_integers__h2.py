import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, g = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        if h1_ok:
            try:
                in_G = G.contains(g)
            except Exception:
                in_G = False
        else:
            in_G = False
            
        # The conclusion states there exists a unique homomorphism phi: Z -> G with phi(1) = g.
        # Since Z is the free group on one generator, such a homomorphism exists and is unique
        # if and only if g is an element of G.
        # Thus, the conclusion fails (neg_Q is True) iff g is NOT in G.
        neg_q_ok = not in_G
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: There does not exist a unique group homomorphism phi: Z -> G such that phi(1) = g"
]

N_HYP = 1
NEG_Q_INDEX = 1