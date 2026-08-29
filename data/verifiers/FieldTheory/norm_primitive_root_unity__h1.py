import sympy
from sympy.abc import x

# Top-level setup
# No specific bindings needed for this number theory / field theory problem.

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1_ok = False
        else:
            n = int(witness)
            h1_ok = (n >= 1)
    except Exception:
        h1_ok = False

    try:
        n = int(witness)
        poly = sympy.cyclotomic_poly(n, x)
        deg = sympy.degree(poly, x)
        const = poly.subs(x, 0)
        norm = ((-1)**deg) * const
        neg_q_ok = bool(norm != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer (zeta_n is a primitive n-th root of unity)",
    "¬Q: The field norm of zeta_n over Q is not equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1