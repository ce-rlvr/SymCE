import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            K1 = witness.get('K1')
            K2 = witness.get('K2')
        else:
            F, f, K1, K2 = witness
    except Exception:
        return [False, False, False, False]

    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
        f_poly = Poly(f_expr, x)
        h1 = f_poly.degree() > 0
    except Exception:
        h1 = False

    try:
        if hasattr(K1, 'order'):
            p = K1.characteristic
            f_poly_p = Poly(f_expr, x, domain=sympy.GF(p))
            factors = f_poly_p.factor_list()[1]
            lcm_deg = 1
            for factor, mult in factors:
                lcm_deg = sympy.lcm(lcm_deg, factor.degree())
            h2 = (K1.order == p**lcm_deg)
        else:
            f_poly_K1 = Poly(f_expr, x, domain=K1)
            roots1 = f_poly_K1.ground_roots()
            if sum(roots1.values()) == f_poly_K1.degree():
                root_exprs = [K1.to_sympy(r) for r in roots1.keys()]
                K_roots = sympy.QQ.algebraic_field(*root_exprs)
                deg1 = K1.ext.degree() if hasattr(K1, 'ext') else 1
                deg_roots = K_roots.ext.degree() if hasattr(K_roots, 'ext') else 1
                h2 = (deg1 == deg_roots)
            else:
                h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(K2, 'order'):
            p = K2.characteristic
            f_poly_p = Poly(f_expr, x, domain=sympy.GF(p))
            factors = f_poly_p.factor_list()[1]
            lcm_deg = 1
            for factor, mult in factors:
                lcm_deg = sympy.lcm(lcm_deg, factor.degree())
            h3 = (K2.order == p**lcm_deg)
        else:
            f_poly_K2 = Poly(f_expr, x, domain=K2)
            roots2 = f_poly_K2.ground_roots()
            if sum(roots2.values()) == f_poly_K2.degree():
                root_exprs = [K2.to_sympy(r) for r in roots2.keys()]
                K_roots = sympy.QQ.algebraic_field(*root_exprs)
                deg2 = K2.ext.degree() if hasattr(K2, 'ext') else 1
                deg_roots = K_roots.ext.degree() if hasattr(K_roots, 'ext') else 1
                h3 = (deg2 == deg_roots)
            else:
                h3 = False
    except Exception:
        h3 = False

    try:
        char1 = getattr(K1, 'characteristic', 0)
        char2 = getattr(K2, 'characteristic', 0)
        if char1 != char2:
            neg_q = True
        else:
            order1 = getattr(K1, 'order', None)
            order2 = getattr(K2, 'order', None)
            if order1 is not None and order2 is not None:
                neg_q = (order1 != order2)
            else:
                deg1 = K1.ext.degree() if hasattr(K1, 'ext') else 1
                deg2 = K2.ext.degree() if hasattr(K2, 'ext') else 1
                if deg1 != deg2:
                    neg_q = True
                else:
                    neg_q = (K1 != K2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = ['H_1: f is a non-constant polynomial', 'H_2: K1 is a splitting field of f', 'H_3: K2 is a splitting field of f', 'not Q: K1 and K2 are not isomorphic']
N_HYP = 3
NEG_Q_INDEX = 3