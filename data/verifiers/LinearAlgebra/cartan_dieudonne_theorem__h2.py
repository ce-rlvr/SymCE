import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    """Helper to check if a sympy matrix is identically zero."""
    for i in range(M.rows):
        for j in range(M.cols):
            if sp.simplify(M[i, j]) != 0:
                return False
    return True

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Cartan-Dieudonné Theorem
    counterexample (where the non-degeneracy hypothesis is dropped).
    
    The witness is expected to be a tuple (B, T) where:
      - B is the matrix of the symmetric bilinear form.
      - T is the matrix of the orthogonal transformation.
    """
    try:
        B, T = witness
        if not isinstance(B, sp.MatrixBase):
            B = sp.Matrix(B)
        if not isinstance(T, sp.MatrixBase):
            T = sp.Matrix(T)
    except Exception:
        return [False, False, False]
        
    # H_1: V is an n-dimensional vector space over a field F of characteristic not 2
    # We verify this by checking that B is a symmetric n x n matrix.
    try:
        h1 = B.is_square and B == B.T
    except Exception:
        h1 = False
        
    # H_2: T: V -> V is an orthogonal transformation (isometry) with respect to B
    # This means T^T * B * T == B and T is invertible.
    try:
        if h1 and T.shape == B.shape:
            diff = T.T * B * T - B
            h2 = is_zero_mat(diff) and sp.simplify(T.det()) != 0
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: T cannot be expressed as the composition of at most n reflections.
    # In a degenerate space, an isometry is a product of reflections IF AND ONLY IF
    # it fixes the radical of B pointwise. If it fails to fix Rad(B), it cannot be
    # expressed as a composition of reflections at all.
    try:
        if h1 and h2:
            rad_basis = B.nullspace()
            fixes_rad = True
            for v in rad_basis:
                diff = T * v - v
                if not is_zero_mat(diff):
                    fixes_rad = False
                    break
            neg_q = not fixes_rad
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over a field F of characteristic not 2 (B is symmetric n x n)",
    "H_2: T: V -> V is an orthogonal transformation (isometry) with respect to B",
    "¬Q: T cannot be expressed as the composition of at most n reflections"
]

N_HYP = 2
NEG_Q_INDEX = 2