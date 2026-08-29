import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_sylow_is_normal(G, p):
    """
    Returns True if the Sylow p-subgroup of G is normal in G.
    By Sylow's theorems, this is equivalent to n_p == 1.
    """
    if G.order() % p != 0:
        return True
    
    P = G.sylow_subgroup(p)
    
    # Check if P is normal in G by conjugating generators of P by generators of G
    for g in G.generators:
        g_inv = g**-1
        for h in P.generators:
            if (g * h * g_inv) not in P:
                return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            # Ensure order can be computed
            _ = witness.order()
    except Exception:
        h1 = False

    # H_2: n_7 is the number of Sylow 7-subgroups of G
    # This is a definitional hypothesis, so it holds trivially if G is a valid group.
    h2 = h1

    # H_3: n_2 is the number of Sylow 2-subgroups of G
    # This is a definitional hypothesis, so it holds trivially if G is a valid group.
    h3 = h1

    # ¬Q: Either n_7 = 1 or n_2 = 1 is FALSE
    # Equivalent to: n_7 != 1 and n_2 != 1
    try:
        if h1 and h2 and h3:
            n7_is_1 = get_sylow_is_normal(witness, 7)
            n2_is_1 = get_sylow_is_normal(witness, 2)
            neg_q = not (n7_is_1 or n2_is_1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: n_7 is the number of Sylow 7-subgroups of G",
    "H_3: n_2 is the number of Sylow 2-subgroups of G",
    "¬Q: n_7 != 1 and n_2 != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3