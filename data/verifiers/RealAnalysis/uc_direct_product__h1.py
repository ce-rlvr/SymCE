import sympy as sp

def check_uc(expr, var, domain):
    try:
        expr = sp.sympify(expr)
        var = sp.sympify(var)
        domain = sp.sympify(domain)
        
        if not expr.has(var):
            return True
            
        if isinstance(domain, sp.Interval):
            if not domain.left_open and not domain.right_open and domain.is_bounded:
                sings = sp.calculus.singularities(expr, var, domain)
                if sings.is_empty:
                    return True
                else:
                    return False
            else:
                if domain.left_open and domain.inf != -sp.oo:
                    lim = sp.limit(expr, var, domain.inf, dir='+')
                    if lim in (sp.oo, -sp.oo, sp.nan):
                        return False
                if domain.right_open and domain.sup != sp.oo:
                    lim = sp.limit(expr, var, domain.sup, dir='-')
                    if lim in (sp.oo, -sp.oo, sp.nan):
                        return False
                        
        d = sp.diff(expr, var)
        if d == 0 or d.is_constant():
            return True
            
        if domain == sp.S.Reals:
            if d.is_polynomial(var):
                return False
                
        if hasattr(domain, 'sup') and domain.sup == sp.oo:
            lim = sp.limit(d, var, sp.oo)
            if lim in (sp.oo, -sp.oo):
                return False
        if hasattr(domain, 'inf') and domain.inf == -sp.oo:
            lim = sp.limit(d, var, -sp.oo)
            if lim in (sp.oo, -sp.oo):
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            x1 = witness.get('x1', sp.Symbol('x1'))
            x2 = witness.get('x2', sp.Symbol('x2'))
            X1 = witness.get('X1', sp.S.Reals)
            X2 = witness.get('X2', sp.S.Reals)
            metric_X = witness.get('metric_X', 'max')
            metric_Y = witness.get('metric_Y', 'max')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            f = witness[0]
            g = witness[1]
            x1 = sp.Symbol('x1')
            x2 = sp.Symbol('x2')
            X1 = sp.S.Reals
            X2 = sp.S.Reals
            metric_X = 'max'
            metric_Y = 'max'
            if len(witness) >= 4:
                X1 = witness[2]
                X2 = witness[3]
        else:
            return [False, False, False, False]
            
        if callable(f):
            try:
                x1 = sp.Symbol('x1')
                f = f(x1)
            except Exception:
                pass
        if callable(g):
            try:
                x2 = sp.Symbol('x2')
                g = g(x2)
            except Exception:
                pass
                
        if isinstance(f, str):
            f = sp.sympify(f)
        if isinstance(g, str):
            g = sp.sympify(g)
            
        if isinstance(f, sp.Expr):
            free = f.free_symbols
            if free and x1 not in free:
                x1 = list(free)[0]
        if isinstance(g, sp.Expr):
            free = g.free_symbols
            if free and x2 not in free:
                x2 = list(free)[0]
                
        if f is None or g is None:
            return [False, False, False, False]
            
        h1 = check_uc(f, x1, X1)
        h2 = check_uc(g, x2, X2)
        h3 = (metric_X == 'max' and metric_Y == 'max')
        
        h_is_uc = check_uc(f, x1, X1) and check_uc(g, x2, X2)
        neg_q = not h_is_uc
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on X_1",
    "H_2: g is uniformly continuous on X_2",
    "H_3: The product spaces X_1 x X_2 and Y_1 x Y_2 are equipped with the maximum metric",
    "¬Q: The product map h is not uniformly continuous on X_1 x X_2"
]

N_HYP = 3
NEG_Q_INDEX = 3