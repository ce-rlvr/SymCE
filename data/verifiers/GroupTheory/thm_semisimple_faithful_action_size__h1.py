import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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
    """
    Given a witness object (a PermutationGroup representing a group action on its natural domain),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: X is a finite set with strictly less than 5 elements
    try:
        # The degree of a PermutationGroup is the size of the set it acts on.
        h1_ok = isinstance(witness, PermutationGroup) and witness.degree < 5
    except Exception:
        h1_ok = False

    # H_2: G acts on the set X
    try:
        # A PermutationGroup inherently represents a group acting on a set of size `degree`.
        h2_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h2_ok = False

    # ¬Q: The action of G on X is faithful
    try:
        # A PermutationGroup acting on its natural domain is always faithful,
        # because the kernel of the action is trivial (only the identity permutation fixes all points).
        neg_q_ok = isinstance(witness, PermutationGroup)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a finite set with strictly less than 5 elements",
    "H_2: G acts on the set X",
    "¬Q: The action of G on X is faithful"
]

N_HYP = 2
NEG_Q_INDEX = 2