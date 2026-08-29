import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    U = witness
    
    def is_zero(M):
        if getattr(M, 'is_zero_matrix', False):
            return True
        try:
            return all(e == 0 for e in M)
        except Exception:
            return False

    # H_1: Assume U is a unitary matrix.
    h1_ok = False
    try:
        if hasattr(U, 'is_unitary'):
            val = U.is_unitary
            if callable(val):
                val = val()
            if val is not None:
                h1_ok = bool(val)
                
        if not h1_ok and hasattr(U, 'shape') and hasattr(U, 'H'):
            if len(U.shape) == 2 and U.shape[0] == U.shape[1]:
                n = U.shape[0]
                I_mat = eye(n)
                prod1 = U.H * U
                prod2 = U * U.H
                if prod1 == I_mat and prod2 == I_mat:
                    h1_ok = True
                else:
                    try:
                        diff1 = sympy.simplify(prod1 - I_mat)
                        diff2 = sympy.simplify(prod2 - I_mat)
                        if is_zero(diff1) and is_zero(diff2):
                            h1_ok = True
                    except Exception:
                        pass
    except Exception:
        h1_ok = False

    # neg_Q: U is not unitarily diagonalizable
    neg_q_ok = False
    try:
        # Check if square
        is_sq = True
        if hasattr(U, 'shape') and len(U.shape) == 2:
            if U.shape[0] != U.shape[1]:
                is_sq = False
        elif hasattr(U, 'is_square'):
            val = U.is_square
            if callable(val):
                val = val()
            if val is False:
                is_sq = False
                
        if not is_sq:
            neg_q_ok = True
        else:
            # Check normality
            is_norm = None
            if hasattr(U, 'is_normal'):
                val = U.is_normal
                if callable(val):
                    val = val()
                is_norm = val
            elif hasattr(U, 'H'):
                prod1 = U.H * U
                prod2 = U * U.H
                if prod1 == prod2:
                    is_norm = True
                else:
                    try:
                        diff = sympy.simplify(prod1 - prod2)
                        if is_zero(diff):
                            is_norm = True
                        else:
                            is_norm = False
                    except Exception:
                        pass
                        
            if is_norm is False:
                neg_q_ok = True
            elif is_norm is True:
                # Check diagonalizability
                is_diag = None
                try:
                    if hasattr(U, 'is_diagonalizable'):
                        val = U.is_diagonalizable
                        if callable(val):
                            val = val()
                        is_diag = val
                except Exception:
                    pass
                    
                if is_diag is False:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: U is not unitarily diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1