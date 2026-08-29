import sympy
from sympy.abc import x
from sympy import QQ, ZZ, RR, CC

def conditions(witness) -> list[bool]:
    # Extract phi from witness if it's a tuple (e.g., (F, phi))
    try:
        if isinstance(witness, tuple):
            phi = witness[-1]
        else:
            phi = witness
    except Exception:
        phi = witness

    # H_1: F is a field
    # We interpret this as phi(x) being a valid polynomial in F[x]
    # where F is a field of numbers (e.g., rationals, reals).
    try:
        poly = sympy.Poly(phi, x)
        h1_ok = all(c.is_number for c in poly.coeffs())
    except Exception:
        h1_ok = False

    # ¬Q: phi(x) is NOT of the form ax + b with a != 0
    # This means the degree of the polynomial is not exactly 1.
    try:
        poly = sympy.Poly(phi, x)
        neg_q_ok = poly.degree() != 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: phi(x) is not of the form ax + b with a != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1