import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2 is definitional given that A and B are groups
    h2 = h1
    
    try:
        # The conclusion states that A * B is a semidirect product of K and A x B.
        # This implies A x B embeds in A * B, which is true if and only if A is trivial or B is trivial.
        # Therefore, the conclusion fails (neg_Q is True) iff both A and B are non-trivial.
        neg_q = h1 and (A.order() > 1) and (B.order() > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: G is the free product of A and B",
    "¬Q: G is not an internal semidirect product of K and a subgroup isomorphic to A x B"
]

N_HYP = 2
NEG_Q_INDEX = 2