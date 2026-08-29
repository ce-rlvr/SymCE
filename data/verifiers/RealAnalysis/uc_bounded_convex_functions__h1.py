import sympy
from sympy import Symbol, Interval, Piecewise, Eq, oo

x = Symbol('x', real=True)

def linspace(start, stop, n):
    if n == 1:
        return [start]
    step = (stop - start) / (n - 1)
    return [start + i * step for i in range(n)]

def is_in_domain(domain, val):
    try:
        res = domain.contains(val)
        if res == True: return True
        if res == False: return False
        return False
    except:
        return False

def get_points(domain, n=50):
    points = []
    inf = domain.inf
    sup = domain.sup
    
    if inf != -sympy.oo and is_in_domain(domain, inf):
        points.append(inf)
    if sup != sympy.oo and is_in_domain(domain, sup):
        points.append(sup)
        
    inf_f = float(inf) if inf != -sympy.oo else -100.0
    sup_f = float(sup) if sup != sympy.oo else 100.0
    
    if inf != -sympy.oo and sup != sympy.oo:
        w = sup_f - inf_f
        for p in linspace(inf_f + w*1e-3, sup_f - w*1e-3, n):
            points.append(p)
        if not is_in_domain(domain, inf):
            points.extend([inf_f + w*1e-4, inf_f + w*1e-5, inf_f + w*1e-6])
        if not is_in_domain(domain, sup):
            points.extend([sup_f - w*1e-4, sup_f - w*1e-5, sup_f - w*1e-6])
    elif inf != -sympy.oo:
        for p in linspace(inf_f + 1e-3, inf_f + 100.0, n):
            points.append(p)
        if not is_in_domain(domain, inf):
            points.extend([inf_f + 1e-4, inf_f + 1e-5, inf_f + 1e-6])
    elif sup != sympy.oo:
        for p in linspace(sup_f - 100.0, sup_f - 1e-3, n):
            points.append(p)
        if not is_in_domain(domain, sup):
            points.extend([sup_f - 1e-4, sup_f - 1e-5, sup_f - 1e-6])
    else:
        for p in linspace(-100.0, 100.0, n):
            points.append(p)
            
    return points

def eval_f(f, val):
    if callable(f):
        return float(f(val))
    if isinstance(f, (int, float)):
        return float(f)
    return float(f.subs(x, val))

def check_convexity(f, domain):
    pts = get_points(domain, 30)
    f_vals = {}
    for p in pts:
        try:
            val = eval_f(f, p)
            f_vals[p] = val
        except Exception:
            return False
            
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            p1 = pts[i]
            p2 = pts[j]
            v1 = f_vals[p1]
            v2 = f_vals[p2]
            
            for t in [0.2, 0.5, 0.8]:
                p_mid = t * p1 + (1 - t) * p2
                try:
                    v_mid = eval_f(f, p_mid)
                except Exception:
                    return False
                
                if v_mid > t * v1 + (1 - t) * v2 + 1e-4:
                    return False
    return True

def check_boundedness(f, domain):
    if not callable(f):
        try:
            from sympy.calculus.util import function_range
            frange = function_range(f, x, domain)
            if frange.inf == -sympy.oo or frange.sup == sympy.oo:
                return False
            if frange.inf != -sympy.oo and frange.sup != sympy.oo:
                return True
        except Exception:
            pass
        
    try:
        if domain.sup == sympy.oo:
            v1 = eval_f(f, 100)
            v2 = eval_f(f, 1e4)
            v3 = eval_f(f, 1e5)
            if abs(v3 - v2) > 100 or abs(v2 - v1) > 100:
                return False
        if domain.inf == -sympy.oo:
            v1 = eval_f(f, -100)
            v2 = eval_f(f, -1e4)
            v3 = eval_f(f, -1e5)
            if abs(v3 - v2) > 100 or abs(v2 - v1) > 100:
                return False
    except:
        pass

    pts = get_points(domain, 100)
    try:
        vals = [eval_f(f, p) for p in pts]
        if max(vals) - min(vals) > 1e4:
            return False
    except Exception:
        return False
        
    return True

def is_not_uniformly_continuous(f, domain):
    try:
        pts = get_points(domain, 100)
        vals = [eval_f(f, p) for p in pts]
        if max(vals) - min(vals) > 1e4:
            return True
    except:
        pass

    if domain.inf != -sympy.oo and is_in_domain(domain, domain.inf):
        try:
            val = eval_f(f, domain.inf)
            w = float(domain.sup - domain.inf) if domain.sup != sympy.oo else 1.0
            val_near = eval_f(f, float(domain.inf) + w * 1e-7)
            if abs(val - val_near) > 1e-3:
                return True
        except:
            pass
            
    if domain.sup != sympy.oo and is_in_domain(domain, domain.sup):
        try:
            val = eval_f(f, domain.sup)
            w = float(domain.sup - domain.inf) if domain.inf != -sympy.oo else 1.0
            val_near = eval_f(f, float(domain.sup) - w * 1e-7)
            if abs(val - val_near) > 1e-3:
                return True
        except:
            pass
            
    if domain.inf != -sympy.oo and not is_in_domain(domain, domain.inf):
        try:
            w = float(domain.sup - domain.inf) if domain.sup != sympy.oo else 1.0
            v1 = eval_f(f, float(domain.inf) + w * 1e-4)
            v2 = eval_f(f, float(domain.inf) + w * 1e-5)
            v3 = eval_f(f, float(domain.inf) + w * 1e-6)
            if (v1 - v2) * (v2 - v3) < 0 and abs(v1 - v2) > 0.1:
                return True
        except:
            pass

    if domain.sup != sympy.oo and not is_in_domain(domain, domain.sup):
        try:
            w = float(domain.sup - domain.inf) if domain.inf != -sympy.oo else 1.0
            v1 = eval_f(f, float(domain.sup) - w * 1e-4)
            v2 = eval_f(f, float(domain.sup) - w * 1e-5)
            v3 = eval_f(f, float(domain.sup) - w * 1e-6)
            if (v1 - v2) * (v2 - v3) < 0 and abs(v1 - v2) > 0.1:
                return True
        except:
            pass

    if not callable(f):
        if domain.sup == sympy.oo:
            try:
                df = sympy.diff(f, x)
                d1 = abs(float(df.subs(x, 100)))
                d2 = abs(float(df.subs(x, 1000)))
                if d2 > 10 and d2 > d1 * 2:
                    return True
            except:
                pass
                
        if domain.inf == -sympy.oo:
            try:
                df = sympy.diff(f, x)
                d1 = abs(float(df.subs(x, -100)))
                d2 = abs(float(df.subs(x, -1000)))
                if d2 > 10 and d2 > d1 * 2:
                    return True
            except:
                pass

    return False

def conditions(witness) -> list[bool]:
    try:
        f, domain = witness
        if isinstance(domain, tuple):
            if len(domain) == 2:
                domain = Interval(domain[0], domain[1])
            elif len(domain) == 4:
                domain = Interval(domain[0], domain[1], domain[2], domain[3])
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_convexity(f, domain)
    except Exception:
        h1 = False
        
    try:
        h2 = check_boundedness(f, domain)
    except Exception:
        h2 = False
        
    try:
        neg_q = is_not_uniformly_continuous(f, domain)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a convex function on I",
    "H_2: f is bounded on I",
    "¬Q: f is not uniformly continuous on I"
]

N_HYP = 2
NEG_Q_INDEX = 2