import sympy
from sympy import cyclotomic_poly

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        n, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(n, int) and n >= 3
    except Exception:
        h1 = False

    try:
        # The second hypothesis is definitional (Phi_n(x) is the n-th cyclotomic polynomial)
        h2 = True
    except Exception:
        h2 = False

    try:
        x_sym = sympy.Symbol('x')
        poly = cyclotomic_poly(n, x_sym)
        val = sympy.simplify(poly.subs(x_sym, sympy.sympify(x)))
        try:
            # In sympy, comparing a non-real complex number to 0 raises a TypeError.
            # If val is real, it evaluates to True or False.
            is_pos = bool(val > 0)
        except TypeError:
            is_pos = False
        neg_q = not is_pos
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: Phi_n(x) is not strictly positive"
]

N_HYP = 2
NEG_Q_INDEX = 2