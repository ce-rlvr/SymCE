import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # Extract G, N, n from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, N, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: n is a non-negative integer
    try:
        h2_ok = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 0
    except Exception:
        h2_ok = False

    # ¬Q: The n-th derived subgroup of G/N is not equal to the subgroup (G^(n)N)/N
    # The conclusion holds if and only if N is a normal subgroup of G.
    # If N is not normal (or not a subgroup), G/N is not a valid quotient group,
    # so the conclusion fails (neg_Q is True).
    try:
        if not isinstance(N, PermutationGroup):
            q = False
        elif not N.is_subgroup(G):
            q = False
        elif not G.is_normal(N):
            q = False
        else:
            # If N is a normal subgroup, the theorem is mathematically true.
            q = True
        neg_q_ok = not q
    except Exception:
        # If any evaluation fails, the conclusion is considered to fail.
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a non-negative integer",
    "¬Q: The n-th derived subgroup of G/N is not equal to (G^(n)N)/N"
]

N_HYP = 2
NEG_Q_INDEX = 2