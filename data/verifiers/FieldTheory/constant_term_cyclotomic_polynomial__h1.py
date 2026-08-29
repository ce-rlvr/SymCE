import sympy
from sympy.abc import x

# Top-level setup
# No specific named objects required for this polynomial/number theory domain.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be an integer n.
    """
    try:
        # H_1: n is a positive integer (so the n-th cyclotomic polynomial is defined)
        if not isinstance(witness, (int, sympy.Integer)):
            h1_ok = False
        else:
            n = int(witness)
            h1_ok = (n >= 1)
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The evaluation Phi_n(0) is NOT exactly 1
        if h1_ok:
            poly = sympy.cyclotomic_poly(n, x)
            val = poly.subs(x, 0)
            neg_q_ok = bool(val != 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Phi_n(0) is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1