import sympy
from sympy import minpoly, degree, Poly, QQ, I, sqrt, Rational
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha and beta are algebraic over F",
    "¬Q: F(alpha) intersection F(beta) is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_deg(expr):
    try:
        p = minpoly(expr, x)
        if isinstance(p, Poly):
            return p.degree()
        return degree(p, x)
    except Exception:
        return 0

def in_field(gamma, alpha):
    try:
        deg_a = get_deg(alpha)
        if deg_a == 0:
            return False
        # If gamma is in F(alpha), then F(alpha, gamma) = F(alpha),
        # so the degree of the primitive element of F(alpha, gamma) over F
        # must equal the degree of alpha over F.
        pe, _ = primitive_element([alpha, gamma], x)
        if isinstance(pe, Poly):
            deg_ext = pe.degree()
        else:
            deg_ext = degree(pe, x)
        return deg_ext == deg_a
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            alpha = witness.get('alpha')
            beta = witness.get('beta')
            gamma = witness.get('gamma', None)
        else:
            if len(witness) == 3:
                F, alpha, beta = witness
                gamma = None
            elif len(witness) == 4:
                F, alpha, beta, gamma = witness
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = (F == QQ) or getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: alpha and beta are algebraic over F
    try:
        h2 = False
        if F == QQ:
            d_alpha = get_deg(alpha)
            d_beta = get_deg(beta)
            h2 = (d_alpha >= 1) and (d_beta >= 1)
    except Exception:
        h2 = False

    # ¬Q: F(alpha) \cap F(beta) != F
    try:
        neg_q = False
        if F == QQ:
            gammas_to_try = []
            if gamma is not None:
                gammas_to_try.append(gamma)
            gammas_to_try.extend([alpha, beta])
            
            for g in gammas_to_try:
                if get_deg(g) > 1:  # g is not in F
                    if in_field(g, alpha) and in_field(g, beta):
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]