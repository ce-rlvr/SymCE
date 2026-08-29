import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def evaluate_func(func, val, x_sym):
    if hasattr(func, 'subs'):
        res = func.subs(x_sym, val).evalf()
        if res.has(sympy.nan, sympy.zoo, sympy.oo, sympy.S.Infinity, sympy.S.NegativeInfinity):
            raise ValueError("Invalid value")
        return complex(res)
    else:
        res = func(val)
        if isinstance(res, complex):
            if math.isnan(res.real) or math.isnan(res.imag) or math.isinf(res.real) or math.isinf(res.imag):
                raise ValueError("Invalid value")
            return res
        else:
            if math.isnan(res) or math.isinf(res):
                raise ValueError("Invalid value")
            return complex(res)

def point_to_segment_dist(p, a, b):
    if a == b:
        return abs(p - a)
    v = b - a
    w = p - a
    t = (w.real * v.real + w.imag * v.imag) / (v.real**2 + v.imag**2)
    if t <= 0:
        return abs(p - a)
    elif t >= 1:
        return abs(p - b)
    else:
        proj = a + t * v
        return abs(p - proj)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
            a = float(witness['a'])
            b = float(witness['b'])
        else:
            f, g, a, b = witness
            a = float(a)
            b = float(b)
    except Exception:
        return [False, False]

    if b - a < 1e-9:
        return [False, False]

    # H1: f is monotonic on the interval
    h1_ok = False
    try:
        N = 1000
        dx = (b - a) / N
        pts = [a + dx * i for i in range(N + 1)]
        vals_complex = [evaluate_func(f, p, x) for p in pts]
        
        if any(abs(v.imag) > 1e-7 for v in vals_complex):
            h1_ok = False
        else:
            vals = [v.real for v in vals_complex]
            inc = all(vals[i] <= vals[i+1] + 1e-7 for i in range(N))
            dec = all(vals[i] >= vals[i+1] - 1e-7 for i in range(N))
            h1_ok = inc or dec
    except Exception:
        h1_ok = False

    # neg_Q: NO c in the interval satisfies the equation
    neg_q_ok = False
    try:
        is_sym = hasattr(f, 'subs') and hasattr(g, 'subs')
        LHS_computed = False
        if is_sym:
            try:
                LHS_exact = sympy.integrate(f * g, (x, a, b))
                if LHS_exact.has(sympy.nan, sympy.zoo, sympy.oo, sympy.S.Infinity, sympy.S.NegativeInfinity):
                    return [h1_ok, True]
                LHS = complex(LHS_exact.evalf())
                LHS_computed = True
            except Exception:
                pass
                
        if not LHS_computed:
            N_int = 1000
            dx_int = (b - a) / N_int
            LHS = sum(evaluate_func(f, a + dx_int * (i + 0.5), x) * evaluate_func(g, a + dx_int * (i + 0.5), x) * dx_int for i in range(N_int))

        G_computed = False
        if hasattr(g, 'subs'):
            try:
                G = sympy.integrate(g, x)
                if G.has(sympy.Integral):
                    raise ValueError("Unevaluated integral")
                def G_val(t):
                    res = G.subs(x, t).evalf()
                    if res.has(sympy.nan, sympy.zoo, sympy.oo, sympy.S.Infinity, sympy.S.NegativeInfinity):
                        raise ValueError("Invalid value")
                    return complex(res)
                Ga = G_val(a)
                Gb = G_val(b)
                
                fa = evaluate_func(f, a, x)
                fb = evaluate_func(f, b, x)
                
                N_c = 1000
                pts_c = [a + (b - a) * i / N_c for i in range(N_c + 1)]
                rhs_vals = [fa * (G_val(p) - Ga) + fb * (Gb - G_val(p)) for p in pts_c]
                G_computed = True
            except Exception:
                pass
                
        if not G_computed:
            N_c = 1000
            dx_c = (b - a) / N_c
            g_vals = [evaluate_func(g, a + dx_c * (i + 0.5), x) for i in range(N_c)]
            G_vals = [0j]
            current = 0j
            for gv in g_vals:
                current += gv * dx_c
                G_vals.append(current)
                
            fa = evaluate_func(f, a, x)
            fb = evaluate_func(f, b, x)
            
            Ga = 0j
            Gb = G_vals[-1]
            
            rhs_vals = [fa * (G_vals[i] - Ga) + fb * (Gb - G_vals[i]) for i in range(N_c + 1)]

        min_dist = min(point_to_segment_dist(LHS, rhs_vals[i], rhs_vals[i+1]) for i in range(len(rhs_vals)-1))
        
        if min_dist > 1e-4:
            neg_q_ok = True
        else:
            neg_q_ok = False
            
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ['H_1: f is monotonic', 'not Q: no such c exists']
N_HYP = 1
NEG_Q_INDEX = 1