import sympy
from sympy.abc import x
import math

# Top-level setup
# (No specific named objects required for this conjecture)

def conditions(witness) -> list[bool]:
    def get_n(w):
        if isinstance(w, str):
            return int(w)
        try:
            return math.prod(int(i) for i in iter(w))
        except TypeError:
            return int(w)

    # H_1: \Phi_{pq}(x) is the pq-th cyclotomic polynomial
    # We interpret this as the index being a valid positive integer.
    try:
        n = get_n(witness)
        h1_ok = bool(n >= 1)
    except Exception:
        h1_ok = False

    # neg_Q: Every coefficient of \Phi_{pq}(x) is an element of {-1, 0, 1}
    # Negation: At least one coefficient is NOT in {-1, 0, 1}
    try:
        n = get_n(witness)
        if n >= 1:
            poly = sympy.cyclotomic_poly(n, x).as_poly()
            coeffs = poly.all_coeffs()
            neg_q_ok = any(c not in [-1, 0, 1] for c in coeffs)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: index is a valid positive integer for a cyclotomic polynomial",
    "¬Q: some coefficient of the cyclotomic polynomial is not in {-1, 0, 1}"
]

N_HYP = 1
NEG_Q_INDEX = 1