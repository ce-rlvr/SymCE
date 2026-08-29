import sympy as sp

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    
    The conjecture claims that if B is obtained by deleting a single column from A,
    then the singular values satisfy sigma_i(A) >= sigma_i(B) >= sigma_{i+1}(A) for all i >= 1.
    
    We evaluate the hypotheses and the negation of the conclusion.
    """
    # H1: A is an m x n complex matrix
    # H2: B is an m x (n-1) submatrix of A obtained by deleting a single column from A
    # neg_Q: The interlacing inequalities fail for some i >= 1
    
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        A, B = witness
        if isinstance(A, sp.Matrix) and isinstance(B, sp.Matrix):
            m, n = A.shape
            if m >= 1 and n >= 1:
                h1_ok = True
    except Exception:
        pass

    try:
        if h1_ok:
            m, n = A.shape
            mB, nB = B.shape
            if mB == m and nB == n - 1:
                # Check if B is obtained by deleting a single column from A
                is_submatrix = False
                for col_to_delete in range(n):
                    # Construct matrix by deleting the column
                    cols = [A[:, j] for j in range(n) if j != col_to_delete]
                    if cols:
                        A_del = sp.Matrix.hstack(*cols)
                    else:
                        A_del = sp.zeros(m, 0)
                    
                    if A_del == B:
                        is_submatrix = True
                        break
                h2_ok = is_submatrix
    except Exception:
        pass

    try:
        if h1_ok and h2_ok:
            # Compute singular values of A and B
            # Singular values are the square roots of the eigenvalues of A*A or A*A
            # We can just check the eigenvalues of A*A and B*B
            A_H_A = A.H * A
            B_H_B = B.H * B
            
            # Get eigenvalues, sort in descending order
            ev_A = list(A_H_A.eigenvals(multiple=True))
            ev_B = list(B_H_B.eigenvals(multiple=True))
            
            # Convert to float for comparison, taking max(0, ev) to avoid small negative numerical errors
            ev_A = sorted([max(0, float(sp.re(ev))) for ev in ev_A], reverse=True)
            ev_B = sorted([max(0, float(sp.re(ev))) for ev in ev_B], reverse=True)
            
            # Singular values are square roots of eigenvalues
            sv_A = [sp.sqrt(ev) for ev in ev_A]
            sv_B = [sp.sqrt(ev) for ev in ev_B]
            
            # Pad with zeros to allow checking for all i >= 1
            max_len = max(len(sv_A), len(sv_B)) + 2
            sv_A.extend([0.0] * (max_len - len(sv_A)))
            sv_B.extend([0.0] * (max_len - len(sv_B)))
            
            # Check if interlacing inequalities hold for all i >= 1
            # sigma_i(A) >= sigma_i(B) >= sigma_{i+1}(A)
            # Note: 1-based indexing in math means i-1 in Python
            interlacing_holds = True
            for i in range(max_len - 1):
                sigma_i_A = sv_A[i]
                sigma_i_B = sv_B[i]
                sigma_i_plus_1_A = sv_A[i+1]
                
                # Use a small tolerance for floating point comparisons
                tol = 1e-9
                if not (sigma_i_A + tol >= sigma_i_B and sigma_i_B + tol >= sigma_i_plus_1_A):
                    interlacing_holds = False
                    break
            
            neg_q_ok = not interlacing_holds
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "H_2: B is an m x (n-1) submatrix of A obtained by deleting a single column from A",
    "¬Q: The interlacing inequalities sigma_i(A) >= sigma_i(B) >= sigma_{i+1}(A) fail for some i >= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2