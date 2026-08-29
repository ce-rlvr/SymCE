import sympy

# Top-level setup
# No specific named objects needed for this number theory problem.

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
    
    # H1: (a, b, c) is a Pythagorean triple consisting of positive integers
    try:
        def is_pos_int(x):
            try:
                sx = sympy.sympify(x)
                return bool(sx.is_integer and sx > 0)
            except Exception:
                return False
        
        h1 = is_pos_int(a) and is_pos_int(b) and is_pos_int(c) and sympy.simplify(a**2 + b**2 - c**2) == 0
    except Exception:
        h1 = False
        
    # neg_Q: α can be expressed as qπ for some rational number q
    try:
        # In a right triangle with legs a and b, the acute angles are atan(a/b) and atan(b/a).
        # If one is a rational multiple of pi, the other is too (they sum to pi/2).
        # We use nsimplify to ensure floats are converted to exact rationals if provided.
        sa = sympy.nsimplify(sympy.sympify(a))
        sb = sympy.nsimplify(sympy.sympify(b))
        alpha = sympy.atan2(sa, sb)
        q = alpha / sympy.pi
        q_simp = sympy.simplify(q)
        neg_q = isinstance(q_simp, sympy.Rational)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a Pythagorean triple consisting of positive integers",
    "¬Q: α can be expressed as qπ for some rational number q"
]

N_HYP = 1
NEG_Q_INDEX = 1