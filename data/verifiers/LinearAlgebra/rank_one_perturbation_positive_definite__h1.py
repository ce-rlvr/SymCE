import sympy
from sympy import Matrix, MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            v = witness.get('v')
        else:
            A, v = witness
            
        if not isinstance(A, MatrixBase):
            A = Matrix(A)
        if not isinstance(v, MatrixBase):
            v = Matrix(v)
            if v.rows == 1 and v.cols > 1:
                v = v.T
    except Exception:
        return [False, False]

    # H_1
    h1 = False
    try:
        if v.cols == 1 and v.rows >= 1 and not v.is_zero:
            if A.rows == A.cols and A.rows == v.rows:
                is_real = True
                for i in range(v.rows):
                    val = v[i, 0]
                    try:
                        if complex(val).imag != 0:
                            is_real = False
                            break
                    except Exception:
                        if val.is_real is False:
                            is_real = False
                            break
                if is_real:
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q
    neg_q = False
    try:
        M = A + v * v.T
        
        is_pos_def = True
        if not M.is_square:
            is_pos_def = False
        elif not M.is_symmetric():
            is_pos_def = False
        else:
            for i in range(1, M.rows + 1):
                d = M[:i, :i].det()
                try:
                    if float(d) <= 0:
                        is_pos_def = False
                        break
                except Exception:
                    if not d.is_positive:
                        is_pos_def = False
                        break
        
        neg_q = not is_pos_def
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: v is a non-zero vector in R^n and A is a compatible n x n matrix",
    "¬Q: The perturbed matrix A + v v^T is not positive definite"
]

N_HYP = 1
NEG_Q_INDEX = 1