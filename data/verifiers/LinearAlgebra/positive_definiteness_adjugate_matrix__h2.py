import sympy as sp

# Top-level setup
# No special named objects needed for this linear algebra conjecture.
# The witness is expected to be a sympy Matrix.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture:
    "Let A be an n \times n real positive definite matrix.
     Then the adjugate matrix adj(A) is positive definite."
    
    Hypothesis:
      1. A is an n x n real positive definite matrix.
         (We check that A is square, real, and its symmetric part has all positive eigenvalues).
    
    Conclusion to negate:
      adj(A) is positive definite.
      (We check if the symmetric part of adj(A) has any non-positive eigenvalues).
    """
    try:
        # Check if witness is a sympy Matrix
        if not isinstance(witness, sp.Matrix):
            return [False, False]
        
        n, m = witness.shape
        if n != m or n == 0:
            return [False, False]
            
        # Check if A is real
        if not all(cell.is_real for cell in witness):
            return [False, False]
            
        # Check if A is positive definite (symmetric part is positive definite)
        # A matrix A is positive definite if x^T A x > 0 for all x != 0.
        # This is equivalent to the symmetric part (A + A^T)/2 being positive definite.
        A = witness
        S_A = (A + A.T) / 2
        
        # To check if S_A is positive definite, we can check its leading principal minors
        # or its eigenvalues. Using leading principal minors is exact and fast in sympy.
        is_A_pd = True
        for i in range(1, n + 1):
            minor_det = S_A[:i, :i].det()
            if minor_det <= 0:
                is_A_pd = False
                break
                
        H1 = is_A_pd
        
    except Exception:
        H1 = False

    try:
        if not H1:
            return [False, False]
            
        # Calculate the adjugate matrix
        # For an invertible matrix, adj(A) = det(A) * A^-1
        # Sympy's adjugate() method computes this directly.
        adj_A = A.adjugate()
        
        # Check if adj(A) is positive definite
        S_adj = (adj_A + adj_A.T) / 2
        
        is_adj_pd = True
        for i in range(1, n + 1):
            minor_det = S_adj[:i, :i].det()
            if minor_det <= 0:
                is_adj_pd = False
                break
                
        # The conclusion is that adj(A) is positive definite.
        # We want the negation of the conclusion to be True.
        neg_Q = not is_adj_pd
        
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: A is an n x n real positive definite matrix",
    "¬Q: The adjugate matrix adj(A) is NOT positive definite"
]

N_HYP = 1
NEG_Q_INDEX = 1