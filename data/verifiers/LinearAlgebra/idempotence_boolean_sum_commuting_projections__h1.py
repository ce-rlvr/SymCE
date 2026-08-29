import sympy
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(mat):
    try:
        if hasattr(mat, '__iter__'):
            for e in mat:
                if sympy.simplify(e) != 0:
                    return False
            return True
        else:
            return sympy.simplify(mat) == 0
    except Exception:
        return False

def conditions(witness):
    try:
        P, Q = witness
    except Exception:
        return [False, False]
        
    try:
        diff_h1 = P * Q - Q * P
        h1 = is_zero_mat(diff_h1)
    except Exception:
        h1 = False
        
    try:
        M = P + Q - P * Q
        diff_q = M * M - M
        neg_q = not is_zero_mat(diff_q)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q commute",
    "¬Q: P + Q - PQ is not a projection matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1