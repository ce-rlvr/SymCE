import sympy
from sympy import Poly, QQ, ZZ
from sympy.abc import x, y, z

def parse_witness(witness):
    if isinstance(witness, Poly):
        return witness
    if isinstance(witness, tuple) and len(witness) == 2:
        dom, expr = witness
        return Poly(expr, domain=dom)
    try:
        p = Poly(witness)
        # Default to QQ if ZZ is inferred, to satisfy the field hypothesis
        if p.domain == ZZ:
            return Poly(witness, domain=QQ)
        return p
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        f = parse_witness(witness)
    except Exception:
        f = None

    # H1: F is a field
    try:
        h1 = False
        if f is not None:
            h1 = bool(f.domain.is_Field)
    except Exception:
        h1 = False

    # H2: f is a polynomial over F
    try:
        h2 = False
        if f is not None:
            h2 = isinstance(f, Poly) and len(f.gens) == 1
    except Exception:
        h2 = False

    # H3: f has no roots in F
    try:
        h3 = False
        if f is not None:
            h3 = len(f.ground_roots()) == 0
    except Exception:
        h3 = False

    # neg_Q: f is irreducible over F -> FAILS -> f is reducible
    try:
        neg_q = False
        if f is not None:
            neg_q = (f.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a univariate polynomial over F",
    "H_3: f has no roots in F",
    "¬Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3