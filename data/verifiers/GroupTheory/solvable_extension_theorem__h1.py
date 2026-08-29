import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            h1 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: N is a solvable group
    try:
        h2 = bool(N.is_solvable)
    except Exception:
        h2 = False

    # H_3: G/N is a solvable group
    # G/N is solvable iff the derived series of G eventually lands in N
    try:
        h3 = False
        curr = G
        while True:
            if curr.is_subgroup(N):
                h3 = True
                break
            next_G = curr.derived_subgroup()
            if next_G == curr:
                h3 = False
                break
            curr = next_G
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a solvable group",
    "H_3: G/N is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3