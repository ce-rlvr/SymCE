import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    # H_1: G is a group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The nilpotency class of G is exactly 2
    try:
        if h1_ok and witness.is_nilpotent:
            lcs = witness.lower_central_series()
            # The nilpotency class is the length of the lower central series minus 1
            h2_ok = (len(lcs) - 1 == 2)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The commutator subgroup G' is NOT a non-trivial subgroup of the center Z(G)
    # Note: For any group of nilpotency class 2, G' <= Z(G) and G' != {e} is a mathematical tautology.
    # Therefore, "non-trivial subgroup of Z(G)" in the conjecture's conclusion means a PROPER non-trivial subgroup.
    # The conclusion fails (neg_Q is True) if G' is not a proper subgroup of Z(G) (e.g., if G' == Z(G)).
    try:
        if h1_ok:
            G_prime = witness.derived_subgroup()
            Z_G = witness.center()
            
            # Check if G' is a subgroup of Z(G)
            is_subgroup = all(g in Z_G for g in G_prime.generators)
            
            # Check if G' is non-trivial (not {e})
            is_not_e = not G_prime.is_trivial
            
            # Check if G' is a proper subgroup of Z(G) (not equal to Z(G))
            is_proper = G_prime.order() < Z_G.order()
            
            # Q is True if G' is a proper, non-trivial subgroup of Z(G)
            Q = is_subgroup and is_not_e and is_proper
            neg_q_ok = not Q
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The nilpotency class of G is exactly 2",
    "¬Q: The commutator subgroup G' is not a non-trivial subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2