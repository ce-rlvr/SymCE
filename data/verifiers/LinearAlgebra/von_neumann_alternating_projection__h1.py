import sympy as sp

# Top-level setup for standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P1 and P2 are orthogonal projection operators onto closed subspaces M1 and M2 of H",
    "H_2: x is an arbitrary vector in H",
    "not Q: The sequence (P1 P2)^n x does NOT converge in norm to the orthogonal projection of x onto M1 \\cap M2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_zero(val):
    try:
        return abs(complex(sp.N(val))) < 1e-9
    except Exception:
        return False

def is_zero_mat(M):
    try:
        for i in range(M.rows):
            for j in range(M.cols):
                if not is_zero(M[i, j]):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        P1, P2, x = witness
    except Exception:
        return [False, False, False]
        
    try:
        if not isinstance(P1, sp.MatrixBase) or not isinstance(P2, sp.MatrixBase) or not isinstance(x, sp.MatrixBase):
            return [False, False, False]
        n = P1.rows
        if P1.cols != n or P2.rows != n or P2.cols != n or x.rows != n or x.cols != 1:
            return [False, False, False]
            
        # H1: P1 and P2 are orthogonal projections (P^2 = P and P^H = P)
        diff1 = P1 * P1 - P1
        diff2 = P1.H - P1
        diff3 = P2 * P2 - P2
        diff4 = P2.H - P2
        h1 = bool(is_zero_mat(diff1) and is_zero_mat(diff2) and is_zero_mat(diff3) and is_zero_mat(diff4))
    except Exception:
        h1 = False
        
    try:
        # H2: x is an arbitrary vector in H
        h2 = True
    except Exception:
        h2 = False
        
    try:
        # Conclusion: limit of (P1 P2)^n x is P_{M1 \cap M2} x
        I = sp.eye(n)
        
        # M1 \cap M2 is exactly the nullspace of (I - P1) + (I - P2)
        M = (I - P1) + (I - P2)
        nullspace = M.nullspace()
        
        if not nullspace:
            P_int = sp.zeros(n, n)
        else:
            B = sp.Matrix.hstack(*nullspace)
            # Orthogonal projection onto the column space of B
            P_int = B * (B.H * B).inv() * B.H
            
        expected_limit = P_int * x
        
        # Compute the exact limit of (P1 P2)^n x using the Jordan form
        A = P1 * P2
        P_mat, J = A.jordan_form()
        limit_J = sp.zeros(n, n)
        diverges = False
        
        for i in range(n):
            val = J[i, i]
            if is_zero(val - 1):
                limit_J[i, i] = 1
                # Check for Jordan blocks of size > 1 for eigenvalue 1
                if i < n - 1 and not is_zero(J[i, i+1]) and is_zero(J[i+1, i+1] - 1):
                    diverges = True
            else:
                try:
                    abs_val = abs(complex(sp.N(val)))
                    if abs_val < 1.0 - 1e-9:
                        limit_J[i, i] = 0
                    else:
                        diverges = True
                except Exception:
                    diverges = True
                    
        if diverges:
            q = False
        else:
            actual_limit = P_mat * limit_J * P_mat.inv() * x
            diff = actual_limit - expected_limit
            q = is_zero_mat(diff)
            
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]