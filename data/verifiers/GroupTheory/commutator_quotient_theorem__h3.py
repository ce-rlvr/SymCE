import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if isinstance(N, PermutationGroup) and N.is_subgroup(G):
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                    if (~g * n * g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            h2 = is_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: NOT (G/N is abelian iff G' <= N)
    try:
        # Check if G/N is abelian
        quotient_abelian = True
        for x in G.generators:
            for y in G.generators:
                if (x * y * ~x * ~y) not in N:
                    quotient_abelian = False
                    break
            if not quotient_abelian:
                break
        
        # Check if G' <= N
        derived_in_N = G.derived_subgroup().is_subgroup(N)
        
        # The conclusion is (quotient_abelian == derived_in_N)
        # We want the negation of the conclusion
        neg_q = not (quotient_abelian == derived_in_N)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: (G/N is abelian) is not equivalent to (G' <= N)"
]

N_HYP = 2
NEG_Q_INDEX = 2