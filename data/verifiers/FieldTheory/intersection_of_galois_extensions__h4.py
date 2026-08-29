import sympy
from sympy import minpoly, factor_list, I, sqrt, Rational, Symbol
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

# Top-level setup
# The witness should be a tuple of two algebraic numbers (K_elem, L_elem)
# representing the primitive elements of K and L over F = QQ.
# Example: K_elem = 2**(1/3), L_elem = 2**(1/3) + I*sqrt(3)
# Alternatively, K_elem and L_elem can be lists of generators.

def extract_elem(obj):
    if isinstance(obj, (list, tuple)):
        if len(obj) == 1:
            return obj[0]
        try:
            return primitive_element(obj, x)[1]
        except Exception:
            pass
    if hasattr(obj, 'ext'):
        return obj.ext
    return obj

def conditions(witness):
    try:
        K_elem, L_elem = witness
        K_elem = extract_elem(K_elem)
        L_elem = extract_elem(L_elem)
    except Exception:
        return [False, False, False, False, False]

    # H_1: F is a field (we fix F = QQ)
    h1 = True

    # H_2: K and L are finite field extensions of F
    try:
        poly_K = minpoly(K_elem, x)
        poly_L = minpoly(L_elem, x)
        h2 = poly_K.degree() > 0 and poly_L.degree() > 0
    except Exception:
        h2 = False

    # H_3: K and L are contained in a common extension field
    # (True for any algebraic numbers, as they are contained in CC)
    h3 = True if h2 else False

    # H_4: L/F is a Galois extension
    try:
        factors_L = factor_list(poly_L, extension=L_elem)[1]
        h4 = all(f.degree(x) == 1 for f, _ in factors_L)
    except Exception:
        h4 = False

    # neg_Q: The intersection field K \cap L is NOT a Galois extension of F
    try:
        # We check if K is a subfield of L.
        # If K is a subfield of L, then K \cap L = K.
        factors_K_in_L = factor_list(poly_K, extension=L_elem)[1]
        is_K_in_L = all(f.degree(x) == 1 for f, _ in factors_K_in_L)
        
        if is_K_in_L:
            # K \cap L = K. We check if K is Galois over F.
            factors_K = factor_list(poly_K, extension=K_elem)[1]
            is_K_galois = all(f.degree(x) == 1 for f, _ in factors_K)
            neg_q = not is_K_galois
        else:
            # For simplicity, we only evaluate the conclusion for witnesses where K \subset L.
            # If K is not a subfield of L, we reject the witness.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are finite field extensions of F",
    "H_3: K and L are contained in a common extension field",
    "H_4: L/F is a Galois extension",
    "¬Q: The intersection field K \\cap L is not a Galois extension of F"
]

N_HYP = 4
NEG_Q_INDEX = 4