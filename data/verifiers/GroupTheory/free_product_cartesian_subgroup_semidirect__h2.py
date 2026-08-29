import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference
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

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple of two groups (A, B).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]
        
    # H_1: A and B are groups
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: A * B is NOT an internal semidirect product of K and a subgroup isomorphic to A x B.
    # A * B is an internal semidirect product of K and A x B if and only if A x B can be embedded into A * B.
    # By the Kurosh Subgroup Theorem (or by analyzing commuting elements in free products), 
    # A x B embeds into A * B if and only if A is trivial or B is trivial.
    # Thus, the conclusion fails (¬Q is True) if and only if both A and B are non-trivial.
    try:
        if h1:
            neg_q = A.order() > 1 and B.order() > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "¬Q: A * B is not an internal semidirect product of K and a subgroup isomorphic to A x B"
]

N_HYP = 1
NEG_Q_INDEX = 1