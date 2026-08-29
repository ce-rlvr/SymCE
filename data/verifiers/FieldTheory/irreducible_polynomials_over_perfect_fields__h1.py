import sympy
from sympy import Poly, symbols
from sympy.polys.domains import ZZ, QQ, GF

t, x, y, z = symbols('t x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            expr, gen, domain = witness
            p = Poly(expr, gen, domain=domain)
        elif isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness)
    except Exception:
        p = None

    try:
        h1_ok = p is not None and len(p.gens) == 1 and p.domain.is_Field
    except Exception:
        h1_ok = False

    try:
        h2_ok = p is not None and p.is_irreducible == True
    except Exception:
        h2_ok = False

    try:
        if p is not None:
            deriv = p.diff()
            g = p.gcd(deriv)
            neg_q_ok = g.degree() > 0
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: p is a polynomial over F",
    "H_2: p is irreducible over F",
    "¬Q: p is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2