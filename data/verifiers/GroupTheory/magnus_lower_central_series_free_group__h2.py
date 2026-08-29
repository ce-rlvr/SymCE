import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: F is a free group
    try:
        if isinstance(witness, FreeGroup):
            h1 = True
        elif isinstance(witness, FpGroup) and len(witness.relators) == 0:
            h1 = True
        elif isinstance(witness, PermutationGroup) and witness.order() == 1:
            # The trivial group is the free group of rank 0
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The intersection of the lower central series of F is NOT the trivial subgroup
    try:
        if isinstance(witness, FreeGroup):
            # By Magnus's Theorem (1935), the intersection of the lower central series 
            # of any free group is always the trivial subgroup.
            neg_q = False
        elif isinstance(witness, PermutationGroup):
            # For finite groups, the lower central series stabilizes, 
            # so the infinite intersection is just the last element of the series.
            lcs = witness.lower_central_series()
            neg_q = lcs[-1].order() > 1
        elif hasattr(witness, 'lower_central_series'):
            lcs = witness.lower_central_series()
            neg_q = lcs[-1].order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: The intersection of the lower central series of F is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1