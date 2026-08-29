import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def to_matrix(obj):
    if isinstance(obj, sp.MatrixBase):
        return obj
    if isinstance(obj, (list, tuple)):
        try:
            return sp.Matrix(obj)
        except Exception:
            return None
    return None

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    try:
        A = None
        B = None
        C = None

        if isinstance(witness, tuple):
            if len(witness) == 2:
                B, C = witness
            elif len(witness) == 3:
                A, B, C = witness
            else:
                A = witness
        elif isinstance(witness, dict):
            B = witness.get('B')
            C = witness.get('C')
            A = witness.get('A')
        else:
            A = witness

        A = to_matrix(A) if A is not None else None
        B = to_matrix(B) if B is not None else None
        C = to_matrix(C) if C is not None else None

        if A is None and (B is None or C is None):
            return [False, False, False]

        # If A is provided but B and C are not, try to find a valid partition
        if A is not None and (B is None or C is None):
            if A.rows != A.cols or A.rows % 2 != 0:
                return [False, False, False]
            
            n = A.rows // 2
            h1 = True
            
            partitions = []
            for k in range(1, A.rows):
                for m in range(1, A.cols):
                    if A[:k, :m].is_zero_matrix and A[k:, m:].is_zero_matrix:
                        partitions.append((k, m))
            
            if not partitions:
                return [True, False, False]
            
            h2 = True
            
            best_B, best_C = None, None
            for k, m in partitions:
                t_B = A[:k, m:]
                t_C = A[k:, :m]
                
                is_neg_q = False
                if t_B.shape[1] != t_C.shape[0]:
                    is_neg_q = True
                else:
                    t_BC = t_B * t_C
                    if t_BC.shape != (n, n):
                        is_neg_q = True
                    else:
                        x = sp.Symbol('x')
                        try:
                            p_A = A.charpoly(x).as_expr()
                            I_n = sp.eye(n)
                            mat = x**2 * I_n - t_BC
                            det_expr = mat.det()
                            if sp.expand(p_A - det_expr) != 0:
                                is_neg_q = True
                        except Exception:
                            is_neg_q = True
                
                if is_neg_q:
                    best_B, best_C = t_B, t_C
                    neg_q = True
                    break
            
            if best_B is None:
                k, m = partitions[0]
                best_B = A[:k, m:]
                best_C = A[k:, :m]
                neg_q = False
                
            B, C = best_B, best_C

        else:
            # B and C are provided
            if B is None or C is None:
                return [False, False, False]
                
            k, q = B.shape
            p, m = C.shape
            
            rows = k + p
            cols = m + q
            
            if rows != cols or rows % 2 != 0:
                return [False, False, False]
                
            n = rows // 2
            h1 = True
            
            if A is not None:
                if A.shape != (2*n, 2*n):
                    h2 = False
                else:
                    if A[:k, :m].is_zero_matrix and A[k:, m:].is_zero_matrix and A[:k, m:] == B and A[k:, :m] == C:
                        h2 = True
                    else:
                        h2 = False
            else:
                top = sp.Matrix.hstack(sp.zeros(k, m), B)
                bottom = sp.Matrix.hstack(C, sp.zeros(p, q))
                A = sp.Matrix.vstack(top, bottom)
                h2 = True
                
            if h2:
                if B.shape[1] != C.shape[0]:
                    neg_q = True
                else:
                    try:
                        BC = B * C
                        if BC.shape != (n, n):
                            neg_q = True
                        else:
                            x = sp.Symbol('x')
                            p_A = A.charpoly(x).as_expr()
                            I_n = sp.eye(n)
                            mat = x**2 * I_n - BC
                            det_expr = mat.det()
                            if sp.expand(p_A - det_expr) != 0:
                                neg_q = True
                    except Exception:
                        neg_q = True

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I_n is the n x n identity matrix",
    "H_2: A is the 2n x 2n block matrix with 0, B, C, 0",
    "not_Q: p_A(x) != det(x^2 I_n - BC)"
]

N_HYP = 2
NEG_Q_INDEX = 2