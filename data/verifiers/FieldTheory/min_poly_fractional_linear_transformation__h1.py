import sympy
from sympy import eye, zeros, minpoly
from sympy.matrices import MatrixBase
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (alpha, n, a, b, c, d)
    where alpha can be a scalar (algebraic number) or a square matrix.
    """
    try:
        if len(witness) != 6:
            return [False, False, False, False]
        alpha, n, a, b, c, d = witness
    except Exception:
        return [False, False, False, False]

    # H_1: The minimal polynomial of alpha over F has degree n
    try:
        if isinstance(alpha, MatrixBase):
            deg_alpha = alpha.minimal_polynomial(x).degree()
        else:
            deg_alpha = minpoly(alpha, x).degree()
        h1 = bool(deg_alpha == n)
    except Exception:
        h1 = False

    # H_2: a, b, c, d in F are scalars such that ad - bc != 0
    try:
        if any(isinstance(var, MatrixBase) for var in (a, b, c, d)):
            h2 = False
        else:
            h2 = bool(a*d - b*c != 0)
    except Exception:
        h2 = False

    # H_3: c*alpha + d != 0
    try:
        if isinstance(alpha, MatrixBase):
            I = eye(alpha.shape[0])
            val = c*alpha + d*I
            h3 = bool(val != zeros(*val.shape))
        else:
            h3 = bool(c*alpha + d != 0)
    except Exception:
        h3 = False

    # Conclusion: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F has degree n
    try:
        if isinstance(alpha, MatrixBase):
            I = eye(alpha.shape[0])
            num = a*alpha + b*I
            den = c*alpha + d*I
            # If den is not invertible, this will raise an exception
            beta = num * den.inv()
            deg_beta = beta.minimal_polynomial(x).degree()
        else:
            beta = (a*alpha + b) / (c*alpha + d)
            deg_beta = minpoly(beta, x).degree()
        q = bool(deg_beta == n)
    except Exception:
        # If division by zero or matrix inversion fails, the conclusion is undefined (hence fails)
        q = False

    neg_q = not q

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The minimal polynomial of alpha over F has degree n",
    "H_2: a, b, c, d in F are scalars such that ad - bc != 0",
    "H_3: c*alpha + d != 0",
    "¬Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does not have degree n (or is undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3