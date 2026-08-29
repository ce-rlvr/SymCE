import sympy
from sympy import eye, zeros, simplify, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: Q is an orthogonal matrix
    def check_h1(Q):
        try:
            if not hasattr(Q, 'rows') or not hasattr(Q, 'cols'):
                return False
            
            I_cols = eye(Q.cols)
            if Q.T * Q == I_cols:
                return True
                
            I_rows = eye(Q.rows)
            if Q * Q.T == I_rows:
                return True
                
            diff1 = simplify(Q.T * Q - I_cols)
            if hasattr(diff1, 'is_zero_matrix') and diff1.is_zero_matrix:
                return True
            if diff1 == zeros(Q.cols, Q.cols):
                return True
                
            diff2 = simplify(Q * Q.T - I_rows)
            if hasattr(diff2, 'is_zero_matrix') and diff2.is_zero_matrix:
                return True
            if diff2 == zeros(Q.rows, Q.rows):
                return True
                
            return False
        except Exception:
            return False

    # H2: Q is an upper triangular matrix
    def check_h2(Q):
        try:
            for i in range(Q.rows):
                for j in range(Q.cols):
                    if i > j:
                        val = Q[i, j]
                        if val != 0 and simplify(val) != 0:
                            return False
            return True
        except Exception:
            return False

    # Conclusion: Q is a diagonal matrix with all diagonal entries equal to 1 or -1
    def check_conclusion(Q):
        try:
            is_diag = True
            for i in range(Q.rows):
                for j in range(Q.cols):
                    if i != j:
                        val = Q[i, j]
                        if val != 0 and simplify(val) != 0:
                            is_diag = False
                            break
                if not is_diag:
                    break
            
            if not is_diag:
                return False
                
            for i in range(min(Q.rows, Q.cols)):
                val = simplify(Q[i, i])
                if val != 1 and val != -1:
                    return False
                    
            return True
        except Exception:
            return False

    h1_ok = check_h1(witness)
    h2_ok = check_h2(witness)
    
    try:
        conc_ok = check_conclusion(witness)
        neg_q_ok = not conc_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: Q is an upper triangular matrix",
    "¬Q: Q is not a diagonal matrix with all diagonal entries equal to 1 or -1"
]

N_HYP = 2
NEG_Q_INDEX = 2