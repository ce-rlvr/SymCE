import sympy
from sympy import Poly, factor_list, minimal_polynomial
from sympy.abc import x

def conditions(witness):
    """
    witness is a tuple: (alpha, p, theta)
    where:
      alpha is a sympy Expr representing an algebraic element over Q
      p is a sympy Expr in x representing a polynomial
      theta is a sympy Expr representing an algebraic element defining the extension field K = Q(theta)
    """
    try:
        alpha, p, theta = witness
    except Exception:
        return [False, False, False]
        
    minpoly_alpha = None
    
    # H1: alpha is an algebraic element over F that is separable over F
    # We assume F = Q. Any algebraic element over Q is separable.
    try:
        minpoly_alpha = minimal_polynomial(alpha, x)
        h1 = minpoly_alpha.degree() >= 1
    except Exception:
        h1 = False
        
    # H2: p in F[x] is the minimal polynomial of alpha over F
    try:
        if minpoly_alpha is None:
            h2 = False
        else:
            p_poly = Poly(p, x, domain='QQ')
            min_poly = Poly(minpoly_alpha, x, domain='QQ')
            # The minimal polynomial over a field is uniquely determined when monic.
            h2 = bool((p_poly.monic() == min_poly.monic()) and (p_poly.LC() == 1))
    except Exception:
        h2 = False
        
    # neg_Q: In K[x], p factors as a product of irreducible polynomials of DIFFERENT degrees
    try:
        if isinstance(theta, (list, tuple)):
            _, factors = factor_list(p, extension=list(theta))
        else:
            _, factors = factor_list(p, extension=theta)
            
        degrees = set()
        for f, mult in factors:
            f_poly = Poly(f, x)
            degrees.add(f_poly.degree())
            
        # If there is more than one distinct degree among the irreducible factors,
        # then they do NOT all have the same degree.
        neg_q = len(degrees) > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an algebraic element over F that is separable over F",
    "H_2: p is the minimal polynomial of alpha over F",
    "¬Q: p factors over K into irreducible polynomials of different degrees"
]

N_HYP = 2
NEG_Q_INDEX = 2