import sympy
from sympy.abc import x
from sympy.ntheory import isprime

# Top-level setup
# (No specific named objects required for this number theory/polynomial conjecture)

def conditions(witness) -> list[bool]:
    try:
        n, p = witness
    except Exception:
        return [False, False, False]

    # H_1: n >= 1 is an integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = (isinstance(p, int) or isinstance(p, sympy.Integer)) and isprime(p)
    except Exception:
        h2 = False

    # ¬Q: Phi_{pn}(x) != Phi_n(x^p) / Phi_n(x)
    # Equivalently: Phi_{pn}(x) * Phi_n(x) != Phi_n(x^p)
    try:
        n_int = int(n)
        p_int = int(p)
        poly_pn = sympy.cyclotomic_poly(p_int * n_int, x)
        poly_n = sympy.cyclotomic_poly(n_int, x)
        poly_n_xp = sympy.cyclotomic_poly(n_int, x**p_int)
        
        diff = sympy.expand(poly_pn * poly_n - poly_n_xp)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p is a prime number",
    "¬Q: Phi_{pn}(x) != Phi_n(x^p) / Phi_n(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2