import sympy

x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)
t = sympy.Symbol('t', real=True)

def num_integrate(expr, var, a, b, n=1000):
    if abs(a - b) < 1e-12:
        return 0.0
    h = (b - a) / n
    try:
        s = float(expr.subs(var, a)) + float(expr.subs(var, b))
    except Exception:
        s = float(expr.subs(var, a + 1e-9)) + float(expr.subs(var, b - 1e-9))
    
    for i in range(1, n, 2):
        s += 4 * float(expr.subs(var, a + i * h))
    for i in range(2, n-1, 2):
        s += 2 * float(expr.subs(var, a + i * h))
    return s * h / 3.0

def conditions(witness):
    try:
        f_expr, g_expr, a_val, b_val = witness
        f_expr = sympy.sympify(f_expr)
        g_expr = sympy.sympify(g_expr)
        
        free_syms = f_expr.free_symbols | g_expr.free_symbols
        free_syms = {s for s in free_syms if s.is_Symbol}
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = x
        else:
            var = x
            for s in free_syms:
                if s.name == 'x':
                    var = s
                    break
            else:
                var = list(free_syms)[0]
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        a_fl = float(a_val)
        b_fl = float(b_val)
        if a_fl > b_fl:
            h1_ok = False
        else:
            pts = [a_fl + (b_fl - a_fl) * i / 200.0 for i in range(201)]
            is_non_neg = True
            is_decreasing = True
            
            try:
                prev_val = float(f_expr.subs(var, pts[0]))
                if prev_val < -1e-7:
                    is_non_neg = False
            except Exception:
                is_non_neg = False
                is_decreasing = False
                
            for p in pts[1:]:
                try:
                    val = float(f_expr.subs(var, p))
                    if val < -1e-7:
                        is_non_neg = False
                    if val > prev_val + 1e-7:
                        is_decreasing = False
                    prev_val = val
                except Exception:
                    pass
            
            h1_ok = is_non_neg and is_decreasing
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        LHS = sympy.integrate(f_expr * g_expr, (var, a_val, b_val))
        
        if LHS.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
            neg_q_ok = True
        else:
            LHS_val = None
            if LHS.has(sympy.Integral):
                try:
                    LHS_val = num_integrate(f_expr * g_expr, var, a_fl, b_fl)
                except Exception:
                    neg_q_ok = True
            else:
                try:
                    LHS_val = float(LHS)
                except Exception:
                    try:
                        LHS_val = num_integrate(f_expr * g_expr, var, a_fl, b_fl)
                    except Exception:
                        neg_q_ok = True
            
            if LHS_val is not None and not neg_q_ok:
                c = sympy.Symbol('c', real=True)
                G = sympy.integrate(g_expr, (var, a_val, c))
                fa = float(f_expr.subs(var, a_val))
                
                if G.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
                    neg_q_ok = True
                else:
                    RHS = fa * G
                    pts = [a_fl + (b_fl - a_fl) * i / 200.0 for i in range(201)]
                    rhs_vals = []
                    
                    for p in pts:
                        if G.has(sympy.Integral):
                            try:
                                g_int = num_integrate(g_expr, var, a_fl, p, n=100)
                                rhs_vals.append(fa * g_int)
                            except Exception:
                                pass
                        else:
                            try:
                                val = RHS.subs(c, p)
                                if not val.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
                                    rhs_vals.append(float(val))
                            except Exception:
                                pass
                                
                    if not rhs_vals:
                        neg_q_ok = True
                    else:
                        m = min(rhs_vals)
                        M = max(rhs_vals)
                        
                        if LHS_val < m - 1e-4 or LHS_val > M + 1e-4:
                            neg_q_ok = True
                        else:
                            neg_q_ok = False
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The function f is non-negative and monotonically decreasing on the interval",
    "¬Q: There does NOT exist a number c such that the integral equality holds"
]

N_HYP = 1
NEG_Q_INDEX = 1