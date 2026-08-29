import sympy
from sympy import Matrix, eye, zeros
import sympy.abc

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        M, W_basis = witness
    except Exception:
        return [False, False, False]
    
    # H1: V is a finite-dimensional vector space over a field F
    try:
        if not (isinstance(M, sympy.Matrix) and M.is_square):
            h1 = False
        else:
            if isinstance(W_basis, (list, tuple)):
                if len(W_basis) == 0:
                    W_mat = sympy.Matrix(M.shape[0], 0, [])
                else:
                    cols = []
                    for v in W_basis:
                        if isinstance(v, sympy.Matrix):
                            cols.append(v)
                        else:
                            cols.append(sympy.Matrix(v))
                    W_mat = sympy.Matrix.hstack(*cols)
            else:
                W_mat = W_basis
                
            h1 = isinstance(W_mat, sympy.Matrix) and W_mat.rows == M.rows
    except Exception:
        h1 = False

    # H2: W is a T-invariant subspace of V
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            rank_W = W_mat.rank()
            for j in range(W_mat.cols):
                v = W_mat[:, j]
                Tv = M * v
                if sympy.Matrix.hstack(W_mat, Tv).rank() > rank_W:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The induced quotient operator T/W on V/W is not diagonalizable
    try:
        if not h1:
            neg_q = False
        else:
            n = M.shape[0]
            W_basis_indep = W_mat.columnspace()
            k = len(W_basis_indep)
            
            basis = list(W_basis_indep)
            for i in range(n):
                e = sympy.zeros(n, 1)
                e[i, 0] = 1
                mat = sympy.Matrix.hstack(*(basis + [e]))
                if mat.rank() > len(basis):
                    basis.append(e)
                if len(basis) == n:
                    break
            
            P = sympy.Matrix.hstack(*basis)
            M_sim = P.inv() * M * P
            C = M_sim[k:, k:]
            
            if C.rows == 0:
                q = True
            else:
                q = C.is_diagonalizable()
                
            if q is None:
                neg_q = False
            else:
                neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The induced quotient operator T/W on V/W is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2