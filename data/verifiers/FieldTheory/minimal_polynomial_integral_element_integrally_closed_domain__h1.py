import sympy
from sympy import Symbol, Rational, minpoly

def conditions(witness):
    x = Symbol('x')
    try:
        theta, coeffs = witness
        
        p_theta = minpoly(theta, x)
        poly_theta = p_theta.as_poly(x)
        
        if not all(c.is_integer for c in poly_theta.coeffs()):
            return [False, False, False, False]
        if not poly_theta.is_monic:
            return [False, False, False, False]
            
        d = poly_theta.degree()
        if len(coeffs) != d:
            return [False, False, False, False]
            
        alpha = sum(Rational(c) * (theta**i) for i, c in enumerate(coeffs))
        
        # H1: F is the field of fractions of R
        # By definition of our witness structure, R = Z[theta] and F = Q(theta).
        # Since theta is an algebraic integer, Z[theta] is an integral domain
        # and its field of fractions is Q(theta).
        h1 = True
        
        # H2: alpha is an element of an extension field of F
        # alpha is in F, so it is trivially in an extension field of F.
        h2 = True
        
        # H3: alpha is integral over R
        # Since alpha is in F, it is integral over R iff it is an algebraic integer.
        p_alpha = minpoly(alpha, x)
        poly_alpha = p_alpha.as_poly(x)
        h3 = all(c.is_integer for c in poly_alpha.coeffs())
        
        # Conclusion: The minimal polynomial of alpha over F lies in R[x]
        # Since alpha is in F, its minimal polynomial over F is x - alpha.
        # This lies in R[x] iff alpha is in R.
        # Since theta is an algebraic integer of degree d, 1, theta, ..., theta^{d-1}
        # form a basis for R over Z. Thus alpha is in R iff all coeffs are integers.
        # We want the conclusion to FAIL, so neg_q is True if any coeff is not an integer.
        neg_q = any(Rational(c).q != 1 for c in coeffs)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: alpha is an element of an extension field of F",
    "H_3: alpha is integral over R",
    "neg_Q: The minimal polynomial of alpha over F does not lie in the polynomial ring over R"
]

N_HYP = 3
NEG_Q_INDEX = 3