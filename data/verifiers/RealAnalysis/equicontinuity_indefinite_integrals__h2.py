import sympy
from sympy.abc import x, n
import math

CONDITION_LABELS = [
    "H_1: F is a family of Riemann integrable functions on the interval",
    "not Q: The family of indefinite integrals is not uniformly equicontinuous"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        a, b, f = witness
        a = float(sympy.sympify(a))
        b = float(sympy.sympify(b))
        f = sympy.sympify(f)
    except Exception:
        return [False, False]

    if a >= b:
        return [False, False]

    try:
        free_syms = list(f.free_symbols)
        for s in free_syms:
            if str(s) == 'x' and s != x:
                f = f.subs(s, x)
        
        free_syms = list(f.free_symbols)
        for s in free_syms:
            if s != x and s != n:
                f = f.subs(s, n)
    except Exception:
        pass

    h1_ok = True
    try:
        for test_x in [a, b, (a + b) / 2.0]:
            v = f.subs({x: test_x, n: 1}).evalf()
            if not v.is_real:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        symbolic = False
        try:
            t = sympy.Symbol('t')
            F_sym = sympy.integrate(f.subs(x, t), (t, a, x))
            if not F_sym.has(sympy.Integral):
                F_num = sympy.lambdify((x, n), F_sym, modules=['math', 'sympy'])
                F_num(a, 1)
                symbolic = True
        except Exception:
            pass

        try:
            f_num = sympy.lambdify((x, n), f, modules=['math', 'sympy'])
        except Exception:
            pass

        def get_integral(y, delta, nv):
            if symbolic:
                try:
                    v1 = F_num(y + delta, nv)
                    v2 = F_num(y, nv)
                    if hasattr(v1, 'real'): v1 = v1.real
                    if hasattr(v2, 'real'): v2 = v2.real
                    return abs(float(v1) - float(v2))
                except Exception:
                    pass
            
            steps = 100
            dx = delta / steps
            tot = 0.0
            for i in range(steps):
                try:
                    val = f_num(y + (i + 0.5) * dx, nv)
                    if hasattr(val, 'real'):
                        val = val.real
                    tot += float(val)
                except Exception:
                    pass
            return abs(tot * dx)

        deltas = [(b - a) / 10.0, (b - a) / 100.0, (b - a) / 1000.0, (b - a) / 10000.0]
        omegas = []
        
        for delta in deltas:
            if delta <= 0:
                continue
            
            n_vals = [1, 10, 100, 1000, 10000]
            if delta > 0:
                n_vals.extend([
                    int(0.5 / delta),
                    int(1.0 / delta),
                    int(2.0 / delta),
                    int(3.0 / delta),
                    int(1.0 / (delta**2))
                ])
            n_vals = sorted(list(set([nv for nv in n_vals if nv >= 1])))
            
            max_int = 0.0
            for nv in n_vals:
                if nv > 10000000:
                    continue
                
                y_vals = [a, b - delta]
                num_y = 400 if symbolic else 100
                for i in range(1, num_y):
                    y_vals.append(a + i * (b - a - delta) / float(num_y))
                if nv > 0:
                    y_vals.append(max(a, min(b - delta, a + 1.0/nv)))
                    y_vals.append(max(a, min(b - delta, a + 1.0/math.sqrt(nv))))
                    y_vals.append(max(a, min(b - delta, a + 1.0/(nv**2))))
                    y_vals.append(max(a, min(b - delta, b - 1.0/nv - delta)))
                if a < 0 < b:
                    y_vals.append(max(a, min(b - delta, 0.0)))
                    y_vals.append(max(a, min(b - delta, -delta/2.0)))
                    y_vals.append(max(a, min(b - delta, -delta)))
                y_vals = sorted(list(set(y_vals)))
                
                for y in y_vals:
                    try:
                        val = get_integral(y, delta, nv)
                        if val > max_int:
                            max_int = val
                    except Exception:
                        pass
            omegas.append(max_int)
            
        if len(omegas) == 4:
            if omegas[-1] > 1e-5 and omegas[-1] >= omegas[0] * 0.5:
                neg_q_ok = True
            else:
                neg_q_ok = False
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]