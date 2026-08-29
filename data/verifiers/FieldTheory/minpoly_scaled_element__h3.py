import sympy as sp
from sympy import Poly, Rational

x = sp.Symbol('x')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (m_expr, c) where:
      - m_expr is a sympy expression representing the minimal polynomial m(x) of alpha over Q.
      - c is the scalar (a rational number).
    """
    try:
        m_expr, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: m(x) is a monic irreducible polynomial over Q of degree >= 1
    try:
        m_poly = Poly(m_expr, x, domain='QQ')
        deg = m_poly.degree()
        is_monic = m_poly.LC() == 1
        is_irred = m_poly.is_irreducible
        h1 = bool(deg >= 1 and is_monic and is_irred)
    except Exception:
        h1 = False
        
    # H_2: c is a rational number
    try:
        c_rat = Rational(c)
        h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of c*alpha over Q is NOT given by c^n * m(x/c)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # Determine the actual minimal polynomial of c*alpha over Q
            if c_rat == 0:
                # If c = 0, c*alpha = 0, whose minimal polynomial is simply x
                actual_min_poly = Poly(x, x, domain='QQ')
            else:
                # If c != 0, the minimal polynomial is indeed c^n * m(x/c)
                coeffs = m_poly.all_coeffs()
                new_coeffs = [coeffs[i] * (c_rat**i) for i in range(deg + 1)]
                actual_min_poly = Poly(new_coeffs, x, domain='QQ')
                
            # Compute the polynomial given by the formula in the conclusion: c^n * m(x/c)
            coeffs = m_poly.all_coeffs()
            formula_coeffs = [coeffs[i] * (c_rat**i) for i in range(deg + 1)]
            formula_poly = Poly(formula_coeffs, x, domain='QQ')
            
            # The conclusion fails if the actual minimal polynomial does not match the formula
            neg_q = bool(actual_min_poly != formula_poly)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m(x) is a monic irreducible polynomial over Q of degree >= 1",
    "H_2: c is a rational number",
    "¬Q: The minimal polynomial of c*alpha over Q is NOT c^n m(x/c)"
]

N_HYP = 2
NEG_Q_INDEX = 2