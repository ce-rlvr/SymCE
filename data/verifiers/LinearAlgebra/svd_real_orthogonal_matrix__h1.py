import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero(expr):
    """Helper to robustly check if a sympy expression is zero."""
    try:
        if expr == 0:
            return True
        simp_expr = sp.simplify(expr)
        if simp_expr == 0:
            return True
        exp_expr = sp.expand(simp_expr)
        if exp_expr == 0:
            return True
        try:
            # Fallback to numerical evaluation for constant expressions
            if abs(complex(exp_expr)) < 1e-9:
                return True
        except Exception:
            pass
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        # Ensure witness is a sympy Matrix
        if not isinstance(witness, sp.MatrixBase):
            witness = sp.Matrix(witness)
            
        n_rows, n_cols = witness.shape
        I_n = sp.eye(n_cols)
        
        # H_1: Q is an orthogonal matrix, meaning Q^T Q = I
        QT_Q = witness.T * witness
        diff_H1 = QT_Q - I_n
        h1_ok = all(is_zero(diff_H1[i, j]) for i in range(n_cols) for j in range(n_cols))
        
        # neg_Q: Not all n singular values of Q are equal to 1.
        # The singular values of Q are the square roots of the eigenvalues of Q^* Q.
        # Since Q^* Q is Hermitian, it is diagonalizable. All its eigenvalues are 1 
        # if and only if Q^* Q = I. Thus, not all singular values are 1 iff Q^* Q != I.
        QH_Q = witness.H * witness
        diff_neg_Q = QH_Q - I_n
        neg_q_ok = not all(is_zero(diff_neg_Q[i, j]) for i in range(n_cols) for j in range(n_cols))
        
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix (Q^T Q = I)",
    "¬Q: Not all singular values of Q are equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1