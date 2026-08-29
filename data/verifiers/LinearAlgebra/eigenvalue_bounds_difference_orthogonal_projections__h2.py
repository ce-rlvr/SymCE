import sympy
from sympy import zeros, simplify, eye
from sympy.matrices import Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    try:
        if getattr(M, 'is_zero_matrix', False) is True:
            return True
    except Exception:
        pass
    try:
        if M == zeros(*M.shape):
            return True
    except Exception:
        pass
    try:
        return simplify(M) == zeros(*M.shape)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            Q = witness.get('Q')
            lam = witness.get('lam', witness.get('lambda'))
        else:
            P, Q, lam = witness
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if hasattr(P, 'is_square') and P.is_square and hasattr(Q, 'is_square') and Q.is_square:
            if P.shape == Q.shape:
                if is_zero_mat(P * P - P) and is_zero_mat(P.H - P):
                    if is_zero_mat(Q * Q - Q) and is_zero_mat(Q.H - Q):
                        h1_ok = True
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        if hasattr(lam, 'is_Matrix') and lam.is_Matrix:
            neg_q = True
        else:
            try:
                c = complex(lam)
                if abs(c.imag) > 1e-9:
                    neg_q = True
                else:
                    neg_q = not (-1 <= c.real <= 1)
            except Exception:
                if getattr(lam, 'is_real', None) is False:
                    neg_q = True
                else:
                    neg_q = bool(lam < -1 or lam > 1)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q are orthogonal projection matrices of the same dimension",
    "¬Q: lambda is not a real number between -1 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1