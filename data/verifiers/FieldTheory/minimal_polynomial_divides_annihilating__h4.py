import sympy
from sympy import Poly, minpoly
from sympy.abc import x

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "Minimal Polynomial Divides Annihilating Polynomial" (with annihilating hypothesis dropped).
    
    Expected witness:
      A dictionary {'alpha': element, 'm': polynomial, 'g': polynomial, 'x': symbol}
      or a tuple (alpha, m, g) or (alpha, m, g, x).
    """
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            m = witness.get('m')
            g = witness.get('g')
            sym_x = witness.get('x', x)
        else:
            alpha = witness[0]
            m = witness[1]
            g = witness[2]
            sym_x = witness[3] if len(witness) > 3 else x
    except Exception:
        return [False, False, False, False]

    # H_1: E is a field extension of F
    # In our SymPy model, F is QQ and any valid SymPy expression alpha 
    # belongs to some field extension E (e.g., CC or QQ(alpha)).
    try:
        h1_ok = alpha is not None
    except Exception:
        h1_ok = False

    # H_2: alpha is an element of E that is algebraic over F
    try:
        mp = minpoly(alpha, sym_x)
        h2_ok = True
    except Exception:
        h2_ok = False

    # H_3: m(x) is the minimal polynomial of alpha over F
    try:
        m_poly = Poly(m, sym_x, domain='QQ')
        mp_poly = Poly(mp, sym_x, domain='QQ')
        # Compare monic versions to avoid scalar multiple mismatches
        h3_ok = (m_poly.monic() == mp_poly.monic())
    except Exception:
        h3_ok = False

    # ¬Q: m(x) does not divide g(x)
    try:
        g_poly = Poly(g, sym_x, domain='QQ')
        m_poly = Poly(m, sym_x, domain='QQ')
        r_poly = g_poly % m_poly
        neg_q_ok = not r_poly.is_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E is a field extension of F",
    "H_2: alpha is an element of E that is algebraic over F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "¬Q: m(x) does not divide g(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3