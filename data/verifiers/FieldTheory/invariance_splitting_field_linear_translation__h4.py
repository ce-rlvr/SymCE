import sympy
from sympy import Poly, RootOf, sympify
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

QQ = sympy.QQ

def is_splitting_field(f_expr, h_expr):
    try:
        f = Poly(f_expr, x, domain='QQ')
        h = Poly(h_expr, x, domain='QQ')
        
        if not h.is_irreducible:
            return False
            
        if h.degree() == 1:
            factors = f.factor_list()[1]
            return all(fac.degree() == 1 for fac, exp in factors)

        ext = RootOf(h.as_expr(), 0)
        f_ext = Poly(f.as_expr(), x, extension=ext)
        factors = f_ext.factor_list()[1]
        if any(fac.degree() > 1 for fac, exp in factors):
            return False
            
        rts = sympy.roots(f.as_expr(), x, multiple=True)
        if len(rts) == f.degree():
            unique_rts = list(set(rts))
            prim = primitive_element(unique_rts, x)
            if h.degree() != Poly(prim[0], x).degree():
                return False
        else:
            return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    f_expr = witness.get('f')
    c_val = witness.get('c')
    g_expr = witness.get('g')
    E1_expr = witness.get('E1')
    E2_expr = witness.get('E2')
    
    try:
        F = witness.get('F', QQ)
        h1_ok = (F == QQ) or getattr(F, 'is_Field', False)
    except Exception:
        h1_ok = False

    try:
        f_poly = Poly(f_expr, x, domain='QQ')
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        c_sym = sympify(c_val)
        h3_ok = c_sym.is_Rational
    except Exception:
        h3_ok = False

    try:
        h4_ok = is_splitting_field(f_expr, E1_expr)
    except Exception:
        h4_ok = False

    try:
        h5_ok = is_splitting_field(g_expr, E2_expr)
    except Exception:
        h5_ok = False

    try:
        deg1 = Poly(E1_expr, x, domain='QQ').degree()
        deg2 = Poly(E2_expr, x, domain='QQ').degree()
        
        if deg1 != deg2:
            isomorphic = False
        else:
            if deg1 == 1:
                isomorphic = True
            else:
                ext = RootOf(E2_expr, 0)
                E1_ext = Poly(E1_expr, x, extension=ext)
                factors = E1_ext.factor_list()[1]
                isomorphic = any(fac.degree() == 1 for fac, exp in factors)
                
        neg_q_ok = not isomorphic
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: c is an element of F",
    "H_4: E_1 is a splitting field of f over F",
    "H_5: E_2 is a splitting field of g over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 5
NEG_Q_INDEX = 5