import sympy
from sympy import Poly, QQ, ZZ, GF
from sympy.abc import x

# Top-level setup
# x is provided for convenience in defining polynomials.
# QQ, ZZ, GF are provided for specifying domains.

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    poly = None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                expr, domain = witness
                poly = sympy.Poly(expr, domain=domain)
            elif len(witness) == 3:
                expr, gen, domain = witness
                poly = sympy.Poly(expr, gen, domain=domain)
        elif isinstance(witness, sympy.Poly):
            poly = witness
    except Exception:
        pass

    # H1: alpha is algebraic over F (witness is an irreducible polynomial over a field F)
    try:
        if poly is not None:
            domain = poly.domain
            if getattr(domain, 'is_Field', False) and poly.is_univariate:
                if poly.is_irreducible:
                    h1 = True
    except Exception:
        h1 = False

    # H2: The minimal polynomial of alpha over F has an odd degree
    try:
        if poly is not None:
            if poly.degree() % 2 == 1:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The simple extension field F(alpha) is not formally real
    try:
        if poly is not None:
            domain = poly.domain
            
            def is_formally_real(dom):
                if hasattr(dom, 'characteristic') and dom.characteristic > 0:
                    return False
                if hasattr(dom, 'char') and dom.char > 0:
                    return False
                if dom == sympy.QQ or dom == sympy.RR:
                    return True
                if dom == sympy.CC:
                    return False
                if hasattr(dom, 'ext'):
                    from sympy import minpoly, real_roots, Dummy
                    x_dummy = Dummy('x')
                    p = minpoly(dom.ext, x_dummy)
                    rr = real_roots(p)
                    return len(rr) > 0
                if hasattr(dom, 'domain'):
                    return is_formally_real(dom.domain)
                return True
            
            if not is_formally_real(domain):
                # If F is not formally real, F(alpha) cannot be formally real
                neg_q = True
            else:
                # If F is formally real, F(alpha) is formally real iff alpha can be embedded in R.
                # For odd degree polynomials, there is always at least one real root.
                if poly.degree() % 2 == 1:
                    neg_q = False
                else:
                    from sympy import real_roots
                    rr = real_roots(poly)
                    if len(rr) == 0:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F (witness is an irreducible polynomial over a field F)",
    "H_2: The minimal polynomial of alpha over F has an odd degree",
    "¬Q: The simple extension field F(alpha) is not formally real"
]

N_HYP = 2
NEG_Q_INDEX = 2