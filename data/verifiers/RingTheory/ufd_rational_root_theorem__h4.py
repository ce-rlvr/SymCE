import sympy as sp
from sympy import Poly

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, p, q = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        f_sym = sp.sympify(f)
        p_sym = sp.sympify(p)
        q_sym = sp.sympify(q)
        
        free_syms = f_sym.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = x
        else:
            var = x
            
        poly_f = Poly(f_sym, var)
        coeffs = poly_f.all_coeffs()
        
        is_ZZ = all(c.is_Integer for c in coeffs) and p_sym.is_Integer and q_sym.is_Integer
        h1 = bool(is_ZZ)
    except Exception:
        h1 = False

    h2 = h1

    try:
        h3 = bool(h1 and poly_f.degree() >= 1)
    except Exception:
        h3 = False

    try:
        if q_sym == 0:
            h4 = False
        else:
            val = f_sym.subs(var, sp.Rational(p_sym, q_sym))
            h4 = bool(val == 0)
    except Exception:
        h4 = False

    try:
        a_n = poly_f.LC()
        a_0 = poly_f.nth(0)
        
        if q_sym == 0:
            divides_an = False
        else:
            divides_an = (a_n % q_sym == 0)
            
        if p_sym == 0:
            divides_a0 = (a_0 == 0)
        else:
            divides_a0 = (a_0 % p_sym == 0)
            
        neg_q = not (divides_an and divides_a0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the fraction field of R",
    "H_3: f(x) is a polynomial over R of degree n >= 1",
    "H_4: The element p/q in K is a root of f(x)",
    "¬Q: q does not divide a_n or p does not divide a_0 in R"
]

N_HYP = 4
NEG_Q_INDEX = 4