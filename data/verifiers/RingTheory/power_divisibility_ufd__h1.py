import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: n is a positive integer",
    "H_3: a^n divides b^n in R",
    "¬Q: a does not divide b in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    We expect the witness to be a tuple: (a, b, n, q, alpha)
    where R = Z[alpha], and q is the quotient such that a^n * q = b^n.
    For example, alpha = sympy.sqrt(-3).
    """
    try:
        if len(witness) == 5:
            a, b, n, q, alpha = witness
        elif len(witness) == 4:
            a, b, n, q = witness
            alpha = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def in_Z_alpha(expr, alpha):
        try:
            expr = sympy.sympify(expr)
            expr = sympy.radsimp(expr)
            expr = sympy.simplify(sympy.expand(expr))
            if expr == 0:
                return True
            if expr.is_Rational:
                return expr.is_Integer
            if alpha is None:
                return False
            p = sympy.Poly(expr, alpha)
            for c in p.coeffs():
                if not (isinstance(c, sympy.Integer) or (hasattr(c, 'is_Integer') and c.is_Integer)):
                    return False
            return True
        except Exception:
            return False

    try:
        h1 = in_Z_alpha(a, alpha) and in_Z_alpha(b, alpha)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    try:
        if in_Z_alpha(q, alpha):
            diff = sympy.simplify(sympy.expand(a**n * q - b**n))
            h3 = (diff == 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        quotient = sympy.radsimp(b / a)
        quotient = sympy.simplify(sympy.expand(quotient))
        neg_q = not in_Z_alpha(quotient, alpha)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]