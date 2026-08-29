import sympy
from sympy import Poly, Symbol

# Top-level setup
# No specific named objects required for this domain

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: The content of f is 1",
    "H_3: f is irreducible",
    "¬Q: The factor ring is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            R, expr = witness
            if isinstance(expr, Poly):
                f = expr
            else:
                free = expr.free_symbols
                gen = list(free)[0] if free else Symbol('x')
                f = Poly(expr, gen, domain=R)
        elif isinstance(witness, Poly):
            R = witness.domain
            f = witness
        else:
            f = Poly(witness)
            R = f.domain
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain (UFD)
    try:
        h1_ok = bool(R.is_UFD)
    except Exception:
        h1_ok = False

    # H_2: The content of f is 1
    try:
        content = f.content()
        h2_ok = (content == R.one) or (content == 1) or (content == sympy.S.One)
    except Exception:
        h2_ok = False

    # H_3: f is irreducible
    try:
        h3_ok = bool(f.is_irreducible)
    except Exception:
        h3_ok = False

    # ¬Q: The factor ring is NOT an integral domain
    try:
        if f.as_expr() == 0:
            # R[x]/<0> is isomorphic to R[x], which is an integral domain since R is a UFD.
            is_id = True
        elif f.degree() == 0 and f.LC() in [1, -1, getattr(R, 'one', 1), -getattr(R, 'one', 1)]:
            # Units generate the whole ring, so the quotient is the zero ring (not an integral domain).
            is_id = False
        else:
            # For all other cases in a UFD, it is an integral domain iff f is irreducible.
            is_id = bool(f.is_irreducible)
            
        neg_q_ok = not is_id
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]