import sympy as sp
from sympy import Symbol, simplify, limit, oo, zoo, nan, integrate, Abs, sqrt, im
import math

# Top-level setup
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    a = witness.get("a")
    b = witness.get("b")
    f_n = witness.get("f_n")
    f = witness.get("f")
    wx = witness.get("x", x)
    wn = witness.get("n", n)
    
    # H_1: interval is closed and bounded
    h1_ok = False
    try:
        if a is not None and b is not None:
            fa = float(a)
            fb = float(b)
            if not (math.isinf(fa) or math.isinf(fb)):
                h1_ok = bool(fa < fb)
    except Exception:
        h1_ok = False
        
    # H_2: sequence of functions to reals
    h2_ok = False
    try:
        if h1_ok and f_n is not None:
            fa = float(a)
            fb = float(b)
            # Check endpoints and some interior points
            pts = [fa, fb, (fa+fb)/2, fa + 0.1*(fb-fa), fb - 0.1*(fb-fa)]
            all_real = True
            for pt in pts:
                for n_val in [1, 2, 10]:
                    val = f_n.subs({wx: pt, wn: n_val})
                    if not val.is_real and not isinstance(val, (int, float)):
                        if not val.is_number or im(val) != 0:
                            all_real = False
                            break
                if not all_real:
                    break
            
            if all_real:
                h2_ok = True
                # Try to find singularities in the interval
                try:
                    from sympy.calculus.singularities import singularities
                    from sympy import Interval
                    sings = singularities(f_n.subs(wn, 1), wx)
                    if not sings.intersect(Interval(a, b)).is_empty:
                        h2_ok = False
                except Exception:
                    pass
    except Exception:
        h2_ok = False
        
    # H_3: sequence converges uniformly
    h3_ok = False
    try:
        if h1_ok and f_n is not None and f is not None:
            diff = simplify(f_n - f)
            if diff == 0:
                h3_ok = True
            elif not diff.has(wx):
                L = limit(diff, wn, oo)
                if not L.has(sp.Limit):
                    h3_ok = bool(L == 0)
            else:
                fa = float(a)
                fb = float(b)
                # Check pointwise convergence on a dense and moving grid
                pts = [
                    fa, fb, (fa+fb)/2,
                    fa + (fb-fa)/wn, fb - (fb-fa)/wn,
                    fa + (fb-fa)/sqrt(wn), fb - (fb-fa)/sqrt(wn),
                    fa + (fb-fa)/wn**2, fb - (fb-fa)/wn**2
                ]
                is_unif = True
                for pt in pts:
                    val = diff.subs(wx, pt)
                    L = limit(val, wn, oo)
                    if L.has(sp.Limit) or L != 0:
                        is_unif = False
                        break
                h3_ok = is_unif
    except Exception:
        h3_ok = False
        
    # ¬Q: limit function is not Riemann integrable or integrals do not converge
    neg_q_ok = False
    try:
        if h1_ok and f is not None and f_n is not None:
            fa = float(a)
            fb = float(b)
            f_unbounded = False
            # Heuristic check for unboundedness (which implies not Riemann integrable)
            pts = [
                fa, fb, (fa+fb)/2,
                fa + 1e-9*(fb-fa), fb - 1e-9*(fb-fa),
                (fa+fb)/2 + 1e-9*(fb-fa), (fa+fb)/2 - 1e-9*(fb-fa)
            ]
            for pt in pts:
                val = f.subs(wx, pt)
                if val.is_number and float(Abs(val)) > 1e6:
                    f_unbounded = True
                    break
            
            if f_unbounded:
                neg_q_ok = True
            else:
                int_f = integrate(f, (wx, a, b))
                if int_f in [oo, -oo, zoo, nan]:
                    neg_q_ok = True
                elif not int_f.has(sp.Integral):
                    fn_unbounded = False
                    for pt in pts:
                        val = f_n.subs({wx: pt, wn: 100})
                        if val.is_number and float(Abs(val)) > 1e6:
                            fn_unbounded = True
                            break
                    if fn_unbounded:
                        neg_q_ok = True
                    else:
                        int_f_n = integrate(f_n, (wx, a, b))
                        if int_f_n in [oo, -oo, zoo, nan]:
                            neg_q_ok = True
                        elif not int_f_n.has(sp.Integral):
                            lim_int = limit(int_f_n, wn, oo)
                            if not lim_int.has(sp.Limit):
                                if simplify(lim_int - int_f) != 0:
                                    neg_q_ok = True
    except Exception:
        pass
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: interval is closed and bounded",
    "H_2: sequence of functions to reals",
    "H_3: sequence converges uniformly",
    "¬Q: limit function is not Riemann integrable or integrals do not converge"
]

N_HYP = 3
NEG_Q_INDEX = 3