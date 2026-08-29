import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
    """
    Given a witness (G, N), checks if it is a valid counterexample to the false conjecture:
    "If G is a nilpotent group, then N is contained in the center of G."
    """
    try:
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # ¬Q: N is NOT contained in the center of G
    try:
        center = G.center()
        if hasattr(N, 'generators'):
            gens = N.generators
        else:
            gens = N
            
        is_contained = True
        for g in gens:
            if g not in center:
                is_contained = False
                break
        neg_q = not is_contained
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 1
NEG_Q_INDEX = 1