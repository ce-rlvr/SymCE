import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
            
        if not isinstance(A, Matrix):
            A = Matrix(A)
        if not isinstance(B, Matrix):
            B = Matrix(B)
    except Exception:
        return [False, False]

    # H_1: A is an n x n real positive semidefinite matrix and B is an n x n real matrix
    h1_ok = False
    try:
        if A.is_square and B.is_square and A.shape == B.shape and A.shape[0] > 0:
            if all(val.is_real for val in A) and all(val.is_real for val in B):
                if A == A.T:
                    evs = A.eigenvals()
                    is_psd = True
                    for ev in evs:
                        try:
                            re_part = sympy.re(ev).evalf()
                            im_part = sympy.im(ev).evalf()
                            if abs(float(im_part)) > 1e-7:
                                is_psd = False
                                break
                            if float(re_part) < -1e-7:
                                is_psd = False
                                break
                        except TypeError:
                            is_psd = False
                            break
                    if is_psd:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: tr(AB) < 0
    neg_q_ok = False
    try:
        if h1_ok:
            tr = (A * B).trace()
            if float(sympy.re(tr).evalf()) < -1e-7:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an n x n real positive semidefinite matrix and B is an n x n real matrix",
    "¬Q: tr(AB) < 0"
]

N_HYP = 1
NEG_Q_INDEX = 1