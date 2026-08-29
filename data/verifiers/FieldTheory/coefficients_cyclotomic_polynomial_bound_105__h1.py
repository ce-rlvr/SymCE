import sympy
from sympy import cyclotomic_poly, Poly
from sympy.abc import x

# Top-level setup
# (No specific named objects required for this integer-based conjecture)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        # Hypothesis 1: n is a positive integer
        h1 = isinstance(witness, (int, sympy.Integer)) and witness >= 1
        n = int(witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Negated Conclusion: Not every coefficient of Phi_n(x) is in {-1, 0, 1}
            # i.e., there exists at least one coefficient outside this set.
            expr = cyclotomic_poly(n, x)
            poly = Poly(expr, x)
            coeffs = poly.all_coeffs()
            neg_q = any(c not in [-1, 0, 1] for c in coeffs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Phi_n(x) has a coefficient not in {-1, 0, 1}"
]

N_HYP = 1
NEG_Q_INDEX = 1