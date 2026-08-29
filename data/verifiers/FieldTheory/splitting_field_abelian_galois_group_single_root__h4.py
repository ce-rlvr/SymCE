import sympy
from sympy import Poly, gcd, diff, factor_list, RootOf
from sympy.abc import x

# Top-level setup
# We import x from sympy.abc so that the witness can be written as a polynomial expression in x.

def conditions(witness):
    # H_1: f(x) is a non-constant polynomial in x over Q
    try:
        p = Poly(witness, x, domain='QQ')
        h1 = p.degree() >= 1
    except Exception:
        h1 = False

    # H_2: f(x) is irreducible over Q
    try:
        if not h1:
            h2 = False
        else:
            h2 = p.is_irreducible
    except Exception:
        h2 = False

    # H_3: f(x) is separable over Q
    try:
        if not h1:
            h3 = False
        else:
            # Over Q, we can check separability by ensuring gcd(f, f') is a constant
            h3 = Poly(gcd(p.as_expr(), diff(p.as_expr(), x)), x).degree() == 0
    except Exception:
        h3 = False

    # neg_Q: F(alpha) != E
    # The simple extension F(alpha) equals the splitting field E if and only if 
    # f(x) splits completely into linear factors over F(alpha).
    try:
        if not h1:
            neg_q = False
        else:
            expr = p.as_expr()
            # Let alpha be a root of f(x)
            alpha = RootOf(expr, 0)
            # Factor f(x) over the extension field Q(alpha)
            fac_list = factor_list(expr, extension=alpha)[1]
            # If any factor has degree > 1 in x, then f(x) does not split completely in Q(alpha),
            # meaning the splitting field E is strictly larger than Q(alpha).
            neg_q = any(Poly(fac, x).degree() > 1 for fac, mult in fac_list)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial in x over Q",
    "H_2: f(x) is irreducible over Q",
    "H_3: f(x) is separable over Q",
    "¬Q: The simple extension F(alpha) is strictly smaller than the splitting field E"
]

N_HYP = 3
NEG_Q_INDEX = 3