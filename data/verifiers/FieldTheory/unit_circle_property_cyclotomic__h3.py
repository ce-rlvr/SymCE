import sympy
from sympy import I, pi, exp, Rational
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices are required for this field theory conjecture)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should provide both n and alpha, e.g., as a tuple (n, alpha) or a dict.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            alpha = witness.get('alpha')
        else:
            n, alpha = witness
    except Exception:
        return [False, False, False]

    # H_1: Let n be a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h1 = False

    # H_2: Let Phi_n(x) be the n-th cyclotomic polynomial over Q
    # This is a definitional hypothesis; it holds as long as n is a valid positive integer.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The absolute value (modulus) of alpha is NOT exactly 1
    try:
        abs_val = sympy.Abs(alpha)
        is_one = (sympy.simplify(abs_val) == 1)
        if not is_one:
            try:
                is_one = (float(abs_val) == 1.0)
            except Exception:
                pass
        neg_q = not is_one
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial over Q",
    "¬Q: The absolute value (modulus) of alpha is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2