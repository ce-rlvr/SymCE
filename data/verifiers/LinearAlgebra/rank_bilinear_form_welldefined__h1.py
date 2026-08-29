import sympy as sp
from sympy import Matrix

# Top-level setup
# Define standard objects that might be used in the witness
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Verifier for the conjecture:
    Hypotheses:
      - B is a bilinear form on V
      - E1 and E2 are two bases for V
      - M1 and M2 are the Gram matrices of B with respect to E1 and E2, respectively
    Conclusion:
      - The rank of the matrix M1 is equal to the rank of the matrix M2.
      
    The witness is expected to be a tuple: (B, E1, E2)
    where B is a square matrix representing the bilinear form on R^n,
    and E1, E2 are matrices whose columns represent the basis vectors of a subspace V.
    """
    try:
        B, E1, E2 = witness
    except Exception:
        return [False, False, False, False]

    # H1: B is a bilinear form on V
    # B must be a square matrix representing the bilinear form
    try:
        h1 = isinstance(B, Matrix) and B.is_square
    except Exception:
        h1 = False

    # H2: E1 and E2 are two bases for V
    # E1 and E2 must be matrices of full column rank, and they must span the same subspace V
    try:
        if isinstance(E1, Matrix) and isinstance(E2, Matrix) and E1.rows == B.rows and E2.rows == B.rows:
            # Check if they are bases (linearly independent columns)
            is_basis_E1 = E1.rank() == E1.cols
            is_basis_E2 = E2.rank() == E2.cols
            # Check if they span the same subspace V
            span_same_space = E1.row_join(E2).rank() == E1.rank()
            h2 = is_basis_E1 and is_basis_E2 and span_same_space
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: M1 and M2 are the Gram matrices of B with respect to E1 and E2, respectively
    try:
        M1 = E1.T * B * E1
        M2 = E2.T * B * E2
        h3 = True  # By construction from the witness
    except Exception:
        h3 = False

    # ¬Q: The rank of the matrix M1 is NOT equal to the rank of the matrix M2
    try:
        neg_q = M1.rank() != M2.rank()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: B is a bilinear form on V",
    "H_2: E1 and E2 are two bases for V",
    "H_3: M1 and M2 are the Gram matrices of B with respect to E1 and E2",
    "¬Q: The rank of the matrix M1 is not equal to the rank of the matrix M2"
]

N_HYP = 3
NEG_Q_INDEX = 3