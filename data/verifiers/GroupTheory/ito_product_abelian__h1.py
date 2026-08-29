import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = sympy.combinatorics.PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        if isinstance(witness, dict):
            G = witness.get('G')
            A = witness.get('A')
            B = witness.get('B')
        else:
            G, A, B = witness
    except Exception:
        return [False, False, False]

    # H1: A and B are abelian subgroups of G
    try:
        h1 = False
        if A.is_abelian and B.is_abelian:
            a_sub = all(g in G for g in A.generators)
            b_sub = all(g in G for g in B.generators)
            h1 = bool(a_sub and b_sub)
    except Exception:
        h1 = False

    # H2: G = AB
    try:
        h2 = False
        set_A = set(A.elements)
        set_B = set(B.elements)
        intersection_size = len(set_A.intersection(set_B))
        size_AB = (A.order() * B.order()) // intersection_size
        h2 = bool(size_AB == G.order())
    except Exception:
        h2 = False

    # neg_Q: G is not metabelian or not solvable
    try:
        derived = G.derived_subgroup()
        is_metabelian = bool(derived.is_abelian)
        is_solvable = bool(G.is_solvable)
        nq = not (is_metabelian and is_solvable)
    except Exception:
        nq = False

    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: A and B are abelian subgroups of G",
    "H_2: G = AB",
    "¬Q: G is not metabelian or not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2