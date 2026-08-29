import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = bool(witness.degree >= 2)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            degree = witness.degree
            has_derangement = False
            for g in witness.generate():
                is_derangement = True
                for i in range(degree):
                    if g(i) == i:
                        is_derangement = False
                        break
                if is_derangement:
                    has_derangement = True
                    break
            neg_q = not has_derangement
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite permutation group acting on a set \\Omega",
    "H_2: The cardinality of \\Omega is at least 2",
    "¬Q: Every element g \\in G has at least one fixed point (no derangements)"
]

N_HYP = 2
NEG_Q_INDEX = 2