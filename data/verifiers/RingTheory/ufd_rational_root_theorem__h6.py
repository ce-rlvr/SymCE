import sympy
from sympy import Symbol, Poly, gcd, sympify

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) < 3:
            return [False] * 6
        
        f, p, q = witness[0], witness[1], witness[2]
        
        # H_1: R is a unique factorization domain
        h1 = True
        
        # H_2: F is the field of fractions of R
        h2 = True
        
        # H_3: f(x) is a polynomial over R
        try:
            f_sym = sympify(f)
            poly_f = Poly(f_sym, x)
            h3 = all(bool(sympify(c).is_integer) for c in poly_f.coeffs())
        except Exception:
            h3 = False
            
        # H_4: p and q are elements of R
        try:
            p_sym = sympify(p)
            q_sym = sympify(q)
            h4 = bool(p_sym.is_integer) and bool(q_sym.is_integer)
        except Exception:
            h4 = False
            
        # H_5: p and q are coprime in R
        try:
            h5 = h4 and (gcd(p_sym, q_sym) in [1, -1])
        except Exception:
            h5 = False
            
        # ~Q: p does not divide a_0 or q does not divide a_n
        try:
            f_sym = sympify(f)
            poly_f = Poly(f_sym, x)
            coeffs = poly_f.all_coeffs()
            a_n = sympify(coeffs[0])
            a_0 = sympify(coeffs[-1])
            
            p_divides_a0 = (a_0 % p_sym == 0) if p_sym != 0 else (a_0 == 0)
            q_divides_an = (a_n % q_sym == 0) if q_sym != 0 else (a_n == 0)
            
            neg_q = not (p_divides_a0 and q_divides_an)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, h5, neg_q]
    except Exception:
        return [False] * 6

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: F is the field of fractions of R",
    "H_3: f(x) is a polynomial over R",
    "H_4: p and q are elements of R",
    "H_5: p and q are coprime in R",
    "neg_Q: p does not divide a_0 or q does not divide a_n"
]

N_HYP = 5
NEG_Q_INDEX = 5