import math
from sympy import Matrix, eye, sympify
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = Matrix([[0, 0], [0, 0]])
O3 = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

def conditions(witness):
    try:
        A, B, U, V = witness
    except Exception:
        return [False, False]
    
    # H1: A and B are real m \times n matrices
    try:
        H1_ok = False
        if getattr(A, 'is_Matrix', False) and getattr(B, 'is_Matrix', False):
            if A.shape == B.shape:
                is_real_A = all(sympify(e).is_real for e in A)
                is_real_B = all(sympify(e).is_real for e in B)
                if is_real_A and is_real_B:
                    H1_ok = True
    except Exception:
        H1_ok = False

    # neg_Q: The real n \times n orthogonal matrix \Omega that minimizes ... is \Omega = U V^T
    try:
        neg_Q_ok = False
        if not (getattr(U, 'is_Matrix', False) and getattr(V, 'is_Matrix', False)):
            neg_Q_ok = True
        else:
            n = A.shape[1]
            Omega = U * V.T
            if Omega.shape != (n, n):
                neg_Q_ok = True
            else:
                is_real_Omega = all(sympify(e).is_real for e in Omega)
                if not is_real_Omega:
                    neg_Q_ok = True
                else:
                    I = eye(n)
                    diff_orth = Omega.T * Omega - I
                    is_orthogonal = True
                    for e in diff_orth:
                        val = e.evalf()
                        if not val.is_number or abs(complex(val)) > 1e-9:
                            is_orthogonal = False
                            break
                    if not is_orthogonal:
                        neg_Q_ok = True
                    else:
                        M = A.T * B
                        trace_val = sum((Omega.T * M)[i, i] for i in range(n))
                        
                        MtM = M.T * M
                        eigvals = MtM.eigenvals()
                        max_trace = 0
                        for val, mult in eigvals.items():
                            val_c = complex(val.evalf())
                            val_f = val_c.real
                            if val_f > 0:
                                max_trace += mult * math.sqrt(val_f)
                        
                        trace_val_f = complex(trace_val.evalf()).real
                        if max_trace - trace_val_f > 1e-5:
                            neg_Q_ok = True
                        else:
                            neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [H1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: A and B are real m x n matrices",
    "¬Q: U V^T is not the real n x n orthogonal matrix that minimizes the Frobenius norm"
]

N_HYP = 1
NEG_Q_INDEX = 1