import sympy
from sympy import I, Matrix, eye, zeros, re, simplify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness must be a tuple (A, lambda)
        if len(witness) != 2:
            return [False, False]
        A, lam = witness
    except Exception:
        return [False, False]
    
    # H_1: A is an n \times n skew-Hermitian matrix over the complex numbers
    h1 = False
    try:
        if isinstance(A, MatrixBase) and A.is_square and A.rows >= 1:
            diff = A.adjoint() + A
            if diff == zeros(A.rows, A.cols):
                h1 = True
            else:
                diff_simp = simplify(diff)
                if diff_simp == zeros(A.rows, A.cols):
                    h1 = True
    except Exception:
        h1 = False

    # ¬Q: \lambda is NOT a purely imaginary complex number or zero
    # (i.e., the real part of \lambda is non-zero)
    neg_q = False
    try:
        real_part = re(lam)
        try:
            neg_q = abs(float(real_part)) > 1e-12
        except TypeError:
            # Fallback for symbolic expressions that cannot be converted to float
            simp_re = simplify(real_part)
            neg_q = simp_re != 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n skew-Hermitian matrix over the complex numbers",
    "¬Q: lambda is NOT a purely imaginary complex number or zero"
]

N_HYP = 1
NEG_Q_INDEX = 1