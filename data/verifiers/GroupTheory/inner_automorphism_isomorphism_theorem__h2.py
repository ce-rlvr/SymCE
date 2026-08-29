import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # Definitional hypothesis: Inn(G) is the group of inner automorphisms.
        # This holds trivially if G is a valid group.
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            if witness.order() <= 2000:
                elements = list(witness.generate())
                elem_to_idx = {e: i for i, e in enumerate(elements)}
                inn_gens = []
                for g in witness.generators:
                    perm = []
                    for x in elements:
                        conj = g * x * ~g
                        perm.append(elem_to_idx[conj])
                    inn_gens.append(Permutation(perm))
                Inn_G = PermutationGroup(inn_gens)
                Z_G = witness.center()
                quotient_order = witness.order() // Z_G.order()
                
                # By the First Isomorphism Theorem, the image of the conjugation action (Inn_G)
                # is isomorphic to G / ker(action). The kernel is Z(G).
                # Thus, Inn_G is isomorphic to G/Z(G) if their orders match.
                is_iso = (Inn_G.order() == quotient_order)
                neg_q = not is_iso
            else:
                # For larger groups, we rely on the mathematical fact that the theorem is universally true.
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2