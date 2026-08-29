import sympy
from sympy.abc import x, y, z, t, u, v

def conditions(witness) -> list[bool]:
    try:
        a, b, third = witness
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(third, (list, tuple)):
            coeffs = list(third)
        else:
            expr = sympy.sympify(third)
            free = expr.free_symbols
            if len(free) == 1:
                sym = list(free)[0]
                poly = sympy.Poly(expr, sym)
                coeffs = poly.all_coeffs()
                coeffs.reverse()
            elif len(free) == 0:
                coeffs = [expr]
            else:
                coeffs = None
    except Exception:
        coeffs = None

    try:
        if coeffs is None or len(coeffs) == 0:
            h1 = False
        else:
            def is_exact(expr):
                if isinstance(expr, (int, sympy.Integer, sympy.Rational)):
                    return True
                if isinstance(expr, float):
                    return False
                if isinstance(expr, sympy.Expr):
                    return not expr.has(sympy.Float)
                return False

            h1 = is_exact(a) and is_exact(b) and all(is_exact(c) for c in coeffs)
    except Exception:
        h1 = False

    try:
        h2 = h1 and b != 0
    except Exception:
        h2 = False

    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            x_val = sympy.Rational(a, b)
        else:
            x_val = a / b
            
        val = sum(c * (x_val**i) for i, c in enumerate(coeffs))
        h3 = sympy.simplify(val) == 0
    except Exception:
        h3 = False

    try:
        coeffs_stripped = list(coeffs)
        while len(coeffs_stripped) > 1 and coeffs_stripped[-1] == 0:
            coeffs_stripped.pop()
            
        c_0 = coeffs_stripped[0]
        c_n = coeffs_stripped[-1]
        
        has_rationals = False
        for elem in [a, b] + coeffs_stripped:
            if isinstance(elem, sympy.Rational) and not isinstance(elem, sympy.Integer):
                has_rationals = True
            elif isinstance(elem, sympy.Expr):
                if any(isinstance(n, sympy.Rational) and not isinstance(n, sympy.Integer) for n in elem.atoms(sympy.Number)):
                    has_rationals = True

        def divides(divisor, dividend):
            if divisor == 0:
                return dividend == 0
            
            res = sympy.cancel(dividend / divisor)
            
            if res.is_number:
                if has_rationals:
                    return True
                else:
                    return sympy.fraction(res)[1] in (1, -1)
            
            num, den = sympy.fraction(res)
            if not den.free_symbols:
                if has_rationals:
                    return True
                else:
                    return den in (1, -1)
            else:
                return False
                
        a_divides_c0 = divides(a, c_0)
        b_divides_cn = divides(b, c_n)
        
        neg_q = not (a_divides_c0 and b_divides_cn)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the field of fractions of R",
    "H_3: x = a/b is a root of the polynomial f(x)",
    "not_Q: The element a does not divide c_0 in R, or b does not divide c_n in R"
]

N_HYP = 3
NEG_Q_INDEX = 3