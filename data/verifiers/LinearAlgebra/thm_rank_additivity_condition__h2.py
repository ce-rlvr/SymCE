import sympy
from sympy import Matrix, eye, zeros

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two SymPy matrices (A, B) representing
    linear transformations from V to W.
    """
    try:
        A, B = witness
        if not (isinstance(A, Matrix) and isinstance(B, Matrix)):
            return [False, False]
        if A.shape != B.shape:
            return [False, False]
        
        # H1: V and W are finite-dimensional vector spaces over a field F.
        # This is implicitly true since A and B are finite matrices.
        h1_ok = True
        
        # Evaluate P: rank(A+B) == rank(A) + rank(B)
        rank_A = A.rank()
        rank_B = B.rank()
        rank_sum = (A + B).rank()
        P = (rank_sum == rank_A + rank_B)
        
        # Evaluate Q: im(A) \cap im(B) = {0} and ker(A) + ker(B) = V
        # im(A) \cap im(B) = {0} iff rank([A | B]) == rank(A) + rank(B)
        im_cap_zero = (A.row_join(B).rank() == rank_A + rank_B)
        
        # ker(A) + ker(B) = V iff rank([A; B]) == rank(A) + rank(B)
        ker_sum_V = (A.col_join(B).rank() == rank_A + rank_B)
        
        Q = im_cap_zero and ker_sum_V
        
        # The conclusion is P <-> Q. We want it to FAIL, so neg_Q is True if P != Q.
        neg_q_ok = (P != Q)
        
    except Exception:
        h1_ok = False
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional vector spaces over a field F",
    "¬Q: rank(A+B) = rank(A) + rank(B) is NOT equivalent to im(A) ∩ im(B) = {0} and ker(A) + ker(B) = V"
]

N_HYP = 1
NEG_Q_INDEX = 1