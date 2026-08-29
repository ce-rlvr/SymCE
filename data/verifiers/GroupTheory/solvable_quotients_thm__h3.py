import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, N = witness
    except Exception:
        return [False, False, False]
    
    def is_subgroup(sub, grp):
        try:
            return all(grp.contains(g) for g in sub.generators)
        except Exception:
            return False

    def is_normal(sub, grp):
        try:
            if not is_subgroup(sub, grp):
                return False
            for n in sub.generators:
                for g in grp.generators:
                    if not sub.contains(g * n * ~g):
                        return False
            return True
        except Exception:
            return False

    # H_1: G is a group and N is a subgroup of G
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and is_subgroup(N, G)
    except Exception:
        h1_ok = False

    # H_2: G is a solvable group
    try:
        h2_ok = bool(G.is_solvable)
    except Exception:
        h2_ok = False

    # ¬Q: The quotient group G/N is not solvable (or not a valid group because N is not normal)
    try:
        if not is_normal(N, G):
            neg_q_ok = True
        else:
            Q_grp = G.quotient_group(N)
            neg_q_ok = not bool(Q_grp.is_solvable)
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: G is a solvable group",
    "¬Q: The quotient group G/N is not solvable (or undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2