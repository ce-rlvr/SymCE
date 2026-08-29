import sympy
from sympy.polys import cyclotomic_poly
from sympy.abc import x

# Top-level setup
# (No special named objects needed for this number/field theory conjecture)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    \Phi_{2n}(x) = \Phi_n(-x)
    """
    try:
        n = int(witness)
        h1 = (n == witness) and (n >= 1)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        poly_2n = cyclotomic_poly(2 * n, x)
        poly_n_minus_x = cyclotomic_poly(n, x).subs(x, -x)
        diff = sympy.expand(poly_2n - poly_n_minus_x)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (domain of cyclotomic polynomials)",
    "¬Q: \Phi_{2n}(x) != \Phi_n(-x)"
]

N_HYP = 1
NEG_Q_INDEX = 1