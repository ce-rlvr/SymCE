import sympy
from sympy import Symbol, Poly, diff, minpoly
from sympy import QQ, ZZ, GF, Rational, Integer, I, sqrt
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (m_expr, alpha) or (F, m_expr, alpha), or a dictionary
    with keys 'm', 'alpha', and optionally 'F'.
    """
    try:
        if isinstance(witness, dict):
            m_expr = witness.get('m')
            alpha = witness.get('alpha')
            F_in = witness.get('F', None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                F_in, m_expr, alpha = witness
            else:
                m_expr, alpha = witness
                F_in = None
        else:
            return [False, False, False, False]
            
        if isinstance(m_expr, Poly):
            m = m_expr
            gen_x = m.gen
            if F_in is not None:
                m = m.set_domain(F_in)
            elif not m.domain.is_Field:
                m = m.set_domain(m.domain.get_field())
        else:
            gen_x = Symbol('x')
            if F_in is not None:
                m = Poly(m_expr, gen_x, domain=F_in)
            else:
                m = Poly(m_expr, gen_x)
                if not m.domain.is_Field:
                    m = Poly(m_expr, gen_x, domain=m.domain.get_field())
        F = m.domain
    except Exception:
        return [False, False, False, False]

    # H1: F is a field and alpha is algebraic over F
    try:
        p = minpoly(alpha, gen_x, domain=F)
        h1 = bool(F.is_Field and p is not None)
    except Exception:
        h1 = False

    # H2: alpha is separable over F
    try:
        p = minpoly(alpha, gen_x, domain=F)
        p_poly = Poly(p, gen_x, domain=F)
        p_diff = Poly(diff(p, gen_x), gen_x, domain=F)
        g = p_poly.gcd(p_diff)
        h2 = bool(g.degree() == 0)
    except Exception:
        h2 = False

    # H3: Let Delta be the discriminant of the polynomial m(x)
    try:
        Delta = m.discriminant()
        h3 = True
    except Exception:
        h3 = False

    # neg_Q: The discriminant Delta is NOT a non-zero element of the base field F
    # Since Delta is computed as the discriminant of a polynomial over F, it is in F.
    # Thus, it fails to be a "non-zero element" precisely when it is zero.
    try:
        neg_q = bool(Delta == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and alpha is algebraic over F",
    "H_2: alpha is separable over F",
    "H_3: Delta is the discriminant of m(x)",
    "¬Q: The discriminant Delta is zero"
]

N_HYP = 3
NEG_Q_INDEX = 3