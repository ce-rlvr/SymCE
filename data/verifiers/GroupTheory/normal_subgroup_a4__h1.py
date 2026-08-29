import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    # H1: N is a subgroup of A4
    try:
        h1 = False
        if hasattr(witness, 'generators'):
            h1 = True
            for g in witness.generators:
                if not A4.contains(g):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: N is a proper subgroup
    try:
        h2 = False
        if hasattr(witness, 'order'):
            h2 = bool(witness.order() < 12)
    except Exception:
        h2 = False

    # H3: N is a non-trivial subgroup
    try:
        h3 = False
        if hasattr(witness, 'order'):
            h3 = bool(witness.order() > 1)
    except Exception:
        h3 = False

    # H4: N is a normal subgroup of A4
    try:
        h4 = False
        if hasattr(witness, 'generators'):
            is_sub = True
            for g in witness.generators:
                if not A4.contains(g):
                    is_sub = False
                    break
            if is_sub:
                h4 = True
                for g in A4.generators:
                    for h in witness.generators:
                        if not witness.contains(g * h * ~g):
                            h4 = False
                            break
                    if not h4:
                        break
    except Exception:
        h4 = False

    # neg_Q: N does not have order 4 or is not isomorphic to the Klein four-group
    try:
        if not hasattr(witness, 'order'):
            neg_q = False
        else:
            is_V4 = False
            if witness.order() == 4:
                is_V4 = True
                iden = witness.identity
                if hasattr(witness, 'elements'):
                    elems = witness.elements
                else:
                    elems = list(witness.generate())
                for g in elems:
                    if g**2 != iden:
                        is_V4 = False
                        break
            neg_q = not is_V4
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a subgroup of A4",
    "H_2: N is a proper subgroup",
    "H_3: N is a non-trivial subgroup",
    "H_4: N is a normal subgroup of A4",
    "¬Q: N does not have order 4 or is not isomorphic to the Klein four-group"
]

N_HYP = 4
NEG_Q_INDEX = 4