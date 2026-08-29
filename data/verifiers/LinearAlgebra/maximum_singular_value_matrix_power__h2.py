import sympy
from sympy import MatrixBase, Integer
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "The maximum singular value of A^k satisfies \sigma_{\max}(A^k) \le (\sigma_{\max}(A))^k."
    
    The witness should be a tuple (A, k) or a dict {'A': A, 'k': k}.
    """
    try:
        if isinstance(witness, dict):
            A_raw = witness.get('A')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A_raw, k = witness
        else:
            return [False, False, False]
            
        if not isinstance(A_raw, MatrixBase):
            A = sympy.Matrix(A_raw)
        else:
            A = A_raw
            
        h1 = isinstance(A, MatrixBase) and A.is_square and isinstance(k, (int, Integer)) and len(A.free_symbols) == 0
    except Exception:
        h1 = False

    # H2 is a definitional hypothesis about notation, which is vacuously true.
    h2 = True

    try:
        if not h1:
            neg_q = False
        else:
            sv_A = A.singular_values()
            if not sv_A:
                neg_q = False
            else:
                max_sv_A = max(sv_A)
                
                Ak = A**k
                sv_Ak = Ak.singular_values()
                max_sv_Ak = max(sv_Ak)
                
                # Evaluate numerically to avoid symbolic comparison issues
                val_Ak = float(abs(max_sv_Ak.evalf()))
                val_A_k = float(abs((max_sv_A**k).evalf()))
                
                # The conclusion is \sigma_{\max}(A^k) \le (\sigma_{\max}(A))^k
                # The negation is \sigma_{\max}(A^k) > (\sigma_{\max}(A))^k
                neg_q = val_Ak > val_A_k + 1e-9
    except Exception:
        # This will catch cases where A is not invertible but k < 0, etc.
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix and k is an integer",
    "H_2: sigma_max(M) denotes the maximum singular value of M",
    "¬Q: sigma_max(A^k) > (sigma_max(A))^k"
]

N_HYP = 2
NEG_Q_INDEX = 2