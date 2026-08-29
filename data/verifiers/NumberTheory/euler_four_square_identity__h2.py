import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(expr):
    if expr == 0:
        return True
    if getattr(expr, 'is_zero_matrix', False):
        return True
    try:
        expanded = expr.expand()
        if expanded == 0:
            return True
        if getattr(expanded, 'is_zero_matrix', False):
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        x1, x2, x3, x4, y1, y2, y3, y4 = witness
    except Exception:
        return [False, False]

    h1_ok = True
    try:
        xs = [x1, x2, x3, x4]
        for i in range(4):
            for j in range(4):
                if not is_zero(xs[i] * xs[j] - xs[j] * xs[i]):
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        lhs = (x1**2 + x2**2 + x3**2 + x4**2) * (y1**2 + y2**2 + y3**2 + y4**2)
        rhs = (x1*y1 - x2*y2 - x3*y3 - x4*y4)**2 + \
              (x1*y2 + x2*y1 + x3*y4 - x4*y3)**2 + \
              (x1*y3 - x2*y4 + x3*y1 + x4*y2)**2 + \
              (x1*y4 + x2*y3 - x3*y2 + x4*y1)**2
        
        if not is_zero(lhs - rhs):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: x_1, x_2, x_3, x_4 are elements of a commutative ring",
    "¬Q: Euler's Four-Square Identity fails"
]

N_HYP = 1
NEG_Q_INDEX = 1