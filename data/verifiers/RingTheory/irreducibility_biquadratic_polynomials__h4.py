import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x
from sympy.polys.domains import QQ, ZZ, GF

# Top-level setup for witness evaluation
# The witness should be a tuple (K, a, b) where K is a SymPy domain (e.g., QQ, GF(p)).

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: a and b are elements of K",
    "H_3: b is not a square in K",
    "H_4: b(a^2 - 4b) is not a square in K",
    "¬Q: The polynomial x^4 + a x^2 + b is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        K, a, b = witness
    except Exception:
        return [False] * 5
        
    # H_1: K is a field of characteristic not equal to 2
    try:
        h1 = bool(K.is_Field and K.characteristic != 2)
    except Exception:
        h1 = False
        
    # H_2: a and b are elements of K
    try:
        # Verify that a and b can be coerced into the domain K
        a_K = K(a)
        b_K = K(b)
        # Convert back to SymPy expressions for safe polynomial construction
        a_sym = K.to_sympy(a_K)
        b_sym = K.to_sympy(b_K)
        h2 = True
    except Exception:
        h2 = False
        
    # H_3: b is not a square in K
    try:
        if not (h1 and h2):
            h3 = False
        else:
            # b is a square iff x^2 - b has a root in K.
            # For a degree 2 polynomial, having a root is equivalent to being reducible.
            # Thus, b is NOT a square iff x^2 - b is irreducible over K.
            poly_b = Poly(x**2 - b_sym, x, domain=K)
            h3 = bool(poly_b.is_irreducible)
    except Exception:
        h3 = False
        
    # H_4: b(a^2 - 4b) is not a square in K
    try:
        if not (h1 and h2):
            h4 = False
        else:
            val_sym = b_sym * (a_sym**2 - 4*b_sym)
            poly_val = Poly(x**2 - val_sym, x, domain=K)
            h4 = bool(poly_val.is_irreducible)
    except Exception:
        h4 = False
        
    # ¬Q: The polynomial x^4 + a x^2 + b is reducible over K
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            poly_q = Poly(x**4 + a_sym*x**2 + b_sym, x, domain=K)
            # The conclusion is that it IS irreducible.
            # We want the negation, so it must be REDUCIBLE (i.e., not irreducible).
            neg_q = not bool(poly_q.is_irreducible)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]