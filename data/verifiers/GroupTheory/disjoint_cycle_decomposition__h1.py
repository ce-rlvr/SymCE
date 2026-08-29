import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # H_1: Let sigma be a permutation in the symmetric group S_n.
    try:
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    # ¬Q: The conclusion states that the disjoint cycle decomposition is unique 
    # up to the order of the factors.
    # This conclusion FAILS (so ¬Q is True) if the permutation has at least one fixed point.
    # When fixed points (1-cycles) are present, they can be optionally included or omitted 
    # from the product, leading to decompositions with different sets of factors.
    try:
        if h1:
            # witness.size is the size of the domain (n).
            # len(witness.support()) is the number of elements moved by the permutation.
            # If size > support, there is at least one fixed point.
            neg_q = witness.size > len(witness.support())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation",
    "¬Q: the disjoint cycle decomposition of sigma is not unique up to the order of factors"
]

N_HYP = 1
NEG_Q_INDEX = 1