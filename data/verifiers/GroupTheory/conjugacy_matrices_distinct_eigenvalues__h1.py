import sympy as sp
import z3
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False]*4 + [False]
        
    # H1: n is a positive integer
    try:
        if not (isinstance(A, sp.MatrixBase) and isinstance(B, sp.MatrixBase)):
            h1 = False
        else:
            n = A.shape[0]
            h1 = (A.shape == (n, n) and B.shape == (n, n) and n > 0)
    except Exception:
        h1 = False

    # H2: A and B are matrices in the general linear group GL_n(F)
    # We evaluate this over F=Z, which is the domain of the standard counterexamples.
    # Over Z, a matrix is in GL_n(Z) iff its determinant is 1 or -1.
    try:
        if h1:
            A_is_int = all(A[i, j].is_integer == True for i in range(n) for j in range(n))
            B_is_int = all(B[i, j].is_integer == True for i in range(n) for j in range(n))
            h2 = A_is_int and B_is_int and abs(A.det()) == 1 and abs(B.det()) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: A and B each have n distinct eigenvalues in F
    try:
        if h1:
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            
            A_evals_int = all(e.is_integer == True for e in evals_A.keys())
            B_evals_int = all(e.is_integer == True for e in evals_B.keys())
            
            h3 = (len(evals_A) == n and len(evals_B) == n and A_evals_int and B_evals_int)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: A and B have the exact same set of eigenvalues
    try:
        if h1:
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            h4 = (set(evals_A.keys()) == set(evals_B.keys()))
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: A and B are NOT conjugate in GL_n(F)
    try:
        if h1 and h2:
            solver = z3.Solver()
            P_vars = [[z3.Int(f'p_{i}_{j}') for j in range(n)] for i in range(n)]
            
            for i in range(n):
                for j in range(n):
                    lhs = sum(P_vars[i][k] * int(A[k, j]) for k in range(n))
                    rhs = sum(int(B[i][k]) * P_vars[k][j] for k in range(n))
                    solver.add(lhs == rhs)
                    
            def z3_det(matrix):
                m = len(matrix)
                if m == 1:
                    return matrix[0][0]
                if m == 2:
                    return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
                det = 0
                for c in range(m):
                    sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                    sign = 1 if c % 2 == 0 else -1
                    det += sign * matrix[0][c] * z3_det(sub_matrix)
                return det

            detP = z3_det(P_vars)
            solver.add(z3.Or(detP == 1, detP == -1))
            
            is_conjugate = (solver.check() == z3.sat)
            neg_q = not is_conjugate
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: A and B are matrices in the general linear group GL_n(F)",
    "H_3: A and B each have n distinct eigenvalues in F",
    "H_4: A and B have the exact same set of eigenvalues",
    "¬Q: A and B are not conjugate in GL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4