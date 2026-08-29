import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    witness: tuple (B, S, T, c)
    B: matrix of the non-degenerate bilinear form
    S, T: matrices of the linear operators
    c: scalar (or matrix, to demonstrate non-linearity)
    """
    try:
        B, S, T, c = witness
    except Exception:
        return [False, False, False]
        
    # H1: V is a finite-dimensional vector space equipped with a non-degenerate bilinear form
    try:
        if isinstance(B, sp.MatrixBase) and B.rows == B.cols and B.rows > 0:
            h1 = (B.det() != 0)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: S and T are linear operators on V
    try:
        if (isinstance(S, sp.MatrixBase) and S.rows == B.rows and S.cols == B.cols and
            isinstance(T, sp.MatrixBase) and T.rows == B.rows and T.cols == B.cols):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # Conclusion: The adjoint operation is linear, meaning the adjoint of S + T is S^* + T^* 
    # and the adjoint of cT is cT^*.
    # We check if this FAILS (neg_Q should be True if it fails).
    try:
        B_inv = B.inv()
        
        # The false conjecture might stem from confusing bilinear forms with inner products
        # (where the adjoint is conjugate-linear), or from assuming operators commute.
        # We evaluate the adjoint under both strict bilinear (transpose) and sesquilinear 
        # (conjugate transpose) interpretations. If the conclusion fails under EITHER 
        # intended interpretation, the witness is a valid counterexample.
        
        def get_adj_trans(M):
            return B_inv * M.transpose() * B
            
        def get_adj_conj(M):
            return B_inv * M.adjoint() * B
            
        def check_equal(M1, M2):
            if M1 == M2:
                return True
            diff = M1 - M2
            if diff == sp.zeros(M1.rows, M1.cols):
                return True
            diff_expanded = sp.expand(diff)
            if diff_expanded == sp.zeros(M1.rows, M1.cols):
                return True
            diff_simplified = sp.simplify(diff)
            if diff_simplified == sp.zeros(M1.rows, M1.cols):
                return True
            return False

        # Interpretation 1: Strict bilinear form (uses transpose)
        S_adj_t = get_adj_trans(S)
        T_adj_t = get_adj_trans(T)
        sum_cond_t = check_equal(get_adj_trans(S + T), S_adj_t + T_adj_t)
        cT_cond_t = check_equal(get_adj_trans(c * T), c * T_adj_t)
        
        # Interpretation 2: Sesquilinear form / inner product (uses conjugate transpose)
        S_adj_c = get_adj_conj(S)
        T_adj_c = get_adj_conj(T)
        sum_cond_c = check_equal(get_adj_conj(S + T), S_adj_c + T_adj_c)
        cT_cond_c = check_equal(get_adj_conj(c * T), c * T_adj_c)
        
        # The conclusion fails if it fails under at least one valid interpretation of the adjoint
        neg_q = (not (sum_cond_t and cT_cond_t)) or (not (sum_cond_c and cT_cond_c))
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space equipped with a non-degenerate bilinear form",
    "H_2: S and T are linear operators on V",
    "¬Q: The adjoint operation is not linear (adjoint of S+T != S^*+T^* or adjoint of cT != cT^*)"
]

N_HYP = 2
NEG_Q_INDEX = 2