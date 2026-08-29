import sympy
from sympy import cyclotomic_poly
from sympy.abc import x

# Top-level setup
# (No specific named bindings required for this domain, but we define x for convenience)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple: (n, alpha)
        if len(witness) != 2:
            return [False, False, False]
        n, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False
        
    # H2: alpha in C is a root of Phi_n(x)
    try:
        if h1:
            poly = cyclotomic_poly(int(n), x)
            val = poly.subs(x, alpha)
            # Evaluate to a complex number to check if it's a root
            val_c = complex(sympy.N(val))
            h2 = abs(val_c) < 1e-5
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: absolute value of alpha is NOT exactly 1
    try:
        alpha_c = complex(sympy.N(alpha))
        neg_q = abs(abs(alpha_c) - 1.0) > 1e-5
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: alpha is a root of the n-th cyclotomic polynomial",
    "¬Q: The absolute value of alpha is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2