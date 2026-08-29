import sympy as sp
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H_1: A is an n x n complex matrix
        if not hasattr(witness, 'rows') or not hasattr(witness, 'cols'):
            return [False, False]
        if witness.rows != witness.cols:
            return [False, False]
        
        h1 = True
        
        # To evaluate the conclusion as intended by the false conjecture,
        # we must compute the compact SVD. The conjecture assumes that 
        # Q = U V^* is unitary, which is only true for the full SVD or 
        # when the matrix is invertible.
        try:
            U_full, S_full, V_full = witness.singular_value_decomposition()
        except Exception:
            return [False, False]
            
        r = 0
        for i in range(S_full.rows):
            val = sp.simplify(S_full[i, i])
            if hasattr(val, 'is_real') and val.is_real and hasattr(val, 'is_number') and val.is_number:
                try:
                    if abs(float(val)) > 1e-9:
                        r += 1
                except Exception:
                    if val != 0:
                        r += 1
            else:
                if hasattr(val, 'is_zero') and val.is_zero is False:
                    r += 1
                elif val != 0:
                    r += 1
                    
        U = U_full[:, :r]
        S = S_full[:r, :r]
        V = V_full[:, :r]
        
        P = U * S * U.H
        Q = U * V.H
        
        # Check if A == P * Q
        diff = sp.simplify(witness - P * Q)
        if hasattr(diff, 'is_zero_matrix'):
            eq_check = diff.is_zero_matrix
        else:
            eq_check = None
            
        if eq_check is None:
            eq_check = all(sp.simplify(diff[i, j]) == 0 for i in range(diff.rows) for j in range(diff.cols))
            
        # Check if Q is unitary (Q * Q^H == I and Q^H * Q == I)
        I = sp.eye(witness.rows)
        diff_Q1 = sp.simplify(Q * Q.H - I)
        diff_Q2 = sp.simplify(Q.H * Q - I)
        
        if hasattr(diff_Q1, 'is_zero_matrix'):
            q1_zero = diff_Q1.is_zero_matrix
        else:
            q1_zero = None
        if q1_zero is None:
            q1_zero = all(sp.simplify(diff_Q1[i, j]) == 0 for i in range(diff_Q1.rows) for j in range(diff_Q1.cols))
            
        if hasattr(diff_Q2, 'is_zero_matrix'):
            q2_zero = diff_Q2.is_zero_matrix
        else:
            q2_zero = None
        if q2_zero is None:
            q2_zero = all(sp.simplify(diff_Q2[i, j]) == 0 for i in range(diff_Q2.rows) for j in range(diff_Q2.cols))
            
        q_unitary = q1_zero and q2_zero
        
        # The conclusion claims A = P Q and Q is unitary.
        # (P is positive semi-definite by construction).
        conclusion = eq_check and q_unitary
        neg_q = not conclusion
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The factorization A = P Q with P = U \\Sigma U^* PSD and Q = U V^* unitary fails"
]
N_HYP = 1
NEG_Q_INDEX = 1