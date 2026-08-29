import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H1: A is an m x n matrix over the real numbers R
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            h1 = all(e.is_real for e in witness)
    except Exception:
        h1 = False

    try:
        # H2: R(A) is the row space of A, considered as a subspace of R^n
        # This is definitional for any valid matrix witness.
        h2 = isinstance(witness, sp.MatrixBase)
    except Exception:
        h2 = False

    try:
        # Conclusion: N(A) is the orthogonal complement of R(A) with respect to the standard Euclidean inner product on R^n
        if not isinstance(witness, sp.MatrixBase):
            neg_q = False
        else:
            n = witness.cols
            null_basis = witness.nullspace()
            row_basis = witness.rowspace()
            
            # For orthogonal complement in R^n, dimensions must sum to n
            dim_sum_correct = (len(null_basis) + len(row_basis) == n)
            
            # Every vector in the null space must be orthogonal to every vector in the row space
            orthogonal = True
            for u in null_basis:
                for v in row_basis:
                    dot_product = sp.simplify(sum(a * b for a, b in zip(u, v)))
                    if dot_product != 0:
                        try:
                            # Allow for minor floating point inaccuracies if evaluated numerically
                            if abs(float(dot_product)) > 1e-12:
                                orthogonal = False
                                break
                        except Exception:
                            # If it cannot be cast to float (e.g., symbolic non-zero), it's not orthogonal
                            orthogonal = False
                            break
                if not orthogonal:
                    break
            
            q = dim_sum_correct and orthogonal
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over the real numbers R",
    "H_2: R(A) is the row space of A, considered as a subspace of R^n",
    "¬Q: N(A) is not the orthogonal complement of R(A) with respect to the standard Euclidean inner product on R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2