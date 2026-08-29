import sympy
from sympy import Poly
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    try:
        f = Poly(witness, x, y)
        if not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        h1_ok = f.domain.is_Field
    except Exception:
        h1_ok = False

    try:
        f = Poly(witness, x, y)
        if not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        if f.is_zero:
            n = -1
        else:
            n = max(sum(monom) for monom in f.monoms())
        h2_ok = n >= 1
    except Exception:
        h2_ok = False

    try:
        f = Poly(witness, x, y)
        if not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        if f.is_zero:
            h3_ok = False
        else:
            n = max(sum(monom) for monom in f.monoms())
            fn_expr = 0
            for monom, coeff in zip(f.monoms(), f.coeffs()):
                if sum(monom) == n:
                    fn_expr += coeff * (x**monom[0]) * (y**monom[1])
            fn_poly = Poly(fn_expr, x, y, domain=f.domain)
            h3_ok = fn_poly.is_irreducible
    except Exception:
        h3_ok = False

    try:
        f = Poly(witness, x, y)
        if not f.domain.is_Field:
            f = f.set_domain(f.domain.get_field())
        neg_q_ok = not f.is_irreducible
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial of degree n >= 1",
    "H_3: f_n is irreducible",
    "¬Q: f is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3