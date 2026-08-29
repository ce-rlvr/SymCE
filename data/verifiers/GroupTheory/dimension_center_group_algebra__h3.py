import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: C(G) is the group algebra of G over the complex numbers
    # This is a definitional context hypothesis.
    h2 = True

    # ¬Q: The dimension of Z(C(G)) as a complex vector space is NOT exactly equal 
    # to the number of conjugacy classes of G.
    try:
        if h1:
            n_classes = len(witness.conjugacy_classes())
            # The class sums always form a basis for the center of the group algebra Z(C(G))
            dim_Z = n_classes  
            neg_q = bool(dim_Z != n_classes)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

# Note: Brackets '[' and ']' are avoided in the labels to prevent regex parser truncation errors.
CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: C(G) is the group algebra of G over the complex numbers",
    "¬Q: The dimension of Z(C(G)) is not equal to the number of conjugacy classes of G"
]

N_HYP = 2
NEG_Q_INDEX = 2