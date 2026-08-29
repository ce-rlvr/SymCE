import sympy
from sympy import Matrix, eye, zeros, Symbol, expand
from sympy.abc import x, y, z, t

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_element(val):
    if val == 0:
        return True
    if hasattr(val, 'is_zero') and val.is_zero:
        return True
    try:
        if expand(val) == 0:
            return True
    except Exception:
        pass
    return False

def is_zero_matrix(mat):
    for i in range(mat.rows):
        for j in range(mat.cols):
            if not is_zero_element(mat[i, j]):
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, B, X = witness
                has_X = True
            elif len(witness) == 2:
                A, B = witness
                has_X = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H1: A is an n x n matrix and B is an m x m matrix over a field F
    try:
        h1 = (hasattr(A, 'is_Matrix') and A.is_Matrix and A.rows == A.cols and
              hasattr(B, 'is_Matrix') and B.is_Matrix and B.rows == B.cols)
    except Exception:
        h1 = False

    # H2: p_A(x) and p_B(x) are coprime polynomials over F
    try:
        if h1:
            var_x = Symbol('x')
            pA = A.charpoly(var_x)
            pB = B.charpoly(var_x)
            g = pA.gcd(pB)
            h2 = (g.degree() == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The matrix equation AX - XB = 0 has a non-trivial solution X != 0
    try:
        if not h1:
            neg_q = False
        elif has_X:
            if not (hasattr(X, 'is_Matrix') and X.is_Matrix and X.rows == A.rows and X.cols == B.cols):
                neg_q = False
            elif is_zero_matrix(X):
                neg_q = False
            else:
                diff = A*X - X*B
                neg_q = is_zero_matrix(diff)
        else:
            def kron(M1, M2):
                if M1.rows == 0 or M1.cols == 0 or M2.rows == 0 or M2.cols == 0:
                    return zeros(M1.rows * M2.rows, M1.cols * M2.cols)
                return Matrix(M1.rows * M2.rows, M1.cols * M2.cols, 
                              lambda i, j: M1[i // M2.rows, j // M2.cols] * M2[i % M2.rows, j % M2.cols])
            
            n = A.rows
            m = B.rows
            if n == 0 or m == 0:
                neg_q = False
            else:
                I_m = eye(m)
                I_n = eye(n)
                M = kron(I_m, A) - kron(B.T, I_n)
                det_val = M.det()
                neg_q = is_zero_element(det_val)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix and B is an m x m matrix over a field F",
    "H_2: p_A and p_B are coprime polynomials over F",
    "not Q: There exists a non-zero n x m matrix X such that AX - XB = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2