import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a nilpotent group and N is a subgroup of G
    try:
        h1 = bool(G.is_nilpotent and N.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H2: The intersection of N and the commutator subgroup is the trivial subgroup
    try:
        C = G.derived_subgroup()
        C_elems = set(C.elements)
        N_elems = set(N.elements)
        intersect_elems = N_elems.intersection(C_elems)
        h2 = (len(intersect_elems) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: N is NOT contained in the center Z(G)
    try:
        Z = G.center()
        Z_elems = set(Z.elements)
        N_elems = set(N.elements)
        N_in_Z = N_elems.issubset(Z_elems)
        neg_q = not N_in_Z
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group and N is a subgroup of G",
    "H_2: The intersection of N and the commutator subgroup is the trivial subgroup",
    "neg_Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2