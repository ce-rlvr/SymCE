import sympy
from sympy import Symbol, Poly

# Top-level setup for witness expressions
x = Symbol('x')

def get_splitting_field_degree(poly_expr):
    p = Poly(poly_expr, x, domain='QQ')
    rts = sympy.roots(p)
    if sum(rts.values()) != p.degree():
        raise ValueError("Roots not found")
    
    irrational_roots = [r for r in rts.keys() if not r.is_rational]
    if not irrational_roots:
        return 1
    
    unique_roots = list(set(irrational_roots))
    result = sympy.polys.numberfields.primitive_element(unique_roots, x)
    if isinstance(result, tuple):
        min_poly = result[0]
    else:
        min_poly = result
    return Poly(min_poly, x).degree()

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            F, f, g, K = witness
            f = sympy.sympify(f)
            g = sympy.sympify(g)
            
            # H_1: F is a field
            try:
                h1 = bool(F.is_Field)
            except Exception:
                h1 = False
                
            # H_2: f(x) and g(x) are polynomials over F
            try:
                Poly(f, x, domain=F)
                Poly(g, x, domain=F)
                h2 = True
            except Exception:
                h2 = False
                
            # H_3: K is the splitting field of f(x) over F
            try:
                if F == sympy.QQ:
                    deg_f = get_splitting_field_degree(f)
                    if hasattr(K, 'ext'):
                        deg_K = K.ext.degree()
                    elif hasattr(K, 'degree'):
                        deg_K = K.degree()
                    elif K == sympy.QQ:
                        deg_K = 1
                    else:
                        deg_K = -1
                    h3 = (deg_K == deg_f)
                else:
                    h3 = False
            except Exception:
                h3 = False
                
            # ¬Q: K is not the splitting field of f(x)g(x) over F
            try:
                if F == sympy.QQ:
                    deg_fg = get_splitting_field_degree(f * g)
                    if hasattr(K, 'ext'):
                        deg_K = K.ext.degree()
                    elif hasattr(K, 'degree'):
                        deg_K = K.degree()
                    elif K == sympy.QQ:
                        deg_K = 1
                    else:
                        deg_K = -1
                    neg_q = (deg_K != deg_fg)
                else:
                    neg_q = False
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
            
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, g = witness
            f = sympy.sympify(f)
            g = sympy.sympify(g)
            
            # H_1: F is a field (implicitly QQ)
            h1 = True
            
            # H_2: f(x) and g(x) are polynomials over F
            try:
                Poly(f, x, domain='QQ')
                Poly(g, x, domain='QQ')
                h2 = True
            except Exception:
                h2 = False
                
            # H_3: K is the splitting field of f(x) over F (implicitly defined)
            try:
                deg_f = get_splitting_field_degree(f)
                h3 = True
            except Exception:
                h3 = False
                
            # ¬Q: K is not the splitting field of f(x)g(x) over F
            try:
                deg_fg = get_splitting_field_degree(f * g)
                neg_q = (deg_fg > deg_f)
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) and g(x) are polynomials over F",
    "H_3: K is the splitting field of f(x) over F",
    "not Q: K is not the splitting field of f(x)g(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3