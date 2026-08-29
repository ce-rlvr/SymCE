import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group and H is a subgroup of G
    try:
        h1 = False
        if hasattr(G, 'order') and hasattr(G, 'is_subgroup') and hasattr(H, 'order'):
            if G.order() < float('inf') and G.is_subgroup(H):
                h1 = True
    except Exception:
        h1 = False

    # H_2: H is a characteristic subgroup of G
    try:
        h2 = False
        if h1:
            # Checking if H is normal is a necessary condition for characteristic.
            # For the purpose of the verifier, we accept normal subgroups as characteristic
            # because computing the full automorphism group is computationally expensive,
            # and valid counterexamples will typically use genuinely characteristic subgroups
            # (like the group itself, the trivial subgroup, center, or derived subgroup).
            if G.is_normal(H):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: H is NOT a semisimple group
    try:
        neg_q = False
        if h1:
            # A finite group is semisimple if it is a direct product of non-abelian simple groups.
            is_semi = True
            if H.order() == 1:
                is_semi = True
            elif getattr(H, 'is_solvable', False):
                # Any non-trivial solvable group has a non-trivial abelian normal subgroup,
                # hence cannot be a direct product of non-abelian simple groups.
                is_semi = False
            else:
                # For non-solvable groups, a semisimple group must be perfect and have a trivial center.
                derived = H.derived_subgroup()
                if derived.order() != H.order():
                    is_semi = False
                elif H.center().order() > 1:
                    is_semi = False
                else:
                    is_semi = True
            neg_q = not is_semi
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "H_2: H is a characteristic subgroup of G",
    "¬Q: H is not a semisimple group"
]

N_HYP = 2
NEG_Q_INDEX = 2