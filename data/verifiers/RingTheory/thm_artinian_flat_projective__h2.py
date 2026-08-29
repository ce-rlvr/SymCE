import sympy
import math

x = sympy.Symbol('x')

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, m = witness
            
            if isinstance(n, (int, sympy.Integer)) and isinstance(m, (int, sympy.Integer)):
                n_int, m_int = int(n), int(m)
                if n_int >= 2 and m_int >= 1 and n_int % m_int == 0:
                    h1_ok = True
                    neg_q_ok = math.gcd(m_int, n_int // m_int) != 1
                    
            elif isinstance(n, sympy.Expr) and isinstance(m, sympy.Expr):
                poly_n = sympy.Poly(n)
                poly_m = sympy.Poly(m)
                if poly_n.degree() >= 1 and poly_m.degree() >= 0:
                    gen = poly_n.gens[0]
                    rem = sympy.rem(n, m, gen)
                    if rem == 0:
                        h1_ok = True
                        quot = sympy.quo(n, m, gen)
                        gcd_poly = sympy.gcd(m, quot, gen)
                        neg_q_ok = sympy.Poly(gcd_poly, gen).degree() > 0
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring (and M is a right R-module)",
    "¬Q: M is not a projective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1