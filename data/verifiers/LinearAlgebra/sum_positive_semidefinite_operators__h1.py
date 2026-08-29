import sympy
from sympy.matrices import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_psd(M):
    try:
        if not hasattr(M, 'is_square') or not M.is_square:
            return False
        # A positive semi-definite operator must be Hermitian (symmetric for real matrices)
        if M != M.H:
            return False
        
        # Use SymPy's built-in property if it can definitively answer
        if hasattr(M, 'is_positive_semidefinite'):
            res = M.is_positive_semidefinite
            if res is not None:
                return bool(res)
                
        # Fallback to checking eigenvalues
        evs = M.eigenvals()
        for ev in evs:
            try:
                if ev.is_real is False:
                    return False
                if ev.is_real is True and ev.is_negative is True:
                    return False
                # Try numerical evaluation for complex/real values
                c = complex(ev)
                if abs(c.imag) > 1e-9:
                    return False
                if c.real < -1e-9:
                    return False
            except Exception:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        T1, T2 = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_psd(T1)
    except Exception:
        h1 = False
        
    try:
        h2 = is_psd(T2)
    except Exception:
        h2 = False
        
    try:
        # The conclusion is that T1 + T2 is positive semi-definite.
        # We want the negated conclusion (i.e., T1 + T2 is NOT positive semi-definite).
        neg_q = not is_psd(T1 + T2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T_1 is a positive semi-definite linear operator on V",
    "H_2: T_2 is a positive semi-definite linear operator on V",
    "¬Q: The linear operator T_1 + T_2 is not positive semi-definite"
]

N_HYP = 2
NEG_Q_INDEX = 2