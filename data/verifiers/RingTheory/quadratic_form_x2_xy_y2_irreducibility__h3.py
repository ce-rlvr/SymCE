import sympy
from sympy import QQ, ZZ, GF
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K is not 2",
    "H_3: There is no element a in K such that a^2 + 3 = 0",
    "not Q: The polynomial x^2 - xy + y^2 is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # H_1: K is a field
    try:
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    # H_2: The characteristic of K is not 2
    try:
        h2 = bool(witness.characteristic != 2)
    except Exception:
        h2 = False

    # H_3: There is no element a in K such that a^2 + 3 = 0
    try:
        z_sym = sympy.Symbol('z')
        poly_z = sympy.Poly(z_sym**2 + 3, z_sym, domain=witness)
        rts = poly_z.ground_roots()
        h3 = len(rts) == 0
    except Exception:
        h3 = False

    # not Q: The polynomial x^2 - xy + y^2 is reducible over K
    try:
        x_sym, y_sym = sympy.symbols('x y')
        poly = x_sym**2 - x_sym*y_sym + y_sym**2
        coeff, factors = sympy.factor_list(poly, x_sym, y_sym, domain=witness)
        # The polynomial is reducible if it has more than one irreducible factor,
        # or if it has one irreducible factor with multiplicity > 1.
        neg_q = len(factors) > 1 or (len(factors) == 1 and factors[0][1] > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]