import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        comm = witness.derived_subgroup()
        neg_q = bool(comm.order() > 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "not Q: The commutator subgroup of G is not the trivial subgroup"
]

N_HYP = 0
NEG_Q_INDEX = 0