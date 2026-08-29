import sympy
from sympy import Matrix, I, re, eye, zeros, sympify

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (T, lambda) or a dict with keys 'T' and 'lambda'.
    """
    try:
        if isinstance(witness, dict):
            T_raw = witness.get('T')
            lam = witness.get('lambda', witness.get('lam'))
        else:
            T_raw, lam = witness
            
        if not isinstance(T_raw, Matrix):
            T = Matrix(T_raw)
        else:
            T = T_raw
    except Exception:
        return [False, False, False]

    # H_1: V is a complex inner product space (T is a square matrix representing an operator on V)
    try:
        h1 = bool(T.is_square)
    except Exception:
        h1 = False

    # H_2: T is a skew-adjoint linear operator on V
    try:
        if T.H == -T:
            h2 = True
        else:
            h2 = bool(sympy.simplify(T.H + T).is_zero_matrix)
    except Exception:
        h2 = False

    # ¬Q: The real part of lambda is not zero
    try:
        lam_sym = sympify(lam)
        # is_zero is False when it is strictly non-zero (avoids True for symbolic expressions)
        neg_q = (sympy.re(lam_sym).is_zero is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a complex inner product space (T is a square matrix)",
    "H_2: T is a skew-adjoint linear operator on V",
    "¬Q: The real part of lambda is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2