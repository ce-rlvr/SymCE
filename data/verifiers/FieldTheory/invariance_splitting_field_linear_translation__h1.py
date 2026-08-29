import sympy
from sympy import Poly, simplify, roots, sympify
from sympy.abc import x
from sympy.polys.domains import QQ, ZZ
from sympy import sqrt, I, Rational

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: c is an element of F",
    "H_3: g(x) equals f(x - c)",
    "H_4: E_1 is a splitting field of f over F",
    "H_5: E_2 is a splitting field of g over F",
    "neg_Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        F = witness.get('F')
        f = witness.get('f')
        c = witness.get('c')
        g = witness.get('g')
        E1 = witness.get('E1')
        E2 = witness.get('E2')
        x_sym = witness.get('x', x)
    except Exception:
        return [False] * 6

    def is_extension_field(E, F):
        try:
            if not (hasattr(E, 'is_Field') and E.is_Field):
                return False
            if not (hasattr(F, 'is_Field') and F.is_Field):
                return False
            return E.unify(F) == E
        except Exception:
            return False

    def is_splitting_field(E, poly_expr, F, x_var):
        try:
            if not is_extension_field(E, F):
                return False
            p = Poly(poly_expr, x_var, domain=F)
            
            if p.is_zero:
                return True
            
            rts = roots(p.as_expr(), x_var)
            if sum(rts.values()) != p.degree():
                return False
                
            for r in rts:
                if r not in E:
                    return False
                    
            try:
                gens = [r for r in rts.keys() if r not in F]
                if not gens:
                    expected_E = F
                else:
                    expected_E = F.algebraic_field(*gens)
                return E == expected_E
            except Exception:
                if all(r in F for r in rts):
                    return E == F
                return False
        except Exception:
            return False

    def degree(E, F):
        if E == F:
            return 1
        if hasattr(E, 'mod'):
            return E.mod.degree()
        if hasattr(E, 'ext'):
            try:
                return E.ext.minpoly.degree()
            except Exception:
                pass
        return float('inf')

    def are_isomorphic(E1, E2, F):
        if E1 == E2:
            return True
        deg1 = degree(E1, F)
        deg2 = degree(E2, F)
        if deg1 != deg2:
            return False
        return True

    try:
        Poly(f, x_sym, domain=F)
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = c in F
    except Exception:
        h2 = False

    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else sympify(f)
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else sympify(g)
        h3 = simplify(g_expr - f_expr.subs(x_sym, x_sym - c)) == 0
    except Exception:
        h3 = False

    try:
        h4 = is_splitting_field(E1, f, F, x_sym)
    except Exception:
        h4 = False

    try:
        h5 = is_splitting_field(E2, g, F, x_sym)
    except Exception:
        h5 = False

    try:
        neg_q = not are_isomorphic(E1, E2, F)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]