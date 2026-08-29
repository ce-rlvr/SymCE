import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be a PermutationGroup.
    Omega is the domain the group acts on, which has cardinality equal to witness.degree.
    """
    # H_1: Assume G acts transitively on Omega
    try:
        degree = witness.degree
        h1 = True
        if degree > 0:
            # A group acts transitively if there is exactly one orbit.
            # For an empty domain (degree == 0), it is vacuously transitive.
            if len(witness.orbits()) != 1:
                h1 = False
    except Exception:
        h1 = False

    # H_2: Assume the stabilizer G_alpha is trivial for all alpha in Omega
    try:
        degree = witness.degree
        h2 = True
        for alpha in range(degree):
            if witness.stabilizer(alpha).order() > 1:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The order of the group G is NOT exactly equal to the cardinality of the set Omega
    try:
        degree = witness.degree
        order = witness.order()
        neg_q = bool(order != degree)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G acts transitively on Omega",
    "H_2: The stabilizer G_alpha is trivial for all alpha in Omega",
    "¬Q: The order of the group G is not exactly equal to the cardinality of Omega"
]

N_HYP = 2
NEG_Q_INDEX = 2