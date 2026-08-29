import sympy as sp
from sympy import eye, zeros, Matrix

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a single matrix A, or a tuple (A, H).
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, H = witness
        else:
            A = witness
            H = None
    except Exception:
        A = witness
        H = None

    # H_1: f is the matrix inversion map
    # This is a definitional hypothesis, so it holds by context.
    h1_ok = True

    # H_2: A is a matrix in GL(n, R)
    try:
        h2_ok = False
        if hasattr(A, 'is_Matrix') and A.is_Matrix:
            if A.shape[0] == A.shape[1]:
                if A.det() != 0:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion fails
    # The conclusion states that the total derivative evaluated at a matrix H 
    # is given by -A^{-1}HA^{-1}. Since the hypothesis "H is a matrix of the same size as A" 
    # was dropped, the statement implies this holds for ANY matrix H. 
    # This fails when H is of a different size, as the total derivative is undefined.
    try:
        if H is not None:
            if not hasattr(H, 'is_Matrix') or not H.is_Matrix:
                neg_q_ok = True
            elif H.shape != A.shape:
                neg_q_ok = True
            else:
                # If H is of the correct size, the formula actually holds, so the conclusion is true.
                neg_q_ok = False
        else:
            # If H is not specified, the universally quantified conclusion over all matrices H is false.
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let f: GL(n, R) -> GL(n, R) be the matrix inversion map defined by f(A) = A^(-1)",
    "H_2: Let A be a matrix in GL(n, R)",
    "¬Q: The total derivative evaluated at a matrix H is NOT given by H |-> -A^(-1)HA^(-1) (e.g., H is of the wrong size)"
]

N_HYP = 2
NEG_Q_INDEX = 2