import sympy
import math
from sympy import Matrix, eye, zeros, sympify, I

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ortho_proj(M):
    if len(M.shape) != 2 or M.shape[0] != M.shape[1]:
        return False
    
    # Fast path for exact symbolic or integer matrices
    if M**2 == M and M.H == M:
        return True
    
    # Fallback for floating point or unsimplified symbolic matrices
    diff1 = M**2 - M
    diff2 = M.H - M
    try:
        for val in diff1:
            if abs(complex(val)) > 1e-7:
                return False
        for val in diff2:
            if abs(complex(val)) > 1e-7:
                return False
        return True
    except TypeError:
        diff1 = sympy.simplify(diff1)
        diff2 = sympy.simplify(diff2)
        return diff1 == zeros(*M.shape) and diff2 == zeros(*M.shape)

def conditions(witness):
    # Extract P, Q, and lambda from the witness
    try:
        if isinstance(witness, dict):
            P = witness['P']
            Q = witness['Q']
            if 'lam' in witness:
                lam = witness['lam']
            elif 'lambda' in witness:
                lam = witness['lambda']
            elif '\\lambda' in witness:
                lam = witness['\\lambda']
            else:
                return [False, False]
        else:
            P, Q, lam = witness
    except Exception:
        return [False, False]
        
    # H_1: P and Q are orthogonal projection matrices of the same dimension
    try:
        if not (hasattr(P, 'shape') and hasattr(P, 'H')):
            P = sympy.Matrix(P)
        if not (hasattr(Q, 'shape') and hasattr(Q, 'H')):
            Q = sympy.Matrix(Q)
        h1 = is_ortho_proj(P) and is_ortho_proj(Q) and P.shape == Q.shape
    except Exception:
        h1 = False
        
    # ¬Q: \lambda is NOT a real number satisfying 0 < \lambda \le 1
    try:
        lam_sym = sympify(lam)
        if hasattr(lam_sym, 'shape'):
            neg_q = True
        else:
            try:
                val = float(lam_sym)
                if math.isnan(val):
                    neg_q = True
                else:
                    neg_q = bool(val <= 0 or val > 1)
            except TypeError:
                try:
                    cval = complex(lam_sym)
                    if math.isnan(cval.real) or math.isnan(cval.imag):
                        neg_q = True
                    elif abs(cval.imag) > 1e-9:
                        neg_q = True
                    else:
                        neg_q = bool(cval.real <= 0 or cval.real > 1)
                except TypeError:
                    # Cannot be evaluated to a number
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q are orthogonal projection matrices of the same dimension",
    "¬Q: \\lambda is not a real number satisfying 0 < \\lambda \\le 1"
]

N_HYP = 1
NEG_Q_INDEX = 1