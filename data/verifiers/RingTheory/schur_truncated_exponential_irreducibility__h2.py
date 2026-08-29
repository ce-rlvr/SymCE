import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup
# The symbol 'x' is imported from sympy.abc and is available for witness expressions.

def conditions(witness) -> list[bool]:
    n = None
    f = None
    try:
        # The witness can be a tuple (n, f) or just the polynomial f
        if isinstance(witness, tuple) and len(witness) == 2:
            n, f = witness
        else:
            f = witness
            n = sympy.degree(f, x)
    except Exception:
        pass

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h1_ok = False

    # ¬Q: f(x) is not irreducible over Q
    try:
        if isinstance(f, list):
            # If f is provided as a list of coefficients [c_0, c_1, ..., c_n]
            f_expr = sum(c * x**i for i, c in enumerate(f))
        else:
            f_expr = sympy.sympify(f)
            
        poly_f = Poly(f_expr, x, domain='QQ')
        # The conclusion is that f(x) is irreducible.
        # We want the negation: f(x) is NOT irreducible.
        neg_q_ok = not poly_f.is_irreducible
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1