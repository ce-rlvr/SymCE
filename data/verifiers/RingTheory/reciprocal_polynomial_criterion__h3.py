import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    f = None
    try:
        f = Poly(witness, x)
        if not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        h1 = f.domain.is_Field
    except Exception:
        h1 = False

    try:
        h2 = (f.degree() >= 1) if f is not None else False
    except Exception:
        h2 = False

    try:
        if f is not None:
            coeffs = f.all_coeffs()
            f_star = Poly.from_list(coeffs[::-1], x, domain=f.domain)
            h3 = (f_star.is_irreducible is True)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if f is not None:
            neg_q = (f.is_irreducible is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F of degree at least 1",
    "H_3: reciprocal polynomial is irreducible over F",
    "not Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3