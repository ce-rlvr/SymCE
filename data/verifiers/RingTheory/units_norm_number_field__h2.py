import sympy as sp
from sympy import I, Rational, Integer, sqrt

x = sp.Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - Let K be an algebraic number field.
      - Let N_{K/Q} denote the absolute field norm from K to the rational numbers Q.
      - Let alpha be an element of O_K.
    Conclusion:
      - The element alpha is a unit in O_K if and only if N_{K/Q}(alpha) = 1 or N_{K/Q}(alpha) = -1.
    """
    alpha = witness
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        alpha = witness[1]

    x_dummy = sp.Dummy('x')

    def check_H1():
        try:
            sp.minpoly(alpha, x_dummy)
            return True
        except Exception:
            return False

    def check_H2():
        return check_H1()

    def check_H3():
        try:
            p = sp.minpoly(alpha, x_dummy, polys=True)
            return all(c.is_integer for c in p.all_coeffs())
        except Exception:
            return False

    def check_neg_Q():
        try:
            p = sp.minpoly(alpha, x_dummy, polys=True)
            a0 = p.all_coeffs()[-1]
            norm_pm1 = (abs(a0) == 1)
            
            in_O_K = all(c.is_integer for c in p.all_coeffs())
            if not in_O_K:
                is_unit = False
            else:
                if alpha == 0:
                    is_unit = False
                else:
                    p_inv = sp.minpoly(1/alpha, x_dummy, polys=True)
                    is_unit = all(c.is_integer for c in p_inv.all_coeffs())
            
            conclusion = (is_unit == norm_pm1)
            return not conclusion
        except Exception:
            return False

    return [
        bool(check_H1()),
        bool(check_H2()),
        bool(check_H3()),
        bool(check_neg_Q())
    ]

CONDITION_LABELS = [
    "H_1: K is an algebraic number field",
    "H_2: N_{K/Q} denotes the absolute field norm",
    "H_3: alpha is an element of O_K",
    "¬Q: alpha is a unit in O_K iff N_{K/Q}(alpha) = 1 or -1 fails"
]

N_HYP = 3
NEG_Q_INDEX = 3