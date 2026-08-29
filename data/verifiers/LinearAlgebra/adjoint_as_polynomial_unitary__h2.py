import sympy
from sympy import Matrix, eye, zeros, simplify, expand
from sympy.matrices.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: U is an n x n complex matrix
    try:
        if isinstance(witness, (list, tuple)):
            U = Matrix(witness)
        else:
            U = witness
            
        if not isinstance(U, MatrixBase):
            h1 = False
        elif U.rows != U.cols:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: There does NOT exist a polynomial p(x) such that U^* = p(U).
    # A square matrix U satisfies U^* = p(U) for some polynomial p 
    # if and only if U is a normal matrix (i.e., U * U^* = U^* * U).
    # Therefore, the conclusion fails iff U is NOT normal.
    try:
        if not h1:
            neg_q = False
        else:
            U_H = U.H
            diff = U * U_H - U_H * U
            is_normal = True
            for i in range(U.rows):
                for j in range(U.cols):
                    val = diff[i, j].expand()
                    if val != 0:
                        val = simplify(val)
                        if val != 0:
                            try:
                                # Check if it's a non-zero float/complex
                                if abs(complex(val)) > 1e-9:
                                    is_normal = False
                                    break
                            except TypeError:
                                # If it contains symbols and didn't simplify to 0, assume non-zero
                                is_normal = False
                                break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: There does not exist a polynomial p(x) such that U^* = p(U) (i.e., U is not normal)"
]

N_HYP = 1
NEG_Q_INDEX = 1