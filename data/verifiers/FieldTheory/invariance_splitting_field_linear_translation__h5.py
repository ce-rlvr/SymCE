import sympy
from sympy import Poly, RootOf, factor, Mul, Rational
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

# Top-level setup for witness expressions
QQ = sympy.QQ
ZZ = sympy.ZZ

def are_isomorphic(m1, m2, var):
    if not isinstance(m1, Poly) or not isinstance(m2, Poly):
        return False
    if m1.degree() != m2.degree():
        return False
    if m1.degree() == 1:
        return True
    try:
        alpha = RootOf(m2.as_expr(), 0)
        factored = factor(m1.as_expr(), extension=alpha)
        if isinstance(factored, Mul):
            factors = factored.args
        else:
            factors = [factored]
        for f in factors:
            base = f.base if f.is_Pow else f
            try:
                p = Poly(base, var)
                if p.degree() == 1:
                    return True
            except Exception:
                pass
    except Exception:
        pass
    return False

def conditions(witness):
    F = witness.get('F')
    f = witness.get('f')
    c = witness.get('c')
    g = witness.get('g')
    E_1 = witness.get('E_1')
    E_2 = witness.get('E_2')
    
    try:
        h1 = getattr(F, 'is_Field', False) or F == sympy.QQ
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(f, Poly) and f.domain == F
    except Exception:
        h2 = False
        
    try:
        h3 = c in F
    except Exception:
        h3 = False
        
    try:
        h4 = (isinstance(f, Poly) and isinstance(g, Poly) and 
              f.gen == g.gen and 
              sympy.simplify(g.as_expr() - f.as_expr().subs(f.gen, f.gen - c)) == 0)
    except Exception:
        h4 = False
        
    try:
        if not isinstance(E_2, Poly) or not isinstance(g, Poly):
            h5 = False
        else:
            var = g.gen
            rts = sympy.roots(g.as_expr(), var)
            if sum(rts.values()) < g.degree():
                h5 = False
            else:
                rts_list = list(rts.keys())
                if not rts_list:
                    minpoly_split = Poly(var, var)
                else:
                    minpoly_split_expr, _ = primitive_element(rts_list, domain=F, x=var)
                    minpoly_split = Poly(minpoly_split_expr, var)
                h5 = are_isomorphic(E_2, minpoly_split, var) and (E_2.is_irreducible == True)
    except Exception:
        h5 = False
        
    try:
        neg_q = isinstance(E_1, Poly) and isinstance(E_2, Poly) and not are_isomorphic(E_1, E_2, E_1.gen)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: c is an element of F",
    "H_4: g(x) = f(x - c)",
    "H_5: E_2 is a splitting field of g(x) over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 5
NEG_Q_INDEX = 5