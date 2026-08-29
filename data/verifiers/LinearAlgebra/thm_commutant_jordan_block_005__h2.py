import sympy
from sympy import eye, zeros, Matrix, Symbol, Rational, Integer
from sympy.abc import x, y, z, t, a, b, c, d
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_zero(val):
    if val == 0:
        return True
    try:
        if hasattr(val, 'is_zero') and val.is_zero is True:
            return True
        if hasattr(val, 'expand'):
            exp = val.expand()
            if hasattr(exp, 'is_zero') and exp.is_zero is True:
                return True
        simp = sympy.simplify(val)
        if hasattr(simp, 'is_zero') and simp.is_zero is True:
            return True
    except Exception:
        pass
    return False

def check_one(val):
    if val == 1:
        return True
    try:
        return check_zero(val - 1)
    except Exception:
        return False

def check_eq(val1, val2):
    if val1 == val2:
        return True
    try:
        return check_zero(val1 - val2)
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (J, X) where J is a Jordan block matrix
    and X is a matrix that commutes with J.
    """
    try:
        J, X = witness
    except Exception:
        return [False, False, False]
    
    # H_1: J is an n x n Jordan block matrix with eigenvalue lambda
    h1 = False
    try:
        if hasattr(J, 'is_square') and J.is_square:
            n = J.shape[0]
            if n > 0:
                lam = J[0, 0]
                is_upper = True
                is_lower = True
                for i in range(n):
                    for j in range(n):
                        if i == j:
                            if not check_eq(J[i, j], lam):
                                is_upper = False
                                is_lower = False
                        elif i + 1 == j:
                            if not check_one(J[i, j]):
                                is_upper = False
                            if not check_zero(J[i, j]):
                                is_lower = False
                        elif i == j + 1:
                            if not check_one(J[i, j]):
                                is_lower = False
                            if not check_zero(J[i, j]):
                                is_upper = False
                        else:
                            if not check_zero(J[i, j]):
                                is_upper = False
                                is_lower = False
                h1 = is_upper or is_lower
    except Exception:
        h1 = False

    # H_2: X commutes with J, satisfying XJ = JX
    h2 = False
    try:
        if hasattr(X, 'is_square') and X.is_square and X.shape == J.shape:
            n = X.shape[0]
            diff = X * J - J * X
            h2 = all(check_zero(diff[i, j]) for i in range(n) for j in range(n))
    except Exception:
        h2 = False

    # ¬Q: X is NOT an upper triangular Toeplitz matrix
    neg_q = False
    try:
        if hasattr(X, 'is_square') and X.is_square:
            n = X.shape[0]
            is_utt = True
            for i in range(n):
                for j in range(n):
                    if i > j:
                        # Below main diagonal must be zero
                        if not check_zero(X[i, j]):
                            is_utt = False
                    else:
                        # On or above main diagonal must be constant along diagonals
                        if not check_eq(X[i, j], X[0, j - i]):
                            is_utt = False
            neg_q = not is_utt
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: J is an n x n Jordan block matrix",
    "H_2: X commutes with J (XJ = JX)",
    "¬Q: X is not an upper triangular Toeplitz matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2