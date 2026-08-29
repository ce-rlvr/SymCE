import sympy

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, a, b = witness
                domain = sympy.Interval(a, b)
            elif len(witness) == 2:
                f, domain = witness
                a, b = domain.inf, domain.sup
            else:
                return [False, False]
        else:
            return [False, False]
            
        if callable(f):
            sym = sympy.Symbol('x')
            f_expr = f(sym)
        else:
            f_expr = f
            free_symbols = f_expr.free_symbols
            if len(free_symbols) == 1:
                sym = list(free_symbols)[0]
            elif len(free_symbols) == 0:
                sym = sympy.Symbol('x')
            else:
                x_sym = sympy.Symbol('x')
                if x_sym in free_symbols:
                    sym = x_sym
                else:
                    return [False, False]
                
        try:
            from sympy.calculus.util import continuous_domain
            cont_dom = continuous_domain(f_expr, sym, sympy.S.Reals)
            h1 = bool(domain.is_subset(cont_dom))
        except Exception:
            h1 = False
            
        try:
            is_unbounded = (a == sympy.oo or a == -sympy.oo or b == sympy.oo or b == -sympy.oo)
            if is_unbounded:
                is_poly = f_expr.is_polynomial(sym)
                neg_q = bool(not is_poly)
            else:
                is_uniformly_cont = True
                if domain.left_open:
                    L = sympy.limit(f_expr, sym, a, dir='+')
                    if L == sympy.oo or L == -sympy.oo or not L.is_finite:
                        is_uniformly_cont = False
                if domain.right_open:
                    R = sympy.limit(f_expr, sym, b, dir='-')
                    if R == sympy.oo or R == -sympy.oo or not R.is_finite:
                        is_uniformly_cont = False
                neg_q = not is_uniformly_cont
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "¬Q: f cannot be uniformly approximated by polynomials"
]

N_HYP = 1
NEG_Q_INDEX = 1