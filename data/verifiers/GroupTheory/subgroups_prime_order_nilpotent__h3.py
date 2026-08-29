import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N) where G and N are PermutationGroup objects.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a nilpotent group
    try:
        nilp = G.is_nilpotent
        if callable(nilp):
            h1 = bool(nilp())
        else:
            h1 = bool(nilp)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        is_sub = True
        for n in N.generators:
            if not G.contains(n):
                is_sub = False
                break
        
        is_normal = True
        if is_sub:
            for g in G.generators:
                for n in N.generators:
                    # Check if the conjugate g * n * g^-1 is in N
                    if not N.contains(g * n * ~g):
                        is_normal = False
                        break
                if not is_normal:
                    break
        h2 = is_sub and is_normal
    except Exception:
        h2 = False

    # ¬Q: N is NOT contained in the center of G
    try:
        in_cent = True
        for n in N.generators:
            for g in G.generators:
                # If any generator of N does not commute with any generator of G,
                # then N is not fully contained in the center of G.
                if n * g != g * n:
                    in_cent = False
                    break
            if not in_cent:
                break
        neg_q = not in_cent
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 2
NEG_Q_INDEX = 2