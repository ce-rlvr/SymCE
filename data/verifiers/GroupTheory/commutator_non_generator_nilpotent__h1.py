import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(H.is_subgroup(G))
    except Exception:
        h1_ok = False

    try:
        derived = G.derived_subgroup()
        gens = list(H.generators) + list(derived.generators)
        if not gens:
            h2_ok = bool(G.order() == 1)
        else:
            H_derived = PermutationGroup(gens)
            h2_ok = bool(H_derived.is_subgroup(G) and H_derived.order() == G.order())
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(H.order() != G.order() or not H.is_subgroup(G) or not G.is_subgroup(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: H * G' = G",
    "¬Q: H != G"
]

N_HYP = 2
NEG_Q_INDEX = 2