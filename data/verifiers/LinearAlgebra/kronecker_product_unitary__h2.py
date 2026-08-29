import sympy
from sympy import Matrix, eye, zeros, I, Rational
from sympy.matrices import MatrixBase

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_zero_mat(M):
    try:
        if M.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if all((e == 0) or (e.is_zero == True) for e in M):
            return True
    except Exception:
        pass
    try:
        M_exp = M.expand()
        if all((e == 0) or (e.is_zero == True) for e in M_exp):
            return True
    except Exception:
        pass
    try:
        M_simp = M.simplify()
        if all((e == 0) or (e.is_zero == True) for e in M_simp):
            return True
    except Exception:
        pass
    return False

def _kron(A, B):
    rA, cA = A.shape
    rB, cB = B.shape
    return Matrix(rA * rB, cA * cB, lambda i, j: A[i // rB, j // cB] * B[i % rB, j % cB])

def conditions(witness) -> list[bool]:
    # H_1: Let U be an n x n complex matrix that is unitary
    try:
        if len(witness) != 2:
            h1 = False
        else:
            U, V = witness
            if not isinstance(U, MatrixBase):
                U = Matrix(U)
            if U.is_square:
                n = U.shape[0]
                diff = U * U.H - eye(n)
                h1 = _is_zero_mat(diff)
            else:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: The Kronecker product of U and V is NOT an nm x nm unitary matrix
    try:
        if len(witness) != 2:
            neg_q = False
        else:
            U, V = witness
            if not isinstance(U, MatrixBase):
                U = Matrix(U)
            if not isinstance(V, MatrixBase):
                V = Matrix(V)
            
            if U.is_square and V.is_square:
                W = _kron(U, V)
                nm = W.shape[0]
                diff = W * W.H - eye(nm)
                is_unitary = _is_zero_mat(diff)
                neg_q = not is_unitary
            else:
                # If V is not square, the Kronecker product is not an nm x nm matrix
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "¬Q: The Kronecker product of U and V is not an nm x nm unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1