import sympy
from sympy import Symbol, Poly, sqrt

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false Kummer Extension Theorem
    (which drops the hypothesis that F contains a primitive n-th root of unity).
    
    The witness is expected to be a polynomial in x over Q, representing the 
    field extension E = Q[x]/(P). F is implicitly Q.
    Alternatively, it can be a tuple (P, n).
    """
    try:
        if isinstance(witness, tuple):
            P_expr, n = witness
        else:
            P_expr = witness
            P = Poly(P_expr, x, domain='QQ')
            n = P.degree()
    except Exception:
        return [False, False, False]

    try:
        P = Poly(P_expr, x, domain='QQ')
        deg = P.degree()
        
        # H1: E is a Galois extension of F (F = Q)
        # We only support verifying counterexamples of degree <= 3 for simplicity.
        if deg not in (1, 2, 3):
            h1 = False
        else:
            if not P.is_irreducible:
                h1 = False
            elif deg == 1:
                h1 = True
            elif deg == 2:
                h1 = True
            elif deg == 3:
                # A cubic extension over Q is Galois iff its discriminant is a perfect square
                disc = P.discriminant()
                h1 = sqrt(disc).is_Rational
    except Exception:
        h1 = False

    try:
        # H2: The Galois group is cyclic of order n
        # For degree <= 3, if it is Galois and irreducible, the Galois group is cyclic of order deg.
        if h1 and deg == n:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        # neg_Q: There is NO element a in F such that E is the splitting field of x^n - a over F.
        # For n=1, splitting field of x-a is Q. E=Q. We can pick a=0. So Q is True, neg_Q is False.
        # For n=2, splitting field of x^2-a is Q(sqrt(a)). E is quadratic, so E=Q(sqrt(d)). Pick a=d. Q is True, neg_Q is False.
        # For n=3, the splitting field of x^3-a over Q has degree 1, 2, or 6. It can never be 3.
        # Since E has degree 3, E cannot be the splitting field of x^3-a for any a in Q. So Q is False, neg_Q is True.
        if n == 3 and h1 and h2:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a Galois extension of F",
    "H_2: The Galois group Gal(E/F) is a cyclic group of order n",
    "¬Q: There is no element a in F such that E is the splitting field of x^n - a over F"
]

N_HYP = 2
NEG_Q_INDEX = 2