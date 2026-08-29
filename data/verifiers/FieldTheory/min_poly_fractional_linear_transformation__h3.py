import sympy
from sympy import minpoly, degree, simplify, S
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices needed for this field theory conjecture,
# but we define standard symbols for convenience)

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple: (alpha, n, a, b, c, d)
        # We evaluate the conjecture over the base field F = Q.
        alpha, n, a, b, c, d = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: alpha is algebraic over F (Q)
    h1 = False
    p_alpha = None
    try:
        p_alpha = minpoly(alpha, x)
        h1 = True
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of alpha over F has degree n
    h2 = False
    try:
        if h1 and p_alpha is not None:
            h2 = bool(degree(p_alpha, x) == n)
    except Exception:
        h2 = False

    # H_3: c*alpha + d != 0
    h3 = False
    try:
        denom = c * alpha + d
        h3 = bool(simplify(denom) != 0)
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does NOT have degree n
    neg_q = False
    try:
        if h3:
            # Enforce that the transformation coefficients a, b, c, d are in F (Q)
            if all(S(val).is_rational for val in (a, b, c, d)):
                beta = simplify((a * alpha + b) / (c * alpha + d))
                p_beta = minpoly(beta, x)
                neg_q = bool(degree(p_beta, x) != n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over a field F",
    "H_2: The minimal polynomial of alpha over F has degree n",
    "H_3: c*alpha + d != 0",
    "¬Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3