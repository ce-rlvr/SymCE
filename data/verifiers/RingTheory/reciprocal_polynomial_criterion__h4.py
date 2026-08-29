import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial of degree at least 1",
    "H_3: The constant term a_0 is non-zero",
    "not Q: f is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    try:
        p = sympy.Poly(witness, x)
        p_field = p.set_domain(p.domain.get_field())
        h1 = bool(p_field.domain.is_Field)
    except Exception:
        h1 = False

    # H_2: f is a polynomial of degree at least 1
    try:
        p = sympy.Poly(witness, x)
        h2 = bool(p.degree() >= 1)
    except Exception:
        h2 = False

    # H_3: The constant term a_0 is non-zero
    try:
        p = sympy.Poly(witness, x)
        h3 = bool(p.nth(0) != 0)
    except Exception:
        h3 = False

    # ¬Q: f is reducible
    try:
        p = sympy.Poly(witness, x)
        p_field = p.set_domain(p.domain.get_field())
        neg_q = not bool(p_field.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]