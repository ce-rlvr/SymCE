import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        A, B, H, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(B)
    except Exception:
        h2 = False

    try:
        if not (isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)):
            neg_q = True
        else:
            is_sub = H.is_subgroup(A) and K.is_subgroup(B)
            if not is_sub:
                neg_q = True
            else:
                idx_LHS = (A.order() * B.order()) // (H.order() * K.order())
                idx_RHS = (A.order() // H.order()) * (B.order() // K.order())
                neg_q = not (idx_LHS == idx_RHS)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: K is a subgroup of B with finite index",
    "¬Q: H x K is not a subgroup of A x B or its index is not the product of the indices"
]

N_HYP = 2
NEG_Q_INDEX = 2