import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: A and B are n x n square matrices
    try:
        h1 = bool((A.shape[0] == A.shape[1]) and (B.shape[0] == B.shape[1]) and (A.shape == B.shape))
    except Exception:
        h1 = False
        
    def get_adjoint(M):
        if hasattr(M, 'H'):
            return M.H
        elif hasattr(M, 'adjoint'):
            return M.adjoint()
        else:
            return M.T

    # H2: A and B are normal matrices
    try:
        A_adj = get_adjoint(A)
        B_adj = get_adjoint(B)
        A_normal = (A_adj * A == A * A_adj)
        B_normal = (B_adj * B == B * B_adj)
        h2 = bool(A_normal and B_normal)
    except Exception:
        h2 = False
        
    # H3: A and B commute
    try:
        h3 = bool(A * B == B * A)
    except Exception:
        h3 = False
        
    # neg_Q: not check_Q(A, B)
    try:
        def check_Q(A, B):
            A_adj = get_adjoint(A)
            B_adj = get_adjoint(B)
            if A * B != B * A:
                return False
            if A_adj * A != A * A_adj or B_adj * B != B * B_adj:
                return False
                
            def is_real_matrix(M):
                try:
                    for i in range(M.shape[0]):
                        for j in range(M.shape[1]):
                            x = M[i, j]
                            if hasattr(x, 'is_real') and x.is_real is not None:
                                if not x.is_real:
                                    return False
                            elif hasattr(x, 'is_real') and x.is_real is None:
                                return False
                            elif isinstance(x, complex):
                                return False
                    return True
                except Exception:
                    return False

            # If the matrices are real, unitary diagonalization over the same field 
            # implies orthogonal diagonalization, which requires the matrices to be symmetric.
            if is_real_matrix(A) and is_real_matrix(B):
                if A != A.T or B != B.T:
                    return False

            # Check if they are diagonalizable over their field
            try:
                if hasattr(A, 'is_diagonalizable'):
                    if not A.is_diagonalizable():
                        return False
                else:
                    return False
                    
                if hasattr(B, 'is_diagonalizable'):
                    if not B.is_diagonalizable():
                        return False
                else:
                    return False
            except Exception:
                return False

            return True

        neg_q = not check_Q(A, B)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n square matrices",
    "H_2: A and B are normal matrices",
    "H_3: A and B commute (AB = BA)",
    "¬Q: There does not exist a single unitary matrix U such that U^* A U and U^* B U are diagonal matrices"
]

N_HYP = 3
NEG_Q_INDEX = 3