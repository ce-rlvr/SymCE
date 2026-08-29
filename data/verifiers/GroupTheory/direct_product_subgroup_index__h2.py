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
V4 = DihedralGroup(2)  # Klein four-group
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
    Checks the remaining hypotheses and the negated conclusion.
    The witness should be a tuple: (G_1, G_2, H_1, H_2)
    """
    try:
        G_1, G_2, H_1, H_2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G_1 and G_2 are finite groups
    try:
        h1 = isinstance(G_1, PermutationGroup) and isinstance(G_2, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H_2 is a subgroup of G_2
    try:
        h2 = isinstance(H_2, PermutationGroup) and isinstance(G_2, PermutationGroup) and H_2.is_subgroup(G_2)
    except Exception:
        h2 = False

    # neg_Q: The index of H_1 x H_2 in G_1 x G_2 is equal to the product of indices
    # The conclusion fails (neg_Q is True) if the equality does not hold, 
    # which includes cases where the index is undefined (i.e., when H_1 is not a subgroup of G_1).
    try:
        if not (isinstance(H_1, PermutationGroup) and isinstance(H_2, PermutationGroup) and 
                isinstance(G_1, PermutationGroup) and isinstance(G_2, PermutationGroup)):
            conclusion = False
        else:
            # The index is only well-defined if the subsets are actually subgroups.
            # If they are subgroups, the index equality holds trivially for finite groups.
            if H_1.is_subgroup(G_1) and H_2.is_subgroup(G_2):
                conclusion = True
            else:
                conclusion = False
        neg_q = not conclusion
    except Exception:
        # If any operation fails, the conclusion is considered False.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are finite groups",
    "H_2: H_2 is a subgroup of G_2",
    "¬Q: The index of H_1 x H_2 in G_1 x G_2 is not equal to the product of the individual indices"
]

N_HYP = 2
NEG_Q_INDEX = 2