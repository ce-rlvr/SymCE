import sympy as sp
import math
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial with integer coefficients",
    "H_2: N(m) is the number of solutions to f(x) ≡ 0 (mod m)",
    "H_3: gcd(m1, m2) = 1",
    "¬Q: N(m1*m2) != N(m1)*N(m2)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        f, m1, m2 = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: f(x) is a polynomial with integer coefficients
    try:
        expr = sp.sympify(f)
        poly = sp.Poly(expr)
        # Ensure it's a polynomial in symbols, not functions like sin(x)
        if not all(isinstance(g, sp.Symbol) for g in poly.gens):
            h1 = False
        else:
            h1 = all(c.is_integer for c in poly.coeffs())
    except Exception:
        h1 = False

    # H_2: N(m) is the number of solutions to f(x) ≡ 0 (mod m)
    # This is a definitional hypothesis; we verify the witness provides valid types.
    try:
        h2 = isinstance(m1, int) and isinstance(m2, int) and expr is not None
    except Exception:
        h2 = False

    # H_3: gcd(m1, m2) = 1
    try:
        h3 = math.gcd(m1, m2) == 1
    except Exception:
        h3 = False

    # ¬Q: N(m1*m2) != N(m1)*N(m2)
    # N(m) is defined as the number of solutions in {0, 1, ..., m-1}.
    # For m <= 0, range(m) is empty, yielding 0 solutions.
    def N(m):
        free = list(expr.free_symbols)
        var = free[0] if free else sp.Symbol('x')
        count = 0
        for i in range(m):
            if expr.subs(var, i) % m == 0:
                count += 1
        return count

    try:
        n_m1 = N(m1)
        n_m2 = N(m2)
        n_m1m2 = N(m1 * m2)
        neg_q = n_m1m2 != n_m1 * n_m2
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]