import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S = witness.get('S')
        else:
            G, S = witness
    except Exception:
        return [False, False]

    # H_1: S is a non-trivial solvable subgroup of G
    try:
        is_sub = True
        for g in S.generators:
            if g not in G:
                is_sub = False
                break
        
        try:
            order = S.order()
        except TypeError:
            order = S.order
            
        h1 = is_sub and (order > 1) and S.is_solvable
    except Exception:
        h1 = False

    # ¬Q: The normalizer of S in G is not a proper subgroup of G
    # For finite groups, this is equivalent to S being a normal subgroup of G.
    try:
        is_norm = True
        for g in G.generators:
            for s in S.generators:
                if (g * s * g**-1) not in S:
                    is_norm = False
                    break
            if not is_norm:
                break
        neg_q = is_norm
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a non-trivial solvable subgroup of G",
    "¬Q: The normalizer of S in G is not a proper subgroup of G (i.e., S is normal in G)"
]

N_HYP = 1
NEG_Q_INDEX = 1