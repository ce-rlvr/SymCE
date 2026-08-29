import math
from sympy import Poly, isprime, lcm, QQ, ZZ
from sympy.abc import x
from sympy.polys.domains import GF

def conditions(witness):
    h1, h2, h3, h4, neg_q = False, False, False, False, False
    
    try:
        F = witness.get('F')
        S = witness.get('S')
        E1 = witness.get('E1')
        g = witness.get('g')
        E2 = witness.get('E2')
    except AttributeError:
        return [False, False, False, False, False]

    # H1: F is a field
    p = None
    try:
        if isinstance(F, int) and isprime(F):
            p = F
            h1 = True
    except Exception:
        pass

    # H2: S is a finite set of polynomials over F
    try:
        if p is not None and isinstance(S, (list, tuple, set)):
            all_poly = True
            for f in S:
                Poly(f, x, domain=GF(p))
            h2 = all_poly
    except Exception:
        pass

    # H3: E_1 is a splitting field of the set S over F
    d1 = None
    try:
        if p is not None and h2:
            if isinstance(E1, int) and E1 >= 1:
                d1 = E1
            if d1 is not None:
                req_d1 = 1
                for f in S:
                    poly = Poly(f, x, domain=GF(p))
                    if poly.is_zero:
                        continue
                    factors = poly.factor_list()
                    for fac, mult in factors[1]:
                        req_d1 = lcm(req_d1, fac.degree())
                if d1 == req_d1:
                    h3 = True
    except Exception:
        pass

    # H4: E_2 is a splitting field of the polynomial g over F
    d2 = None
    try:
        if p is not None:
            if isinstance(E2, int) and E2 >= 1:
                d2 = E2
            if d2 is not None:
                poly_g = Poly(g, x, domain=GF(p))
                req_d2 = 1
                if not poly_g.is_zero:
                    factors = poly_g.factor_list()
                    for fac, mult in factors[1]:
                        req_d2 = lcm(req_d2, fac.degree())
                if d2 == req_d2:
                    h4 = True
    except Exception:
        pass

    # neg_Q: E_1 and E_2 are NOT isomorphic over F
    try:
        if d1 is not None and d2 is not None:
            if d1 != d2:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: S is a finite set of polynomials over F",
    "H_3: E_1 is a splitting field of the set S over F",
    "H_4: E_2 is a splitting field of the polynomial g over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 4
NEG_Q_INDEX = 4