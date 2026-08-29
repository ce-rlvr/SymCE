import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that V is n-dimensional (i.e., M is square).
    """
    try:
        # The witness can be just the matrix M, or a tuple (v_list, M)
        if isinstance(witness, tuple) and len(witness) == 2:
            v_list, M = witness
            try:
                cols = [sp.Matrix(v) for v in v_list]
                expected_M = sp.Matrix.hstack(*cols)
                h2 = bool(M == expected_M)
            except Exception:
                h2 = False
        else:
            M = witness
            h2 = True
            
        if not hasattr(M, 'rows') or not hasattr(M, 'cols'):
            return [False, False, False]
            
        # H_1: v_1, ..., v_n is a basis of V
        # This holds if the columns of M are linearly independent (they form a basis for their span).
        try:
            h1 = bool(M.rank() == M.cols)
        except Exception:
            h1 = False
            
        # Conclusion: |\det(M)| \le \prod_{i=1}^n \|v_i\|
        # If M is not square, det(M) is undefined, so the conclusion fails (neg_q = True).
        try:
            if M.rows != M.cols:
                neg_q = True
            else:
                det_val = abs(M.det())
                prod_norms = 1
                for i in range(M.cols):
                    prod_norms *= M.col(i).norm()
                
                diff = prod_norms - det_val
                
                # Check if det_val > prod_norms (i.e., diff < 0)
                if diff.is_real and diff.is_number:
                    neg_q = bool(diff < 0)
                else:
                    val = diff.evalf()
                    if val.is_real and val.is_number:
                        neg_q = bool(val < 0)
                    else:
                        diff_simp = sp.simplify(diff)
                        if diff_simp.is_real and diff_simp.is_number:
                            neg_q = bool(diff_simp < 0)
                        else:
                            val_simp = diff_simp.evalf()
                            if val_simp.is_real and val_simp.is_number:
                                neg_q = bool(val_simp < 0)
                            else:
                                neg_q = False
        except Exception:
            # If determinant or norm calculation fails, the conclusion is undefined/fails.
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: v_1, v_2, \\dots, v_n is a basis of V",
    "H_2: M is the matrix whose columns are v_1, v_2, \\dots, v_n",
    "¬Q: |\\det(M)| > \\prod_{i=1}^n \\|v_i\\| or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2