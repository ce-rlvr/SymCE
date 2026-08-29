import sympy
from sympy import Matrix, eye, zeros, Rational
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        else:
            is_real = True
            for elem in witness:
                try:
                    sym_elem = sympy.sympify(elem)
                    if sym_elem.is_real is False:
                        is_real = False
                        break
                except Exception:
                    is_real = False
                    break
            
            if not is_real:
                h1 = False
            else:
                n = witness.rows
                I = eye(n)
                diff = sympy.simplify(witness.T * witness - I)
                h1 = (diff == zeros(n, n))
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, Matrix):
            neg_q = False
        elif witness.rows != witness.cols:
            neg_q = False
        else:
            n = witness.rows
            I = eye(n)
            diff2 = sympy.simplify(witness**2 + I)
            neg_q = (diff2 != zeros(n, n))
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "¬Q: Q^2 is not equal to -I"
]

N_HYP = 1
NEG_Q_INDEX = 1