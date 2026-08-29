import sympy
from sympy.abc import x
from sympy.ntheory import factorint
from sympy.polys import cyclotomic_poly

# Top-level setup
# No specific named objects are required for this domain, but we define x for polynomials.

def conditions(witness) -> list[bool]:
    try:
        val = sympy.sympify(witness)
        if not val.is_integer:
            return [False, False, False]
        n = int(val)
    except Exception:
        return [False, False, False]

    # H_1: n is not of the form p^k for any prime p and integer k >= 1
    try:
        if n < 1:
            h1 = False
        elif n == 1:
            h1 = True
        else:
            factors = factorint(n)
            h1 = (len(factors) != 1)
    except Exception:
        h1 = False

    # H_2: zeta_n is a primitive n-th root of unity
    # This implies n is a valid index for roots of unity (n >= 1)
    try:
        h2 = (n >= 1)
    except Exception:
        h2 = False

    # neg_Q: The field norm N_{Q(zeta_n)/Q}(1-zeta_n) is NOT equal to 1
    try:
        if n >= 1:
            poly = cyclotomic_poly(n, x)
            norm = poly.subs(x, 1)
            neg_q = bool(norm != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is not of the form p^k for any prime p and integer k >= 1",
    "H_2: zeta_n is a primitive n-th root of unity",
    "¬Q: The field norm N_{Q(zeta_n)/Q}(1-zeta_n) is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2