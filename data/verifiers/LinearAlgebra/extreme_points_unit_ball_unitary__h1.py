import sympy
from sympy import MatrixBase, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is a matrix
    try:
        if not isinstance(witness, MatrixBase):
            return [False, False, False]
        h1 = True
    except Exception:
        return [False, False, False]

    # H_2: U is in the closed unit ball B (operator 2-norm <= 1)
    try:
        U = witness
        # The operator 2-norm is the maximum singular value.
        # Singular values are the square roots of the eigenvalues of U.H * U.
        eigvals = (U.H * U).eigenvals()
        max_eig_val = 0.0
        for e in eigvals.keys():
            if e.is_number:
                val = float(abs(complex(e.evalf())))
            else:
                e_simp = sympy.simplify(e)
                if e_simp.is_number:
                    val = float(abs(complex(e_simp.evalf())))
                else:
                    raise ValueError("Cannot evaluate eigenvalue")
            if val > max_eig_val:
                max_eig_val = val
        h2 = bool(max_eig_val <= 1 + 1e-9)
    except Exception:
        h2 = False

    # ¬Q: The matrix U is an extreme point of the convex set B if and only if U is a unitary matrix
    try:
        def is_zero(mat):
            for i in range(mat.rows):
                for j in range(mat.cols):
                    if mat[i, j] != 0:
                        if sympy.simplify(mat[i, j]) != 0:
                            return False
            return True

        # In the unit ball of matrices under the operator 2-norm, the extreme points 
        # are exactly the isometries (U.H * U = I) and co-isometries (U * U.H = I).
        diff1 = U.H * U - eye(U.cols)
        diff2 = U * U.H - eye(U.rows)
        
        is_extreme = is_zero(diff1) or is_zero(diff2)
        
        # A matrix is unitary if it is square and U.H * U = I.
        is_unitary = (U.rows == U.cols) and is_zero(diff1)
        
        q = (is_extreme == is_unitary)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is a matrix",
    "H_2: U is in the closed unit ball B (operator 2-norm <= 1)",
    "¬Q: U is an extreme point of B iff U is a unitary matrix (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2