import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import math

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

def has_normal_sylow_3(G):
    try:
        H = G.sylow_subgroup(3)
        for g in G.generators:
            for h in H.generators:
                if (~g * h * g) not in H:
                    return False
        return True
    except Exception:
        return False

def is_iso_A4(G):
    try:
        if G.order() != 12:
            return False
        if hasattr(G, 'is_isomorphic'):
            return G.is_isomorphic(A4)
        for g in G.elements:
            if g.order() > 3:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = h1 and not has_normal_sylow_3(witness)
    except Exception:
        h2 = False

    try:
        neg_q = h1 and not is_iso_A4(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G does not have a normal Sylow 3-subgroup",
    "¬Q: G is not isomorphic to A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2