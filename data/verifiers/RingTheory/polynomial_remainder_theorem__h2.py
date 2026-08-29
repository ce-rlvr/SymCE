import sympy
from sympy import Symbol, rem, simplify
from sympy.polys.domains import QQ, RR, CC, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: c is an element of F",
    "¬Q: The remainder when f(x) is divided by (x - c) is not f(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (F, c, f), checks if it is a valid counterexample.
    F: a sympy Domain (e.g., QQ, RR, CC)
    c: an element of F
    f: a sympy expression in terms of x
    """
    try:
        F, c, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1_ok = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1_ok = False
        
    # H_2: c is an element of F
    try:
        h2_ok = bool(c in F)
    except Exception:
        h2_ok = False
        
    # ¬Q: The remainder when f(x) is divided by (x - c) is not f(c)
    try:
        # Compute the polynomial remainder of f divided by (x - c)
        remainder = sympy.rem(f, x - c)
        # Evaluate f at c
        val = f.subs(x, c)
        # Check if they are mathematically equal
        diff = sympy.simplify(remainder - val)
        neg_q_ok = bool(diff != 0)
    except Exception:
        # If rem() raises an exception (e.g., because f(x) is not a polynomial),
        # then the conclusion "the remainder is f(c)" fails.
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]