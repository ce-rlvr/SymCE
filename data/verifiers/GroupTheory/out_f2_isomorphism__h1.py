import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # H_1: The rank of F is exactly 2
    h1_ok = False
    try:
        if hasattr(witness, 'rank'):
            r = witness.rank() if callable(witness.rank) else witness.rank
            if r == 2:
                h1_ok = True
        else:
            if not getattr(witness, 'is_cyclic', False):
                if hasattr(witness, 'generators') and len(witness.generators) <= 2:
                    h1_ok = True
                elif hasattr(witness, 'generate') and hasattr(witness, 'order'):
                    elements = list(witness.generate())
                    order = witness.order() if callable(witness.order) else witness.order
                    pairs_checked = 0
                    for a, b in itertools.combinations(elements, 2):
                        if PermutationGroup(a, b).order() == order:
                            h1_ok = True
                            break
                        pairs_checked += 1
                        if pairs_checked > 1000:
                            break
    except Exception:
        h1_ok = False

    # neg_Q: The outer automorphism group Out(F) is not isomorphic to GL(2, Z)
    # GL(2, Z) is an infinite group. If the witness is a finite group, its outer
    # automorphism group is finite, hence cannot be isomorphic to GL(2, Z).
    neg_q_ok = False
    try:
        if hasattr(witness, 'order'):
            ord_F = witness.order() if callable(witness.order) else witness.order
            if ord_F < float('inf'):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The rank of F is exactly 2",
    "¬Q: The outer automorphism group Out(F) is not isomorphic to GL(2, Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1