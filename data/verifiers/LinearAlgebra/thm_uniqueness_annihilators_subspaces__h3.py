import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: W_1 and W_2 are subspaces of V",
    "H_3: W_1^0 = W_2^0",
    "¬Q: W_1 != W_2"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                W1, W2 = witness
            elif len(witness) == 3:
                V, W1, W2 = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    def to_matrix(W):
        if isinstance(W, sp.MatrixBase):
            return W
        if isinstance(W, (list, tuple, set)):
            W = list(W)
            if len(W) == 0:
                return sp.Matrix([])
            if isinstance(W[0], sp.MatrixBase):
                if W[0].cols == 1:
                    return sp.Matrix.hstack(*W).T
                elif W[0].rows == 1:
                    return sp.Matrix.vstack(*W)
        return sp.Matrix(W)

    try:
        M1 = to_matrix(W1)
        M2 = to_matrix(W2)
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = isinstance(M1, sp.MatrixBase) and isinstance(M2, sp.MatrixBase)
    except Exception:
        h1 = False
        
    # H_2: W_1 and W_2 are subspaces of V
    try:
        h2 = (M1.cols == M2.cols)
    except Exception:
        h2 = False
        
    # H_3: W_1^0 = W_2^0
    try:
        if not h2:
            h3 = False
        else:
            N1 = M1.nullspace()
            N2 = M2.nullspace()
            if len(N1) != len(N2):
                h3 = False
            else:
                h3 = True
                for v in N1:
                    if not (M2 * v).is_zero_matrix:
                        h3 = False
                        break
                if h3:
                    for v in N2:
                        if not (M1 * v).is_zero_matrix:
                            h3 = False
                            break
    except Exception:
        h3 = False
        
    # ¬Q: W_1 != W_2
    try:
        if not h2:
            neg_q = False
        else:
            rref1 = M1.rref()[0]
            rref2 = M2.rref()[0]
            
            def get_nonzero_rows(mat):
                rows = []
                for i in range(mat.rows):
                    row = mat.row(i)
                    if not row.is_zero_matrix:
                        rows.append(row)
                return rows
                
            rows1 = get_nonzero_rows(rref1)
            rows2 = get_nonzero_rows(rref2)
            
            if len(rows1) != len(rows2):
                q = False
            else:
                q = True
                for r1, r2 in zip(rows1, rows2):
                    if r1 != r2:
                        q = False
                        break
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]