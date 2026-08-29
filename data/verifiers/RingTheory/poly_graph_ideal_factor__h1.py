import sympy as sp
from sympy import Symbol, Matrix, eye, zeros

# Top-level setup
x = Symbol('x')
y = Symbol('y')

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_poly_in_x(expr, x, y):
    try:
        if hasattr(expr, 'has') and expr.has(y):
            return False
    except Exception:
        pass

    if isinstance(expr, sp.MatrixBase):
        for i in range(expr.rows):
            for j in range(expr.cols):
                if not is_poly_in_x(expr[i, j], x, y):
                    return False
        return True
    else:
        if isinstance(expr, str):
            return False
        if not hasattr(expr, 'has') or not expr.has(x):
            return True
        try:
            if expr.is_polynomial(x):
                return True
        except Exception:
            pass
        try:
            d = expr
            for _ in range(20):
                d = sp.diff(d, x)
                if d == 0:
                    return True
            return False
        except Exception:
            return False

def conditions(witness):
    R = None
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R, f = witness
        elif len(witness) > 0:
            f = witness[0]
        else:
            return [False, False]
    else:
        f = witness

    # H_1: f(x) is a polynomial in x
    try:
        h1 = is_poly_in_x(f, x, y)
    except Exception:
        h1 = False

    # neg_Q: The factor ring modulo y - f(x) is not isomorphic to the polynomial ring
    # This occurs when f(x) is not in the center of the ring.
    try:
        neg_q = False
        if R is not None and isinstance(R, (list, tuple)):
            for r in R:
                diff = f * r - r * f
                if isinstance(diff, sp.MatrixBase):
                    diff = sp.simplify(diff)
                    if not diff.is_zero_matrix:
                        neg_q = True
                        break
                else:
                    if sp.simplify(diff) != 0:
                        neg_q = True
                        break
        elif isinstance(f, sp.MatrixBase):
            if f.rows != f.cols:
                neg_q = True
            else:
                for i in range(f.rows):
                    for j in range(f.cols):
                        if i == j:
                            diff = sp.simplify(f[i, j] - f[0, 0])
                            if diff != 0:
                                neg_q = True
                        else:
                            diff = sp.simplify(f[i, j])
                            if diff != 0:
                                neg_q = True
                if not neg_q:
                    if hasattr(f[0, 0], 'is_commutative') and f[0, 0].is_commutative is False:
                        neg_q = True
        else:
            if hasattr(f, 'is_commutative') and f.is_commutative is False:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial in x",
    "¬Q: The factor ring modulo y - f(x) is not isomorphic to the polynomial ring"
]

N_HYP = 1
NEG_Q_INDEX = 1