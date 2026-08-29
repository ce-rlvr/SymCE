import sympy
from sympy import Symbol, Poly, QQ, ZZ, GF, RR, CC, Rational, Integer

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Check the remaining hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (F, f), where F is a sympy domain (e.g., QQ)
    and f is a polynomial or an expression in x.
    """
    # H_1: F is a field
    try:
        F, f = witness
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # ¬Q: There does NOT exist a splitting field for f(x) over F.
    # A splitting field exists for any non-zero polynomial (even constants, where the field itself is the splitting field).
    # The only polynomial that does not have a splitting field is the zero polynomial, 
    # because it cannot be factored into a product of linear factors.
    try:
        F, f = witness
        if isinstance(f, Poly):
            neg_q = bool(f.is_zero)
        else:
            poly_f = Poly(f, x)
            neg_q = bool(poly_f.is_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: f(x) does not have a splitting field over F"
]

N_HYP = 1
NEG_Q_INDEX = 1