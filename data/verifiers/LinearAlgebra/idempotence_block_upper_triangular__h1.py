import sympy
from sympy import Matrix, zeros, eye, simplify

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is a block upper triangular operator on V_1 \\oplus V_2",
    "H_2: M is a projection operator",
    "¬Q: A and C are not projection operators, or AB + BC != B"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_zero_matrix(mat):
    """Helper function to check if a sympy matrix is exactly zero."""
    for i in range(mat.rows):
        for j in range(mat.cols):
            if mat[i, j] != 0 and simplify(mat[i, j]) != 0:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness. It can be:
        # 1. A tuple (A, B, C) of the blocks.
        # 2. A tuple (M, k) where M is the full matrix and k is the size of block A.
        # 3. A single matrix M, in which case we infer a valid block partition.
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, B, C = witness
                h1 = (hasattr(A, 'is_square') and A.is_square and 
                      hasattr(C, 'is_square') and C.is_square and 
                      hasattr(B, 'rows') and B.rows == A.rows and 
                      hasattr(B, 'cols') and B.cols == C.cols)
                if not h1:
                    return [False, False, False]
                
                top = A.row_join(B)
                bottom = zeros(C.rows, A.cols).row_join(C)
                M = top.col_join(bottom)
            elif len(witness) == 2:
                M, k = witness
                if not (hasattr(M, 'is_square') and M.is_square):
                    return [False, False, False]
                if not (isinstance(k, int) and 0 <= k <= M.rows):
                    return [False, False, False]
                
                A = M[:k, :k]
                B = M[:k, k:]
                C = M[k:, k:]
                lower_left = M[k:, :k]
                
                h1 = is_zero_matrix(lower_left)
                if not h1:
                    return [False, False, False]
            else:
                return [False, False, False]
        elif hasattr(witness, 'is_square') and witness.is_square:
            M = witness
            valid_k = []
            for k in range(M.rows + 1):
                lower_left = M[k:, :k]
                if is_zero_matrix(lower_left):
                    valid_k.append(k)
            
            if not valid_k:
                return [False, False, False]
            
            # Pick the first valid partition
            k = valid_k[0]
            A = M[:k, :k]
            B = M[:k, k:]
            C = M[k:, k:]
            h1 = True
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        # H_2: M is a projection operator (M^2 = M)
        h2 = is_zero_matrix(M**2 - M)
    except Exception:
        h2 = False

    try:
        # Conclusion Q: A and C are projection operators, and AB + BC = B
        is_A_proj = is_zero_matrix(A**2 - A)
        is_C_proj = is_zero_matrix(C**2 - C)
        is_B_eq = is_zero_matrix(A*B + B*C - B)
        
        q = is_A_proj and is_C_proj and is_B_eq
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]