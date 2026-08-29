import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        B_raw, x_raw, y_raw = witness
        B = sympy.Matrix(B_raw) if not isinstance(B_raw, sympy.MatrixBase) else B_raw
    except Exception:
        return [False, False]
    
    # H_1: B is a symmetric positive semidefinite bilinear form
    h1 = False
    try:
        if B.is_square and B.is_symmetric():
            n = B.shape[0]
            is_psd = True
            # A symmetric matrix is positive semidefinite iff all principal minors are non-negative
            for k in range(1, n + 1):
                for indices in itertools.combinations(range(n), k):
                    sub_B = B.extract(indices, indices)
                    det_val = sub_B.det()
                    if det_val.is_real is False:
                        is_psd = False
                        break
                    if bool(det_val < 0):
                        is_psd = False
                        break
                if not is_psd:
                    break
            h1 = is_psd
    except Exception:
        h1 = False

    # neg_Q: |B(x,y)|^2 > B(x,x)B(y,y)
    neg_q = False
    try:
        n = B.shape[0]
        
        def to_col_vec(v):
            if isinstance(v, sympy.MatrixBase):
                return v.reshape(n, 1)
            if isinstance(v, (list, tuple)):
                return sympy.Matrix(v).reshape(n, 1)
            return sympy.Matrix([v]).reshape(n, 1)
            
        x_vec = to_col_vec(x_raw)
        y_vec = to_col_vec(y_raw)
        
        Bxy = (x_vec.T * B * y_vec)[0]
        Bxx = (x_vec.T * B * x_vec)[0]
        Byy = (y_vec.T * B * y_vec)[0]
        
        lhs = sympy.Abs(Bxy)**2
        rhs = Bxx * Byy
        
        if bool(lhs > rhs):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a symmetric positive semidefinite bilinear form",
    "¬Q: |B(x,y)|^2 > B(x,x)B(y,y)"
]

N_HYP = 1
NEG_Q_INDEX = 1