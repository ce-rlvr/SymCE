import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            alpha, m = witness
        else:
            alpha = witness
            m = sympy.minpoly(alpha, x)
            
        expected_m = sympy.minpoly(alpha, x)
        m_poly = Poly(m, x, domain='QQ')
        expected_poly = Poly(expected_m, x, domain='QQ')
        
        if m_poly.degree() != expected_poly.degree():
            h1 = False
        else:
            h1 = bool(m_poly.monic() == expected_poly.monic())
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            alpha, m = witness
        else:
            alpha = witness
            m = sympy.minpoly(alpha, x)
            
        m_poly = Poly(m, x)
        deg = m_poly.degree()
        
        if deg in (sympy.oo, -sympy.oo) or deg <= 0:
            neg_q = True
        else:
            deg_int = int(deg)
            is_power_of_2 = (deg_int & (deg_int - 1)) == 0
            neg_q = not is_power_of_2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m(x) is the minimal polynomial of alpha over Q",
    "¬Q: The degree of m(x) is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1