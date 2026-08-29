import sympy
from sympy import MatrixBase, eye, zeros, simplify, expand, Integer, Rational, Float, Expr, Matrix
from sympy.abc import *

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                x, n = witness
            elif len(witness) == 3:
                R, x, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # H_1: R is a ring
        # We assume the implicit or explicit R is a ring if x is a valid element
        h1 = True
        
        # H_2: x is an element of R
        if isinstance(x, MatrixBase):
            h2 = x.is_square
        elif isinstance(x, (int, Integer, Rational, float, Float, Expr)):
            h2 = True
        else:
            h2 = False
            
        if not isinstance(n, (int, Integer)) or n < 1 or n > 10000:
            h2 = False
            
    except Exception:
        return [False, False, False]

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            one = eye(x.rows) if isinstance(x, MatrixBase) else 1
            zero = zeros(x.rows, x.cols) if isinstance(x, MatrixBase) else 0
            
            S = zero
            x_pow = one
            for i in range(int(n)):
                S = S + x_pow
                x_pow = x_pow * x
                
            term1 = (one - x) * S
            term2 = S * (one - x)
            
            if isinstance(x, MatrixBase):
                diff1 = expand(term1 - one)
                diff2 = expand(term2 - one)
                is_inv = diff1.is_zero_matrix and diff2.is_zero_matrix
            else:
                is_inv = (simplify(term1 - one) == 0) and (simplify(term2 - one) == 0)
                
            neg_q = not is_inv
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x is an element of R",
    "¬Q: 1 - x is not invertible or its inverse is not \\sum_{i=0}^{n-1} x^i"
]

N_HYP = 2
NEG_Q_INDEX = 2