import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def num_conjugacy_classes(G):
    # Try using built-in conjugacy_classes if available
    try:
        cc = G.conjugacy_classes
        if callable(cc):
            return len(cc())
        else:
            return len(cc)
    except Exception:
        pass
    
    # Fallback: compute manually
    try:
        elements = list(G.elements)
    except Exception:
        elements = list(G.generate())
        
    seen = set()
    num_classes = 0
    for g in elements:
        if g not in seen:
            num_classes += 1
            for x in elements:
                # x * g * ~x is the conjugate of g by x
                seen.add(x * g * ~x)
    return num_classes

def conditions(witness):
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            # Ensure it's a valid finite group by checking its order
            _ = witness.order()
    except Exception:
        h1 = False

    # ¬Q: The number of conjugacy classes of G is an even integer
    try:
        n_classes = num_conjugacy_classes(witness)
        neg_q = (n_classes % 2 == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The number of conjugacy classes of G is an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1