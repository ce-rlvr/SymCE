import sympy as sp
import math

x, y, n = sp.symbols('x y n', real=True)

def conditions(witness) -> list[bool]:
    try:
        a = float(witness["a"])
        b = float(witness["b"])
        K = sp.sympify(witness["K"])
        f = sp.sympify(witness["f"])
        M = float(witness["M"])
        g = sp.sympify(witness["g"])
        epsilon = float(witness["epsilon"])
        x1 = sp.sympify(witness["x1"])
        x2 = sp.sympify(witness["x2"])
    except Exception:
        return [False, False, False, False]

    h1_ok = True
    try:
        for x_val in [a, a + 0.5 * (b - a), b]:
            for y_val in [a, a + 0.5 * (b - a), b]:
                val = float(sp.re(K.subs({x: x_val, y: y_val}).evalf()))
                if math.isnan(val) or math.isinf(val):
                    h1_ok = False
    except Exception:
        h1_ok = False

    h2_ok = True
    try:
        for n_val in [1, 5]:
            for y_val in [a, a + 0.5 * (b - a), b]:
                val = float(sp.re(f.subs({n: n_val, y: y_val}).evalf()))
                if math.isnan(val) or math.isinf(val):
                    h2_ok = False
    except Exception:
        h2_ok = False

    h3_ok = True
    try:
        for n_val in [10, 50]:
            f_sub = f.subs(n, n_val)
            integral = float(sp.re(sp.Integral(sp.Abs(f_sub), (y, a, b)).evalf()))
            if math.isnan(integral) or math.isinf(integral) or integral > M + 1e-3:
                h3_ok = False
    except Exception:
        h3_ok = False

    neg_q_ok = False
    try:
        is_V = True
        is_F = True
        for n_val, x_val in [(5, a + 0.3 * (b - a)), (7, a + 0.7 * (b - a))]:
            K_sub = K.subs(x, x_val)
            f_sub = f.subs(n, n_val)
            integrand = K_sub * f_sub
            
            V_int = float(sp.re(sp.Integral(integrand, (y, a, x_val)).evalf()))
            F_int = float(sp.re(sp.Integral(integrand, (y, a, b)).evalf()))
            g_val = float(sp.re(g.subs({n: n_val, x: x_val}).evalf()))
            
            if math.isnan(V_int) or math.isnan(g_val) or abs(V_int - g_val) > 1e-2:
                is_V = False
            if math.isnan(F_int) or math.isnan(g_val) or abs(F_int - g_val) > 1e-2:
                is_F = False
                
        g_is_valid = is_V or is_F
        
        if g_is_valid:
            for n_test in [10, 100, 1000, 10000]:
                x1_test = float(sp.re(x1.subs(n, n_test).evalf()))
                x2_test = float(sp.re(x2.subs(n, n_test).evalf()))
                
                if a - 1e-5 <= x1_test <= b + 1e-5 and a - 1e-5 <= x2_test <= b + 1e-5:
                    if abs(x1_test - x2_test) < 1e-2:
                        g1 = float(sp.re(g.subs({n: n_test, x: x1_test}).evalf()))
                        g2 = float(sp.re(g.subs({n: n_test, x: x2_test}).evalf()))
                        if not math.isnan(g1) and not math.isnan(g2):
                            if abs(g1 - g2) >= epsilon - 1e-3:
                                neg_q_ok = True
                                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: K is a continuous real-valued function", "H_2: F is a family of Riemann integrable functions", "H_3: There exists M > 0 such that integral of abs f is bounded by M", "¬Q: The family of functions is not uniformly equicontinuous"]
N_HYP = 3
NEG_Q_INDEX = 3