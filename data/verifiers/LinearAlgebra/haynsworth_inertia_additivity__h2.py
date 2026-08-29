import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B, C = witness
        h1 = False
        if hasattr(A, 'is_square') and A.is_square and hasattr(C, 'is_square') and C.is_square:
            if B.rows == A.rows and B.cols == C.cols:
                if A == A.H and C == C.H:
                    h1 = True
    except Exception:
        h1 = False

    try:
        A, B, C = witness
        M = A.row_join(B).col_join(B.H.row_join(C))
        
        def inertia(mat):
            evs = mat.eigenvals()
            p = q = z = 0
            for val, mult in evs.items():
                if val.is_zero:
                    z += mult
                    continue
                if val.is_positive:
                    p += mult
                    continue
                if val.is_negative:
                    q += mult
                    continue
                
                val_c = complex(val)
                if abs(val_c) < 1e-9:
                    z += mult
                elif val_c.real > 0:
                    p += mult
                else:
                    q += mult
            return (p, q, z)
            
        in_M = inertia(M)
        in_A = inertia(A)
        
        try:
            A_inv = A.inv()
        except Exception:
            # If A is not invertible, the Schur complement is undefined,
            # so the equality in the conclusion cannot hold.
            neg_q = True
        else:
            Schur = C - B.H * A_inv * B
            in_Schur = inertia(Schur)
            sum_in = (in_A[0] + in_Schur[0], in_A[1] + in_Schur[1], in_A[2] + in_Schur[2])
            neg_q = (in_M != sum_in)
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a partitioned Hermitian matrix",
    "¬Q: Inertia of M is not equal to inertia of A plus inertia of Schur complement"
]

N_HYP = 1
NEG_Q_INDEX = 1