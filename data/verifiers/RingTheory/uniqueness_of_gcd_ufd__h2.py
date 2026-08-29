import sympy
from sympy import ZZ, QQ, Poly, Symbol
from sympy.abc import x, y, z

# Top-level setup
# (No specific named bindings required for this ring theory conjecture, 
# but we provide standard rings just in case)

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: d_1 is a greatest common divisor of a and b",
    "H_3: d_2 is a greatest common divisor of a and b",
    "¬Q: There does not exist a unit u in R such that d_1 = u d_2"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 5:
            R, a, b, d1, d2 = witness
        else:
            R = witness.R
            a = witness.a
            b = witness.b
            d1 = witness.d1
            d2 = witness.d2
    except Exception:
        return [False, False, False, False]

    def eq(R, u, v):
        if hasattr(R, 'eq'): 
            return R.eq(u, v)
        if u == v: 
            return True
        try:
            return sympy.simplify(u - v) == 0
        except Exception:
            return False

    def mul(R, u, v):
        if hasattr(R, 'mul'): 
            return R.mul(u, v)
        return u * v

    def zero(R):
        if hasattr(R, 'zero'):
            val = R.zero
            return val() if callable(val) else val
        return 0

    def one(R):
        if hasattr(R, 'one'):
            val = R.one
            return val() if callable(val) else val
        return 1

    def divides(R, divisor, dividend):
        if hasattr(R, 'divides'):
            return R.divides(divisor, dividend)
        if hasattr(R, 'elements'):
            for k in R.elements:
                if eq(R, mul(R, divisor, k), dividend):
                    return True
            return False
        if hasattr(R, 'exquo'):
            if eq(R, divisor, zero(R)):
                return eq(R, dividend, zero(R))
            try:
                R.exquo(dividend, divisor)
                return True
            except Exception:
                return False
        if divisor == 0:
            return dividend == 0
        try:
            if isinstance(divisor, (int, sympy.Integer)) and isinstance(dividend, (int, sympy.Integer)):
                return dividend % divisor == 0
        except Exception:
            pass
        try:
            q = sympy.cancel(dividend / divisor)
            if q.as_numer_denom()[1] == 1:
                return True
        except Exception:
            pass
        return False

    def is_gcd(R, a, b, d):
        if not (divides(R, d, a) and divides(R, d, b)):
            return False
        if hasattr(R, 'is_gcd'):
            return R.is_gcd(a, b, d)
        if hasattr(R, 'elements'):
            for c in R.elements:
                if divides(R, c, a) and divides(R, c, b):
                    if not divides(R, c, d):
                        return False
            return True
        if hasattr(R, 'gcd'):
            g = R.gcd(a, b)
            return divides(R, d, g) and divides(R, g, d)
        try:
            g = sympy.gcd(a, b)
            return divides(R, d, g) and divides(R, g, d)
        except Exception:
            return False

    def is_unit(R, u):
        if hasattr(R, 'is_unit'):
            val = R.is_unit
            if callable(val): return val(u)
        if hasattr(R, 'units'):
            for v in R.units:
                if eq(R, u, v):
                    return True
            return False
        if hasattr(R, 'elements'):
            for v in R.elements:
                if eq(R, mul(R, u, v), one(R)):
                    return True
            return False
        if hasattr(R, 'revert'):
            try:
                inv = R.revert(u)
                return eq(R, mul(R, u, inv), one(R))
            except Exception:
                return False
        return divides(R, u, one(R))

    # H1: R is a UFD
    try:
        if hasattr(R, 'is_UFD'):
            val = R.is_UFD
            h1 = val() if callable(val) else bool(val)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: d1 is a gcd of a and b
    try:
        h2 = bool(is_gcd(R, a, b, d1))
    except Exception:
        h2 = False

    # H3: d2 is a gcd of a and b
    try:
        h3 = bool(is_gcd(R, a, b, d2))
    except Exception:
        h3 = False

    # Negated Conclusion: There does NOT exist a unit u in R such that d1 = u * d2
    try:
        neg_q = True
        if hasattr(R, 'units'):
            for u in R.units:
                if eq(R, d1, mul(R, u, d2)):
                    neg_q = False
                    break
        elif hasattr(R, 'elements'):
            for u in R.elements:
                if is_unit(R, u):
                    if eq(R, d1, mul(R, u, d2)):
                        neg_q = False
                        break
        else:
            if eq(R, d2, zero(R)):
                neg_q = not eq(R, d1, zero(R))
            elif divides(R, d2, d1):
                if hasattr(R, 'exquo'):
                    try:
                        u = R.exquo(d1, d2)
                        if is_unit(R, u):
                            neg_q = False
                    except Exception:
                        pass
                else:
                    try:
                        u = sympy.cancel(d1 / d2)
                        if is_unit(R, u):
                            neg_q = False
                    except Exception:
                        pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]