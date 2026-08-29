import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic(group):
    """Helper function to check if a PermutationGroup is cyclic."""
    try:
        if not isinstance(group, PermutationGroup):
            return False
        order = group.order()
        if order == 1:
            return True
        for g in group.generate():
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, N = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
        else:
            G = witness
            N = None
    except Exception:
        G, N = None, None

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: N is a cyclic group
    try:
        h3 = is_cyclic(N)
    except Exception:
        h3 = False

    # ¬Q: The commutator subgroup G' is not a cyclic group
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            neg_q = not is_cyclic(G_prime)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a cyclic group",
    "¬Q: The commutator subgroup G' is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3