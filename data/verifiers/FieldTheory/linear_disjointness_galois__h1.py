import sympy
from sympy import minpoly, degree, isprime, Expr, Symbol
from sympy.polys.numberfields import primitive_element

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two SymPy expressions (a, b) representing 
    the primitive elements of the fields L = Q(a) and E = Q(b).
    """
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            a, b = witness[0], witness[1]
        else:
            a, b = witness, witness
    except Exception:
        return [False, False, False]

    # H_1: E/K is an arbitrary field extension
    # We verify that E = Q(b) is a valid finite extension of Q.
    try:
        poly_b = minpoly(b, x)
        d_E = degree(poly_b, x)
        h1 = isinstance(b, Expr) and d_E > 0
    except Exception:
        h1 = False

    # H_2: L and E are subfields of a common overfield
    # We verify that L = Q(a) is a valid finite extension of Q.
    # Both are subfields of C, so they naturally share a common overfield.
    try:
        poly_a = minpoly(a, x)
        d_L = degree(poly_a, x)
        h2 = isinstance(a, Expr) and d_L > 0
    except Exception:
        h2 = False

    # ¬Q: L and E are NOT linearly disjoint over L \cap E
    try:
        # To rigorously and quickly compute the intersection degree without full Galois theory,
        # we restrict our verification to the standard counterexample family where 
        # the degrees of L and E over Q are prime.
        if not (isprime(d_L) and isprime(d_E)):
            neg_q = False
        else:
            # Compute the degree of the composite field LE = Q(a, b)
            elem, poly_ab = primitive_element([a, b], x, ex=True)
            d_LE = degree(poly_ab, x)
            
            if d_LE > max(d_L, d_E):
                # Since d_L and d_E are prime and L != E (because d_LE > d_L), 
                # their intersection L \cap E must be exactly Q (degree 1).
                # For finite extensions over Q, L and E are linearly disjoint over Q 
                # if and only if [LE : Q] == [L : Q] * [E : Q].
                neg_q = (d_LE < d_L * d_E)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/K is an arbitrary field extension",
    "H_2: L and E are subfields of a common overfield",
    "¬Q: L and E are not linearly disjoint over L \\cap E"
]

N_HYP = 2
NEG_Q_INDEX = 2