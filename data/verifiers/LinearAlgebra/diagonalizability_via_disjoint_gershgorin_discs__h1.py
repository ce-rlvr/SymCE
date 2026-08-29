import sympy as sp
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if not isinstance(witness, sp.MatrixBase):
            A = sp.Matrix(witness)
        else:
            A = witness
    except Exception:
        return [False, False]
    
    # H_1: The n Gershgorin discs of A are mutually disjoint
    h1_ok = False
    try:
        n = A.rows
        m = A.cols
        # To have n Gershgorin discs, the matrix must have at least n columns 
        # so that the diagonal elements A[i, i] exist for all i in 0..n-1.
        if m >= n:
            discs = []
            for i in range(n):
                c = complex(A[i, i])
                r = sum(abs(complex(A[i, j])) for j in range(m) if j != i)
                discs.append((c, r))
            
            disjoint = True
            for i in range(n):
                for j in range(i + 1, n):
                    c1, r1 = discs[i]
                    c2, r2 = discs[j]
                    # Discs are disjoint if the distance between centers is strictly greater than the sum of radii
                    if abs(c1 - c2) <= r1 + r2:
                        disjoint = False
                        break
                if not disjoint:
                    break
            h1_ok = disjoint
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: A is NOT diagonalizable over the complex numbers
    neg_q_ok = False
    try:
        if not A.is_square:
            # Non-square matrices are not diagonalizable
            neg_q_ok = True
        else:
            # For square matrices, check if it is diagonalizable
            res = A.is_diagonalizable()
            if res is False:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The n Gershgorin discs of A are mutually disjoint",
    "¬Q: A is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1