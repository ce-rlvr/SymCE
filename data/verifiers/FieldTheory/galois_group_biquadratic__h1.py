import sympy
from sympy import fraction, factor_list, Expr

# Top-level setup: named object bindings that the witness expression may reference.
u, v = sympy.symbols('u v')

def is_in_F(expr, p):
    """Check if expr is a valid element of the rational function field over GF(p)."""
    try:
        if not isinstance(expr, Expr) and not isinstance(expr, int):
            return False
        expr = sympy.sympify(expr)
        num, den = fraction(sympy.cancel(expr))
        
        if den.is_Number:
            if int(den) % p == 0:
                return False
        else:
            coeff, factors = factor_list(den, modulus=p)
            if int(coeff) % p == 0:
                return False
        return True
    except Exception:
        return False

def is_square_in_F(expr, p):
    """Check if expr is a square in the rational function field over GF(p)."""
    try:
        expr = sympy.sympify(expr)
        num, den = fraction(sympy.cancel(expr))
        
        # Denominator must not be 0 mod p
        if den.is_Number:
            if int(den) % p == 0:
                return False
        else:
            coeff, factors = factor_list(den, modulus=p)
            if int(coeff) % p == 0:
                return False
                
        # f/g is a square iff f*g is a square
        poly_expr = num * den
        
        if poly_expr.is_Number:
            val = int(poly_expr) % p
            if val == 0:
                return True
            if p == 2:
                return True
            return pow(val, (p - 1) // 2, p) in (0, 1)
            
        coeff, factors = factor_list(poly_expr, modulus=p)
        val = int(coeff) % p
        if val == 0:
            return True
        if p != 2:
            if pow(val, (p - 1) // 2, p) not in (0, 1):
                return False
        for f, m in factors:
            if m % 2 != 0:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        p = witness[0]
        a = witness[1]
        b = witness[2]
    except Exception:
        return [False] * 6

    try:
        h1 = bool(sympy.isprime(p) and is_in_F(a, p) and is_in_F(b, p))
    except Exception:
        h1 = False

    try:
        h2 = not is_square_in_F(a, p)
    except Exception:
        h2 = False

    try:
        h3 = not is_square_in_F(b, p)
    except Exception:
        h3 = False

    try:
        h4 = not is_square_in_F(a * b, p)
    except Exception:
        h4 = False

    # K is defined as the splitting field of (x^2 - a)(x^2 - b) over F.
    # This hypothesis establishes the context for the conclusion.
    h5 = True

    try:
        # The conclusion states K/F is Galois with degree 4 and Gal = V4.
        # If p == 2, the polynomial is inseparable, so the extension is purely inseparable
        # and thus NOT Galois (and degree may be 2 or 4, but Gal is trivial).
        # If p != 2, Kummer theory guarantees the conclusion holds.
        # Therefore, the conclusion fails (neg_Q is True) if and only if p == 2.
        neg_q = bool(p == 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of F",
    "H_2: There is no element x in F such that x^2 = a",
    "H_3: There is no element y in F such that y^2 = b",
    "H_4: There is no element z in F such that z^2 = ab",
    "H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: K/F is not Galois with degree 4 and Gal = V4"
]

N_HYP = 5
NEG_Q_INDEX = 5