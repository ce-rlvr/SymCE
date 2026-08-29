import sympy
from sympy import eye, zeros, Matrix
from sympy.abc import x, y, z
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is a unitary matrix
    try:
        if not getattr(witness, 'is_square', False):
            h1 = False
        else:
            n = witness.shape[0]
            I = eye(n)
            prod1 = witness * witness.adjoint()
            prod2 = witness.adjoint() * witness
            if prod1 == I and prod2 == I:
                h1 = True
            else:
                diff1 = sympy.simplify(prod1 - I)
                diff2 = sympy.simplify(prod2 - I)
                h1 = bool(all(e == 0 for e in diff1) and all(e == 0 for e in diff2))
    except Exception:
        h1 = False

    # neg_Q: The condition number of U with respect to the 2-norm is NOT exactly 1
    try:
        n1 = witness.norm(2)
        n2 = witness.inv().norm(2)
        cond = sympy.simplify(n1 * n2)
        if cond == 1:
            neg_q = False
        else:
            try:
                neg_q = bool(abs(float(cond) - 1.0) > 1e-12)
            except Exception:
                neg_q = True
    except Exception:
        # If norm or inverse is undefined (e.g., for 0x0 matrix), condition number is not 1.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The condition number of U with respect to the 2-norm is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1