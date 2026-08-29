import sympy
from sympy import Poly, minpoly, eye, zeros, Rational, Integer
from sympy.abc import x

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    
    The witness can be a tuple: (alpha, p) or (F, alpha, p)
    where alpha is an algebraic element and p is a sympy.Poly.
    """
    try:
        if len(witness) == 2:
            alpha, p = witness
            if not isinstance(p, Poly):
                p = Poly(p, x)
            F = p.domain
        elif len(witness) == 3:
            F, alpha, p = witness
            if not isinstance(p, Poly):
                p = Poly(p, x, domain=F)
            F = p.domain
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: F is a field
    try:
        h1 = F.is_Field
    except Exception:
        h1 = False

    # H_2: alpha is an algebraic element over F
    try:
        gen = p.gen
        # minpoly will raise an exception if alpha is not algebraic over F
        m_alpha = minpoly(alpha, gen, domain=F)
        h2 = True
    except Exception:
        h2 = False

    # H_3: n is the degree of p(x)
    try:
        if not p.is_univariate:
            h3 = False
        else:
            n = p.degree()
            h3 = (n >= 0)
    except Exception:
        h3 = False

    # H_4: g(x) is defined by g(x^2) = (-1)^n p(x)p(-x)
    try:
        p_minus = Poly(p.as_expr().subs(gen, -gen), gen, domain=F)
        prod = p * p_minus * ((-1)**n)
        
        g_dict = {}
        h4 = True
        for power, coeff in prod.terms():
            if power[0] % 2 != 0:
                if coeff != 0:
                    h4 = False
                    break
            else:
                g_dict[(power[0] // 2,)] = coeff
        
        if h4:
            g = Poly.from_dict(g_dict, gen, domain=F)
            h4 = True
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of alpha^2 over F does NOT divide g(x)
    try:
        m_alpha2 = minpoly(alpha**2, gen, domain=F)
        m_alpha2_poly = Poly(m_alpha2, gen, domain=F)
        rem = g % m_alpha2_poly
        neg_q = not rem.is_zero
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: n is the degree of p(x)",
    "H_4: g(x) is defined by g(x^2) = (-1)^n p(x)p(-x)",
    "¬Q: The minimal polynomial of alpha^2 over F does not divide g(x)"
]

N_HYP = 4
NEG_Q_INDEX = 4