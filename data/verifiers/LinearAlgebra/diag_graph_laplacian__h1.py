import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        D, A, L = witness
    except Exception:
        return [False, False, False, False]

    # H1: A is the n x n adjacency matrix of G
    try:
        h1 = True
        if not getattr(A, 'is_square', False):
            h1 = False
        else:
            for i in range(A.rows):
                for j in range(A.cols):
                    val = A[i, j]
                    try:
                        fval = float(val)
                        if not fval.is_integer() or fval < 0:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: D is the n x n degree matrix of G
    try:
        h2 = True
        if not getattr(D, 'is_square', False) or D.rows != A.rows:
            h2 = False
        else:
            for i in range(D.rows):
                for j in range(D.cols):
                    if i != j:
                        try:
                            if float(D[i, j]) != 0.0:
                                h2 = False
                                break
                        except Exception:
                            h2 = False
                            break
                if not h2:
                    break
            
            if h2:
                is_out = True
                is_in = True
                for i in range(D.rows):
                    out_deg = sum(A[i, j] for j in range(A.cols))
                    in_deg = sum(A[j, i] for j in range(A.rows))
                    try:
                        if float(D[i, i]) != float(out_deg):
                            is_out = False
                        if float(D[i, i]) != float(in_deg):
                            is_in = False
                    except Exception:
                        is_out = False
                        is_in = False
                
                if not (is_out or is_in):
                    h2 = False
    except Exception:
        h2 = False

    # H3: L = D - A is the Laplacian matrix of G
    try:
        h3 = bool(L == D - A)
    except Exception:
        h3 = False

    # neg_Q: L is not orthogonally diagonalizable over the real numbers
    try:
        # A real matrix is orthogonally diagonalizable over R iff it is symmetric.
        neg_q = not bool(L.is_symmetric())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is the n x n adjacency matrix of G",
    "H_2: D is the n x n degree matrix of G",
    "H_3: L = D - A is the Laplacian matrix of G",
    "¬Q: The Laplacian matrix L is not orthogonally diagonalizable over the real numbers"
]

N_HYP = 3
NEG_Q_INDEX = 3