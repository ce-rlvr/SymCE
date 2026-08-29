import sympy
from sympy.matrices import MatrixBase, Matrix, eye, zeros
from sympy import Symbol, expand, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The characteristic polynomial of A ⊗ B is not the product of (x - \lambda_i \mu_j)"
]

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                A, B, mu = witness
            elif len(witness) == 2:
                A, B = witness
                if isinstance(B, MatrixBase) and B.is_square:
                    try:
                        mu = list(B.eigenvals(multiple=True))
                    except Exception:
                        mu = None
                else:
                    mu = []
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: A is a square matrix
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # neg_Q
    try:
        x = Symbol('x')
        if not (isinstance(A, MatrixBase) and isinstance(B, MatrixBase)):
            neg_q = True
        else:
            def kron(X, Y):
                if X.rows == 0 or X.cols == 0 or Y.rows == 0 or Y.cols == 0:
                    return Matrix(X.rows * Y.rows, X.cols * Y.cols, [])
                return Matrix(X.rows * Y.rows, X.cols * Y.cols, 
                              lambda i, j: X[i // Y.rows, j // Y.cols] * Y[i % Y.rows, j % Y.cols])
            
            M = kron(A, B)
            if not M.is_square:
                neg_q = True
            else:
                try:
                    if mu is None:
                        neg_q = False
                    else:
                        cp_M = M.charpoly(x).as_expr()
                        A_eigen = list(A.eigenvals(multiple=True))
                        
                        expected_prod = 1
                        for l in A_eigen:
                            for m_val in mu:
                                expected_prod *= (x - l * m_val)
                                
                        diff = simplify(expand(cp_M - expected_prod))
                        neg_q = not (diff == 0)
                except Exception:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]