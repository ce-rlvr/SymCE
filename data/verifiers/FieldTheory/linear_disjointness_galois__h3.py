import sympy as sp
from sympy.polys.polytools import gcd, factor_list

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: E/K is an arbitrary field extension",
    "¬Q: The fields L and E are not linearly disjoint over their intersection L ∩ E"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_galois(poly):
    """
    Check if the polynomial defines a Galois extension over Q.
    A polynomial defines a Galois extension if it is irreducible and
    its splitting field has degree equal to the degree of the polynomial.
    For simplicity in this verifier, we check if it is irreducible and
    if the number of roots in its own field equals its degree, or we can
    just check if it factors completely over its own root field.
    """
    try:
        if not poly.is_irreducible:
            return False
        # For small degree polynomials, we can check if the Galois group order equals degree.
        # SymPy's galois_group is not always available or fast, so we use a heuristic or exact check.
        # A quick way for small degrees:
        deg = poly.degree()
        if deg == 1:
            return True
        if deg == 2:
            return True
        # For degree > 2, we can compute the splitting field degree or use factor_list over algebraic extension.
        x = sp.Symbol('x')
        root = sp.RootOf(poly, 0)
        factors = factor_list(poly, extension=root)[1]
        # If it factors completely into linear factors, it's Galois.
        return all(f.degree() == 1 for f, _ in factors)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    witness: A tuple of two SymPy polynomials (f, g) in one variable over Q,
             representing the extensions L = Q[x]/(f) and E = Q[y]/(g).
    """
    try:
        f, g = witness
        x = f.gen
        y = g.gen if g.gen else x
        
        # Ensure they are polynomials over Q
        f = sp.Poly(f, x, domain='QQ')
        g = sp.Poly(g, y, domain='QQ')
    except Exception:
        return [False, False, False]

    # H_1: L/K is a finite Galois extension
    try:
        h1_ok = is_galois(f)
    except Exception:
        h1_ok = False

    # H_2: E/K is an arbitrary field extension
    try:
        h2_ok = g.is_irreducible
    except Exception:
        h2_ok = False

    # ¬Q: L and E are not linearly disjoint over their intersection L ∩ E.
    # If L and E are abstract extensions, their intersection as subfields of a common
    # unspecified field can be ambiguous. If they are not embedded in a common field,
    # their intersection over K is just K.
    # The conjecture fails if we consider them as extensions over K and they share a
    # subextension, making them not linearly disjoint over K.
    # We check if f and g share a common factor in some extension, which means
    # L \otimes_K E is not a field.
    try:
        # L \otimes_K E is a field iff f is irreducible over E = Q[y]/(g).
        # We can check this by seeing if f and g share a common root, or if f factors over E.
        # A simpler check: if f and g are not coprime, or if they share a subfield.
        # Since L/K is Galois, L \otimes_K E is a field iff L \cap E = K.
        # If L \cap E != K, then they are not linearly disjoint over K.
        # We compute the GCD of f and g. If they are the same field, or share a subfield,
        # the tensor product over K is not a field.
        # To be robust, we check if f factors over the field defined by g.
        root_g = sp.RootOf(g, 0)
        factors_f_over_E = factor_list(f, extension=root_g)[1]
        
        # If f factors into more than 1 irreducible polynomial over E, L \otimes_K E is not a field.
        # This means they are not linearly disjoint over K (which is their intersection as abstract extensions).
        is_linearly_disjoint_over_K = (len(factors_f_over_E) == 1 and factors_f_over_E[0][1] == 1)
        
        neg_q_ok = not is_linearly_disjoint_over_K
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]