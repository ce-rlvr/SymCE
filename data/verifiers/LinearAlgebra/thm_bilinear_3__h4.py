import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_B_W(witness):
    """
    Extracts the bilinear form matrix B and the subspace basis matrix W from the witness.
    The witness can be a dictionary {'B': Matrix, 'W': Matrix} or a tuple/list (B, W).
    W is expected to be a matrix whose columns span the subspace.
    """
    if isinstance(witness, dict):
        B, W = witness.get('B'), witness.get('W')
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        B, W = witness[0], witness[1]
    else:
        return None, None
        
    # If W is provided as a list of column vectors, concatenate them into a matrix
    if isinstance(W, list) and len(W) > 0 and isinstance(W[0], sympy.MatrixBase):
        W_mat = W[0]
        for v in W[1:]:
            W_mat = W_mat.row_join(v)
        W = W_mat
    elif isinstance(W, list) and len(W) == 0:
        if isinstance(B, sympy.MatrixBase):
            W = sympy.zeros(B.rows, 0)
            
    return B, W

def conditions(witness) -> list[bool]:
    B, W = extract_B_W(witness)
    
    # H_1: V is a vector space
    # We verify this by checking if B is a square matrix and W has the correct number of rows.
    try:
        h1 = False
        if hasattr(B, 'rows') and hasattr(W, 'rows'):
            if B.rows == B.cols and W.rows == B.rows:
                h1 = True
    except Exception:
        h1 = False

    # H_2: B is a symmetric bilinear form on V
    try:
        h2 = False
        if h1 and B.is_square and B == B.T:
            h2 = True
    except Exception:
        h2 = False

    # H_3: W is a subspace of V
    # Represented by a matrix W whose columns span the subspace.
    try:
        h3 = False
        if h1 and isinstance(W, sympy.MatrixBase):
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The radical of the restricted bilinear form B_W is NOT equal to W \cap W^{\perp}
    try:
        neg_q = False
        if h1 and h2 and h3:
            # 1. Compute Rad(B_W)
            # B_W is represented by W^T * B * W
            if W.cols == 0:
                rad_B_W = zeros(W.rows, 0)
            else:
                B_W = W.T * B * W
                null_B_W = B_W.nullspace()
                if not null_B_W:
                    rad_B_W = zeros(W.rows, 0)
                else:
                    rad_vectors = [W * vec for vec in null_B_W]
                    rad_B_W = rad_vectors[0]
                    for v in rad_vectors[1:]:
                        rad_B_W = rad_B_W.row_join(v)
            
            # 2. Compute W^\perp
            # W^\perp = {v \in V | B(v, w) = 0 for all w \in W}
            # This is the nullspace of W^T * B
            if W.cols == 0:
                W_perp = eye(B.rows)
            else:
                eq_matrix = W.T * B
                null_W_perp = eq_matrix.nullspace()
                if not null_W_perp:
                    W_perp = zeros(W.rows, 0)
                else:
                    W_perp = null_W_perp[0]
                    for v in null_W_perp[1:]:
                        W_perp = W_perp.row_join(v)
            
            # 3. Compute W \cap W^\perp
            if W.cols == 0 or W_perp.cols == 0:
                W_cap_W_perp = zeros(W.rows, 0)
            else:
                # Intersection of column spaces of W and W_perp
                # Solve W * x = W_perp * y  =>  [W, -W_perp] * [x; y] = 0
                M_block = W.row_join(-W_perp)
                null_block = M_block.nullspace()
                if not null_block:
                    W_cap_W_perp = zeros(W.rows, 0)
                else:
                    cap_vectors = []
                    for vec in null_block:
                        x = vec[:W.cols, :]
                        cap_vectors.append(W * x)
                    W_cap_W_perp = cap_vectors[0]
                    for v in cap_vectors[1:]:
                        W_cap_W_perp = W_cap_W_perp.row_join(v)
            
            # 4. Check if rad_B_W and W_cap_W_perp span the same subspace
            def same_column_space(A, B_mat):
                if A.cols == 0 and B_mat.cols == 0:
                    return True
                if A.cols == 0:
                    return B_mat.rank() == 0
                if B_mat.cols == 0:
                    return A.rank() == 0
                rank_A = A.rank()
                if rank_A != B_mat.rank():
                    return False
                return A.row_join(B_mat).rank() == rank_A
            
            conclusion_holds = same_column_space(rad_B_W, W_cap_W_perp)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: B is a symmetric bilinear form on V",
    "H_3: W is a subspace of V",
    "¬Q: The radical of the restricted bilinear form B_W is NOT equal to W \\cap W^{\\perp}"
]

N_HYP = 3
NEG_Q_INDEX = 3