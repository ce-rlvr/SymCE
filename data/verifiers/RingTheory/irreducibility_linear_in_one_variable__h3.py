import sympy
from sympy import Poly, gcd, factor_list
from sympy.abc import x, y

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple or list of two expressions: (a(x), b(x)).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        a_expr, b_expr = witness
        a = sympy.sympify(a_expr)
        b = sympy.sympify(b_expr)
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain (UFD)
    # We evaluate the conjecture over R = QQ, which is a UFD.
    h1 = True

    # H_2: a(x) and b(x) are polynomials in R[x]
    try:
        if not (a.free_symbols.issubset({x}) and b.free_symbols.issubset({x})):
            h2 = False
        else:
            Poly(a, x, domain='QQ')
            Poly(b, x, domain='QQ')
            h2 = True
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of a(x) and b(x) in R[x] is 1
    try:
        if h2:
            g = gcd(a, b)
            g_poly = Poly(g, x, domain='QQ')
            h3 = (g_poly.degree() == 0 and g != 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: a(x)y + b(x) is NOT irreducible in R[x,y]
    try:
        if h2:
            P = a * y + b
            factors = factor_list(P, domain='QQ')
            num_factors = sum(power for f, power in factors[1])
            is_irreducible = (num_factors == 1)
            neg_q = not is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a(x) and b(x) are polynomials over R",
    "H_3: The greatest common divisor of a(x) and b(x) is 1",
    "¬Q: a(x)y + b(x) is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3