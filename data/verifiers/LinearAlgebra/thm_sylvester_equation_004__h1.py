import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: B is an m x m matrix over F",
    "H_2: A and B have no common eigenvalues in the algebraic closure of F",
    "H_3: C is an n x m matrix over F",
    "¬Q: The matrix equation AX - XB = C does not have a unique n x m matrix solution X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        A, B, C = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: B is an m x m matrix
    try:
        h1 = bool(isinstance(B, sp.MatrixBase) and B.is_square)
    except Exception:
        h1 = False

    # H2: A and B have no common eigenvalues in the algebraic closure of F
    # This is equivalent to their characteristic polynomials being coprime.
    try:
        if isinstance(A, sp.MatrixBase) and A.is_square and isinstance(B, sp.MatrixBase) and B.is_square:
            x = sp.Symbol('x')
            pA = A.charpoly(x).as_expr()
            pB = B.charpoly(x).as_expr()
            gcd_poly = sp.gcd(pA, pB)
            h2 = bool(sp.degree(gcd_poly, x) == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: C is an n x m matrix
    try:
        if isinstance(B, sp.MatrixBase) and B.is_square and isinstance(C, sp.MatrixBase):
            m = B.rows
            h3 = bool(C.cols == m)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: AX - XB = C does NOT have a unique n x m matrix solution X
    try:
        if not (isinstance(A, sp.MatrixBase) and isinstance(B, sp.MatrixBase) and isinstance(C, sp.MatrixBase)):
            neg_q = True
        elif not B.is_square:
            neg_q = True
        else:
            m = B.rows
            n = C.rows
            if C.cols != m:
                neg_q = True
            elif A.cols != n or A.rows != A.cols:
                # If A is not an n x n matrix, the dimensions for AX - XB = C will not match
                # for an n x m matrix X, meaning there are 0 solutions (which is not unique).
                neg_q = True
            else:
                # Set up the linear system for the entries of X
                X_mat = sp.MatrixSymbol('x', n, m).as_explicit()
                eqs = list(A * X_mat - X_mat * B - C)
                vars = list(X_mat)
                M, rhs = sp.linear_eq_to_matrix(eqs, vars)
                
                # A square linear system has a unique solution iff the determinant of its coefficient matrix is non-zero
                if M.rows == M.cols and M.det() != 0:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]