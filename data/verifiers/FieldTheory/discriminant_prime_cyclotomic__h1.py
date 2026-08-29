import sympy

x = sympy.Symbol('x')

def conditions(witness):
    try:
        p = int(witness)
        h1 = (p >= 1 and p == witness)
    except Exception:
        h1 = False

    try:
        p_val = int(witness)
        poly = sympy.cyclotomic_poly(p_val, x)
        
        # The ring of integers of Q(zeta_p) is Z[zeta_p].
        # Thus, the discriminant of the field Q(zeta_p) over Q is exactly 
        # the discriminant of the minimal polynomial of zeta_p, 
        # which is the p-th cyclotomic polynomial.
        actual_disc = sympy.discriminant(poly, x)
        
        p_sym = sympy.Integer(p_val)
        formula_disc = ((-1)**sympy.Rational(p_val - 1, 2)) * (p_sym**(p_val - 2))
        
        neg_q = bool(sympy.simplify(actual_disc - formula_disc) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_p is a primitive p-th root of unity",
    "¬Q: The discriminant of Q(zeta_p) over Q is not (-1)^{(p-1)/2} p^{p-2}"
]

N_HYP = 1
NEG_Q_INDEX = 1