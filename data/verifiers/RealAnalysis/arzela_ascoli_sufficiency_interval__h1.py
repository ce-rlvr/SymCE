import sympy
from sympy import Symbol, oo, limit, diff

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def is_bounded(expr, a, b):
    try:
        for nv in [1, 10]:
            fn = expr.subs(n, nv)
            if b == oo:
                L = limit(fn, x, oo)
                if L in [oo, -oo, sympy.zoo]: return False
                if hasattr(L, 'min') and (L.min == -oo or L.max == oo): return False
            if a == -oo:
                L = limit(fn, x, -oo)
                if L in [oo, -oo, sympy.zoo]: return False
                if hasattr(L, 'min') and (L.min == -oo or L.max == oo): return False
                    
        test_x = 0
        if a != -oo and a > 0: test_x = float(a)
        elif b != oo and b < 0: test_x = float(b)
        
        x_vals = [test_x, 0, 1, 2, 3, 10, 100, 1000, 10000]
        if a != -oo: x_vals.append(float(a))
        if b != oo: x_vals.append(float(b))
        
        max_vals = []
        for nv in [10, 100, 1000]:
            current_max = 0
            test_x_nv = x_vals + [nv, nv**2, nv/2, nv*2, nv**0.5, nv*10, 1/nv, 1/(nv**2), 2/nv]
            if a == -oo:
                test_x_nv += [-nv, -nv**2, -nv/2, -nv*2, -nv**0.5, -nv*10, -1/nv, -1/(nv**2), -2/nv]
            for xv in test_x_nv:
                try:
                    if (a == -oo or xv >= float(a)) and (b == oo or xv <= float(b)):
                        val = abs(complex(expr.subs({n: nv, x: xv})))
                        if val > current_max:
                            current_max = val
                except Exception:
                    pass
            max_vals.append(current_max)
            
        if max_vals[2] > max_vals[0] * 2 and max_vals[2] > 10:
            return False
            
        fn = expr.subs(n, 10)
        if b == oo:
            try:
                v1 = abs(complex(fn.subs(x, 10)))
                v2 = abs(complex(fn.subs(x, 1000)))
                if v2 > v1 * 2 and v2 > 10:
                    return False
            except Exception:
                pass
        if a == -oo:
            try:
                v1 = abs(complex(fn.subs(x, -10)))
                v2 = abs(complex(fn.subs(x, -1000)))
                if v2 > v1 * 2 and v2 > 10:
                    return False
            except Exception:
                pass
                
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        f = witness['f']
        a = witness['a']
        b = witness['b']
    except Exception:
        return [False, False, False]

    h1 = is_bounded(f, a, b)

    try:
        df = diff(f, x)
        h2 = is_bounded(df, a, b)
    except Exception:
        h2 = False

    neg_q = False
    try:
        try:
            f_inf = limit(f, n, oo)
            if f_inf.has(sympy.Limit):
                f_inf = f.subs(n, 100000)
        except Exception:
            f_inf = f.subs(n, 100000)
            
        x_vals = [0, 1, 2, 3, 10, 100, 1000]
        if a != -oo: x_vals.append(float(a))
        if b != oo: x_vals.append(float(b))
        
        def get_max_diff(nv):
            fn_val = f.subs(n, nv)
            md = 0
            test_x = x_vals + [nv, nv**2, nv/2, nv*2, nv**0.5, nv*10, 1/nv, 1/(nv**2), 2/nv]
            if a == -oo:
                test_x += [-nv, -nv**2, -nv/2, -nv*2, -nv**0.5, -nv*10, -1/nv, -1/(nv**2), -2/nv]
            for xv in test_x:
                try:
                    if (a == -oo or xv >= float(a)) and (b == oo or xv <= float(b)):
                        v1 = complex(fn_val.subs(x, xv))
                        v2 = complex(f_inf.subs(x, xv))
                        d = abs(v1 - v2)
                        if d > md:
                            md = d
                except Exception:
                    pass
            return md
            
        md1 = get_max_diff(1000)
        md2 = get_max_diff(10000)
        
        if md2 > 1e-2 and md2 >= md1 * 0.8:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The sequence f_n is uniformly bounded on the interval",
    "H_2: The sequence f_n is uniformly equicontinuous on the interval",
    "\u00acQ: The sequence f_n does not contain a subsequence that converges uniformly on the interval"
]

N_HYP = 2
NEG_Q_INDEX = 2