import sympy as sp
import math

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, p, q) where:
      - f is either a list of integers [a_0, a_1, ..., a_n] representing sum(a_i * x^i)
        or a sympy expression representing a polynomial with integer coefficients.
      - p and q are integers.
    """
    try:
        f, p, q = witness
    except Exception:
        return [False, False, False]
        
    if not (isinstance(p, int) and isinstance(q, int)):
        return [False, False, False]
        
    try:
        if isinstance(f, list):
            if not all(isinstance(c, int) for c in f):
                h1 = False
            elif len(f) == 0:
                h1 = False
            else:
                f_stripped = f.copy()
                while len(f_stripped) > 1 and f_stripped[-1] == 0:
                    f_stripped.pop()
                h1 = True
                a_0 = f_stripped[0]
                a_n = f_stripped[-1]
                n = len(f_stripped) - 1
                f = f_stripped
        else:
            f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
            free = f_expr.free_symbols
            if len(free) > 1:
                h1 = False
            else:
                var = list(free)[0] if free else x
                poly = sp.Poly(f_expr, var)
                if not poly.domain.is_ZZ:
                    h1 = False
                else:
                    h1 = True
                coeffs = poly.all_coeffs()
                a_n = int(coeffs[0])
                a_0 = int(coeffs[-1])
    except Exception:
        return [False, False, False]
        
    try:
        if q == 0:
            h2 = False
        else:
            coprime = math.gcd(p, q) == 1
            if isinstance(f, list):
                val = sum(c * (p**i) * (q**(n - i)) for i, c in enumerate(f))
                is_root = (val == 0)
            else:
                var = list(free)[0] if free else x
                is_root = (f_expr.subs(var, sp.Rational(p, q)) == 0)
            h2 = coprime and is_root
    except Exception:
        h2 = False
        
    try:
        try:
            p_divides = (a_0 % p == 0)
        except ZeroDivisionError:
            p_divides = (a_0 == 0)
            
        try:
            q_divides = (a_n % q == 0)
        except ZeroDivisionError:
            q_divides = (a_n == 0)
            
        neg_q = not (p_divides and q_divides)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial with integer coefficients",
    "H_2: p/q is a rational root of f such that p and q are coprime",
    "neg_Q: p does not divide a_0 or q does not divide a_n"
]

N_HYP = 2
NEG_Q_INDEX = 2