import sympy
from sympy import eye, zeros
from sympy.matrices.normalforms import smith_normal_form, hermite_normal_form

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def safe_hnf(M):
    if M.rows == 0 or M.cols == 0:
        return M
    return hermite_normal_form(M)

def inv_factors(A, n_cols):
    if A.rows == 0 or A.cols == 0:
        return [0] * n_cols
    S = smith_normal_form(A)
    factors = []
    for i in range(min(S.rows, S.cols)):
        val = abs(S[i, i])
        if val > 1:
            factors.append(val)
    rank_A = sum(1 for i in range(min(S.rows, S.cols)) if S[i, i] != 0)
    factors.extend([0] * (n_cols - rank_A))
    return sorted(factors)

def conditions(witness):
    """
    Witness is expected to be a tuple (A, B) of sympy.Matrix objects.
    M is the finitely generated abelian group Z^n / rowspan(A).
    N is the subgroup rowspan(B) / rowspan(A).
    """
    try:
        A, B = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a principal ideal domain
    # We are working over Z, which is a PID.
    h1 = True
    
    # H_2: M is an R-module (and N is a valid submodule)
    try:
        if not isinstance(A, sympy.Matrix) or not isinstance(B, sympy.Matrix):
            h2 = False
        elif A.cols != B.cols:
            h2 = False
        else:
            H_B = safe_hnf(B)
            H_BA = safe_hnf(B.col_join(A))
            def non_zero_rows(M):
                return [M.row(i) for i in range(M.rows) if not all(x == 0 for x in M.row(i))]
            # N is a submodule iff rowspan(A) is a subset of rowspan(B)
            h2 = non_zero_rows(H_B) == non_zero_rows(H_BA)
    except Exception:
        h2 = False
        
    # H_3: There exists a non-zero element r in R such that r x = 0 for all x in N
    # This means N is of bounded order (finite), which is true iff rank(A) == rank(B).
    try:
        if not h2:
            h3 = False
        else:
            h3 = (A.rank() == B.rank())
    except Exception:
        h3 = False
        
    # neg_Q: N is NOT a direct summand of M
    try:
        if not h2:
            neg_q = False
        else:
            inv_M = inv_factors(A, A.cols)
            
            H_B = safe_hnf(B)
            nz_rows = [H_B.row(i) for i in range(H_B.rows) if not all(x == 0 for x in H_B.row(i))]
            if not nz_rows:
                # N is trivial, so it is a direct summand
                neg_q = False
            else:
                B_prime = sympy.Matrix(nz_rows)
                k = B_prime.rows
                
                # Find Y such that Y * B_prime = A
                M_mat = B_prime * B_prime.T
                Y_rat = A * B_prime.T * M_mat.inv()
                Y = sympy.Matrix(Y_rat.rows, Y_rat.cols, lambda i, j: int(Y_rat[i, j]))
                
                mY, nY = Y.rows, Y.cols
                mB, nB = B.rows, B.cols
                
                # Block diagonal matrix representing N \oplus (M/N)
                Y_B = sympy.zeros(mY + mB, nY + nB)
                if mY > 0 and nY > 0:
                    Y_B[:mY, :nY] = Y
                if mB > 0 and nB > 0:
                    Y_B[mY:, nY:] = B
                    
                inv_sum = inv_factors(Y_B, nY + nB)
                
                # N is a direct summand iff M is isomorphic to N \oplus (M/N)
                neg_q = (inv_M != inv_sum)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is an R-module",
    "H_3: There exists a non-zero element r in R such that r x = 0 for all x in N",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 3
NEG_Q_INDEX = 3