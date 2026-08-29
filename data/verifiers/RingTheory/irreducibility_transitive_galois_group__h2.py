import sympy
from sympy import Poly, factor_list, Symbol

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a SymPy expression representing a polynomial f(x) over Q.
    """
    # H_1: K is a field
    # We check if the witness is a valid non-constant polynomial over the rationals (Q).
    try:
        p = Poly(witness, x, domain='QQ')
        h1 = p.degree() >= 1
    except Exception:
        h1 = False

    # H_2: L is the splitting field of f(x) over K
    # This is a definitional hypothesis. If f(x) is a valid polynomial over K, 
    # its splitting field L inherently exists.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)
    # Over Q, the Galois group acts transitively on the roots of f(x) if and only if 
    # all roots share the same minimal polynomial. This means the square-free part 
    # of f(x) must be irreducible over Q (i.e., exactly one distinct irreducible factor).
    try:
        if h1:
            factors = factor_list(witness, domain='QQ')
            poly_factors = [f for f, e in factors[1] if Poly(f, x).degree() >= 1]
            h3 = len(poly_factors) == 1
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: f(x) is NOT irreducible over K
    # The polynomial is irreducible if it has exactly one irreducible factor with multiplicity 1.
    # The negation is that it is reducible (either multiple distinct factors or a repeated factor).
    try:
        if h1:
            factors = factor_list(witness, domain='QQ')
            poly_factors = [(f, e) for f, e in factors[1] if Poly(f, x).degree() >= 1]
            is_irreducible = (len(poly_factors) == 1 and poly_factors[0][1] == 1)
            neg_q = not is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is the splitting field of f(x) over K",
    "H_3: The Galois group Gal(L/K) acts transitively on the roots of f(x)",
    "¬Q: f(x) is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3