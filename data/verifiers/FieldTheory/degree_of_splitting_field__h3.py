import sympy
from sympy.abc import x
import math

# Top-level setup for Ring/Field domain
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    """
    try:
        K = witness[0]
        f = witness[1]
    except Exception:
        return [False, False, False]
    
    # H1: K is a field
    try:
        if hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
        elif isinstance(K, sympy.polys.domains.Domain) and getattr(K, 'has_Field', False):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial in K[x] of degree n >= 1
    try:
        poly_f = sympy.Poly(f, x, domain=K)
        n = poly_f.degree()
        h2 = bool(n >= 1)
    except Exception:
        h2 = False

    # neg_Q: The degree [L:K] does NOT divide n! OR [L:K] > n!
    try:
        # If the witness provides the splitting field degree as a third element, use it.
        if len(witness) >= 3:
            L_degree = int(witness[2])
            n_fact = math.factorial(n)
            neg_q = not ((n_fact % L_degree == 0) and (L_degree <= n_fact))
        else:
            # Mathematically, the degree of the splitting field of any polynomial 
            # of degree n over any field always divides n! and is <= n!.
            # If no explicit degree is provided to override, the conclusion holds.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial of degree n >= 1",
    "neg_Q: L:K does not divide n! or L:K > n!"
]

N_HYP = 2
NEG_Q_INDEX = 2