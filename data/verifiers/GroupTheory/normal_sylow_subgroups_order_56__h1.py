import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() == 56
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(witness, PermutationGroup)
    except Exception:
        h3 = False

    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.generate())
            
            P7 = witness.sylow_subgroup(7)
            P7_elems = list(P7.generate())
            conj7 = set()
            for g in elements:
                conj7.add(frozenset([g * x * ~g for x in P7_elems]))
            n_7 = len(conj7)

            P2 = witness.sylow_subgroup(2)
            P2_elems = list(P2.generate())
            conj2 = set()
            for g in elements:
                conj2.add(frozenset([g * x * ~g for x in P2_elems]))
            n_2 = len(conj2)

            neg_q = bool((n_7 != 1) and (n_2 != 1))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is 56",
    "H_2: n_7 is the number of Sylow 7-subgroups of G",
    "H_3: n_2 is the number of Sylow 2-subgroups of G",
    "¬Q: n_7 != 1 and n_2 != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3