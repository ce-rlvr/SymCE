import sympy as sp

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a list or tuple of integers representing a finite simple continued fraction.
    """
    # H_1: Let the witness be a finite simple continued fraction
    try:
        if not isinstance(witness, (list, tuple)):
            h1 = False
        elif len(witness) == 0:
            h1 = False
        else:
            h1 = True
            if not isinstance(witness[0], int):
                h1 = False
            for a in witness[1:]:
                if not isinstance(a, int) or a < 1:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: The numerator p_n is NOT equal to the determinant of the specified matrix M
    try:
        n = len(witness) - 1
        
        # Calculate p_n using the standard recurrence
        p_prev2 = 0
        p_prev1 = 1
        for a in witness:
            curr = a * p_prev1 + p_prev2
            p_prev2 = p_prev1
            p_prev1 = curr
        p_n = p_prev1
        
        # Calculate the determinant of the matrix M
        M = sp.zeros(n + 1, n + 1)
        for i in range(n + 1):
            M[i, i] = witness[i]
        for i in range(n):
            M[i, i + 1] = 1
            M[i + 1, i] = -1
            
        det_M = M.det()
        
        # The conclusion is that p_n == det_M. We want the negation.
        neg_q = (p_n != det_M)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is a finite simple continued fraction",
    "¬Q: The numerator p_n is NOT equal to the determinant of the specified tridiagonal matrix M"
]

N_HYP = 1
NEG_Q_INDEX = 1