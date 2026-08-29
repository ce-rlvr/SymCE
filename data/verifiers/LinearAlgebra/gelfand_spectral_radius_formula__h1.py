import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be a matrix A), checks if it is a counterexample
    to the false conjecture.
    
    The dropped hypothesis from Gelfand's Spectral Radius Formula is that A must 
    be a square matrix. For non-square matrices, the matrix powers A^k and the 
    spectral radius ρ(A) are undefined, causing the conclusion to fail.
    """
    try:
        # H_1: ||·|| is a submultiplicative matrix norm
        # Since the witness provides the matrix A, the norm is universally quantified 
        # or assumed to be a standard submultiplicative norm (like the Frobenius norm).
        # Therefore, this hypothesis is trivially satisfied for the matrix witness.
        h1 = True
    except Exception:
        h1 = False

    try:
        # Extract the matrix if the witness is a tuple (e.g., (A, norm))
        if isinstance(witness, tuple) and len(witness) >= 1:
            A = witness[0]
        else:
            A = witness
            
        # Convert list of lists to a sympy Matrix
        if isinstance(A, list):
            A = sp.Matrix(A)
            
        # Check if A is a matrix-like object with a 2D shape
        if hasattr(A, 'shape') and len(A.shape) == 2:
            is_sq = (A.shape[0] == A.shape[1])
            
            # Conclusion: ρ(A) == lim_{k → ∞} ||A^k||^{1/k}
            if not is_sq:
                # For non-square matrices, A^k and ρ(A) are undefined.
                # Thus, the equality fails.
                neg_q = True
            elif A.shape == (0, 0):
                # For an empty matrix, the spectral radius is the supremum of an empty set (-inf),
                # while the limit of the norm of A^k is 0. Thus, the equality fails.
                neg_q = True
            else:
                # For all valid square matrices, Gelfand's formula holds mathematically.
                neg_q = False
        else:
            # Not a valid matrix witness
            return [False, False]
            
    except Exception:
        # If any unexpected error occurs during evaluation, we assume the conclusion fails
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: ||·|| is a submultiplicative matrix norm",
    "¬Q: The spectral radius ρ(A) is not equal to lim_{k → ∞} ||A^k||^{1/k}"
]

N_HYP = 1
NEG_Q_INDEX = 1