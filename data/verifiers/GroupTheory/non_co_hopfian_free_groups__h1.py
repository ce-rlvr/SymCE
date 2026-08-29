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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    h1_ok = False
    try:
        # H_1: The rank of F is at least 2.
        # For finite groups, rank >= 2 is equivalent to the group not being cyclic.
        if hasattr(witness, 'order') and hasattr(witness, 'generate'):
            order = witness.order() if callable(witness.order) else witness.order
            if 1 < order < float('inf'):
                is_cyclic = False
                for g in witness.generate():
                    g_order = g.order() if callable(g.order) else g.order
                    if g_order == order:
                        is_cyclic = True
                        break
                h1_ok = not is_cyclic
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        # ¬Q: Every injective group homomorphism F -> F is surjective (F is co-Hopfian).
        # Any finite group is trivially co-Hopfian by the Pigeonhole Principle.
        if hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            if order < float('inf'):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The rank of F is at least 2",
    "¬Q: Every injective group homomorphism F -> F is surjective (F is co-Hopfian)"
]

N_HYP = 1
NEG_Q_INDEX = 1