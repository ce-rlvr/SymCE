import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.homomorphisms import homomorphism

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    Expected witness format: (F, R, images)
      - F: PermutationGroup
      - R: PermutationGroup
      - images: list of elements in R corresponding to the images of F.generators under the retraction
    """
    try:
        F, R, images = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a subgroup of F
    try:
        h1_ok = all(g in F for g in R.generators)
    except Exception:
        h1_ok = False
        
    # H_2: There exists a retraction homomorphism from F onto R
    try:
        # Create the homomorphism from F to R
        hom = homomorphism(F, R, F.generators, images)
        # A retraction must be the identity on the subgroup R
        h2_ok = all(hom(g) == g for g in R.generators)
    except Exception:
        h2_ok = False
        
    # neg_Q: R is NOT a free factor of F
    try:
        order_F = F.order()
        order_R = R.order()
        # For finite groups, a subgroup R is a free factor of F if and only if R is trivial or R == F.
        # (Since the free product of two non-trivial groups is infinite).
        if order_F != float('inf') and order_F > 0:
            neg_q_ok = (order_R != order_F) and (order_R != 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a subgroup of F",
    "H_2: There exists a retraction homomorphism from F onto R",
    "¬Q: R is not a free factor of F"
]

N_HYP = 2
NEG_Q_INDEX = 2