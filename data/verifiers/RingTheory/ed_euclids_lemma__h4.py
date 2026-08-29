import sympy
from sympy.abc import x, y, z

# Top-level setup
# No specific named groups or matrices are needed for this ring theory conjecture.
# We provide standard polynomial symbols x, y, z for convenience if the witness uses polynomials.

def is_int_val(val):
    return isinstance(val, int) or isinstance(val, sympy.Integer)

def divides(a, b):
    try:
        # For integers, use exact integer arithmetic
        if is_int_val(a) and is_int_val(b):
            return int(b) % int(a) == 0
        
        # For polynomials or other expressions, use polynomial division over a field
        q, r = sympy.div(b, a)
        return sympy.simplify(r) == 0
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a Euclidean domain
    # We accept integers (Z is a Euclidean domain) or univariate polynomials (F[x] is a Euclidean domain)
    try:
        if all(is_int_val(val) for val in (a, b, c)):
            h1 = True
        elif all(isinstance(val, sympy.Expr) for val in (a, b, c)):
            syms = set()
            for val in (a, b, c):
                syms.update(val.free_symbols)
            h1 = len(syms) <= 1
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: a, b, and c are non-zero elements of R
    try:
        def is_nonzero(val):
            if is_int_val(val):
                return int(val) != 0
            return bool(sympy.simplify(val) != 0)
        
        h2 = is_nonzero(a) and is_nonzero(b) and is_nonzero(c)
    except Exception:
        h2 = False

    # H3: The element a divides the product bc
    try:
        h3 = bool(divides(a, b * c))
    except Exception:
        h3 = False

    # neg_Q: The element a does not divide c
    try:
        neg_q = not divides(a, c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: The element a divides the product bc",
    "¬Q: The element a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3