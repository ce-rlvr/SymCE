import sympy
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                h1 = True
            elif len(witness) == 3:
                F, f, g = witness
                if hasattr(F, 'is_Field') and F.is_Field:
                    h1 = True
                elif F in [sympy.QQ, sympy.RR, sympy.CC]:
                    h1 = True
                elif str(F) in ['Q', 'R', 'C', 'QQ', 'RR', 'CC', 'Field', 'F']:
                    h1 = True
                else:
                    h1 = False
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if isinstance(f, sympy.Poly):
            f = f.as_expr()
        else:
            f = sympy.sympify(f)
            
        if isinstance(g, sympy.Poly):
            g = g.as_expr()
        else:
            g = sympy.sympify(g)
            
        try:
            poly_f = sympy.Poly(f, x, domain='QQ')
            poly_g = sympy.Poly(g, x, domain='QQ')
            
            h2 = (f != 0) and (g != 0)
            if f.free_symbols - {x} or g.free_symbols - {x}:
                h2 = False
        except Exception:
            h2 = False
            
        if h2:
            try:
                deg_f = poly_f.degree()
                deg_g = poly_g.degree()
                h3 = max(deg_f, deg_g) >= 1
            except Exception:
                h3 = False
                
        if h2:
            try:
                expr = f + y * g
                factors = sympy.factor_list(expr)
                num_non_constant_factors = sum(mult for fac, mult in factors[1] if fac.free_symbols)
                neg_q = num_non_constant_factors > 1
            except Exception:
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f and g are non-zero polynomials over F",
    "H_3: max(deg(f), deg(g)) >= 1",
    "not Q: f(x) + y g(x) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3