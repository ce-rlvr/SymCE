import sympy
from sympy.abc import x
from sympy.polys import cyclotomic_poly

# Top-level setup for witness evaluation
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    # H_1: n is an odd number
    try:
        n = int(witness)
        # Cyclotomic polynomials are defined for n >= 1
        h1 = (n % 2 == 1) and (n >= 1)
    except Exception:
        h1 = False

    # ¬Q: \Phi_n(-1) != 1
    try:
        n = int(witness)
        if n < 1:
            neg_q = False
        else:
            poly = cyclotomic_poly(n, x)
            val = poly.subs(x, -1)
            neg_q = bool(val != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd number",
    "¬Q: \\Phi_n(-1) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1