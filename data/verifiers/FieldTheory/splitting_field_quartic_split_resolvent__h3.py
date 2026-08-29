import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        poly = Poly(witness, x, domain='QQ')
        h1 = poly.degree() == 4
    except Exception:
        h1 = False

    try:
        poly = Poly(witness, x, domain='QQ')
        h2 = poly.is_irreducible
    except Exception:
        h2 = False

    try:
        poly = Poly(witness, x, domain='QQ')
        h3 = poly.is_squarefree
    except Exception:
        h3 = False

    try:
        poly = Poly(witness, x, domain='QQ')
        if poly.degree() == 4:
            poly = poly.monic()
            coeffs = poly.all_coeffs()
            # A monic quartic has exactly 5 coefficients: [1, a, b, c, d]
            a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
            
            # The resolvent cubic of x^4 + a*x^3 + b*x^2 + c*x + d is:
            # R(x) = x^3 - b*x^2 + (a*c - 4*d)*x - a^2*d + 4*b*d - c^2
            R = Poly(x**3 - b*x**2 + (a*c - 4*d)*x - a**2*d + 4*b*d - c**2, x, domain='QQ')
            
            # The Galois group of an irreducible separable quartic over a field of char != 2, 3
            # is V_4 if and only if its resolvent cubic splits completely over the base field.
            factors = R.factor_list()[1]
            
            # Count the number of rational roots (with multiplicity)
            num_rational_roots = sum(f[1] for f in factors if f[0].degree() == 1)
            has_3_roots = (num_rational_roots == 3)
            
            # Negated conclusion: The Galois group is NOT V_4
            neg_q = not has_3_roots
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a quartic polynomial over Q",
    "H_2: f(x) is irreducible over Q",
    "H_3: f(x) is separable over Q",
    "¬Q: The Galois group of f(x) over Q is not V_4"
]

N_HYP = 3
NEG_Q_INDEX = 3