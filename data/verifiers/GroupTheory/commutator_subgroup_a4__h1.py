import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Define V4 as the Klein four-group in A4
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)

def conditions(witness):
    try:
        # H_1: Let V_4 be the Klein four-group consisting of the identity and the double transpositions in A_4
        # This is a definitional hypothesis. We require the witness to be a valid PermutationGroup.
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # Conclusion: The commutator subgroup of the witness is exactly V_4
        # (The original theorem was about A_4, but since the hypothesis "G = A_4" was dropped, 
        # we evaluate the conclusion on the witness group).
        D = witness.derived_subgroup()
        
        is_V4 = False
        if D.order() == 4:
            try:
                # Safely compare the elements of the derived subgroup with V4
                if set(D.elements) == set(V4.elements):
                    is_V4 = True
            except Exception:
                pass
                    
        neg_q = not is_V4
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V_4 is defined as the Klein four-group in A_4",
    "¬Q: The commutator subgroup of the witness is not exactly V_4"
]

N_HYP = 1
NEG_Q_INDEX = 1