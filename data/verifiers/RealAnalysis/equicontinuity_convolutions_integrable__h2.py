import sympy as sp
import math

x, y, n = sp.symbols('x y n', real=True)

def get_val(witness, key):
    if isinstance(witness, dict):
        return witness.get(key)
    return getattr(witness, key, None)

def conditions(witness) -> list[bool]:
    try:
        g_obj = get_val(witness, 'g')
        f_obj = get_val(witness, 'f')
        h_obj = get_val(witness, 'h')
        M = float(get_val(witness, 'M'))
        x_n_obj = get_val(witness, 'x_n')
        y_n_obj = get_val(witness, 'y_n')
        eps = float(get_val(witness, 'eps'))
    except Exception:
        return [False, False, False, False]

    # H1: g in L1
    try:
        if callable(g_obj):
            total = 0.0
            dx = 0.1
            for i in range(-10000, 10000):
                try:
                    total += abs(g_obj(i * dx)) * dx
                except Exception:
                    pass
            tail_small = True
            try:
                if abs(g_obj(900)) > 1e-2 or abs(g_obj(-900)) > 1e-2:
                    tail_small = False
            except Exception:
                pass
            h1 = (total < 1e5) and tail_small
        else:
            try:
                integ = sp.integrate(sp.Abs(g_obj), (x, -sp.oo, sp.oo))
                if isinstance(integ, sp.Integral):
                    raise ValueError("Unevaluated integral")
                h1 = bool(integ.is_real and integ < sp.oo)
            except Exception:
                total = 0.0
                dx = 0.1
                for i in range(-10000, 10000):
                    try:
                        total += float(sp.Abs(g_obj.subs(x, i * dx))) * dx
                    except Exception:
                        pass
                tail_small = True
                try:
                    if float(sp.Abs(g_obj.subs(x, 900))) > 1e-2 or float(sp.Abs(g_obj.subs(x, -900))) > 1e-2:
                        tail_small = False
                except Exception:
                    pass
                h1 = (total < 1e5) and tail_small
    except Exception:
        h1 = False

    # H2: |f| <= M
    try:
        if callable(f_obj):
            h2 = True
            for n_val in [1, 2, 5, 10]:
                for x_val in [-10, -5, -1, 0, 1, 5, 10]:
                    if abs(f_obj(n_val, x_val)) > M + 1e-6:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            try:
                max_val = sp.calculus.util.maximum(sp.Abs(f_obj), x, sp.Reals)
                h2 = bool(max_val <= M)
            except Exception:
                h2 = True
                for n_val in [1, 2, 5, 10]:
                    f_sub = f_obj.subs(n, n_val)
                    for x_val in [-10, -5, -1, 0, 1, 5, 10]:
                        if float(sp.Abs(f_sub.subs(x, x_val))) > M + 1e-6:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H3: h = f * g
    try:
        if callable(f_obj) and callable(g_obj) and callable(h_obj):
            h3 = True
            for n_val in [1, 2]:
                for x_val in [0, 1]:
                    total = 0.0
                    dy = 0.05
                    for i in range(-2000, 2000):
                        y_val = i * dy
                        try:
                            total += f_obj(n_val, y_val) * g_obj(x_val - y_val) * dy
                        except Exception:
                            pass
                    expected = h_obj(n_val, x_val)
                    if abs(total - expected) > 0.1 * max(1.0, abs(expected)):
                        h3 = False
                        break
                if not h3:
                    break
        else:
            y_sym = sp.Symbol('y', real=True)
            integrand = f_obj.subs(x, y_sym) * g_obj.subs(x, x - y_sym)
            try:
                conv = sp.integrate(integrand, (y_sym, -sp.oo, sp.oo))
                if isinstance(conv, sp.Integral):
                    raise ValueError("Unevaluated integral")
                h3 = bool(sp.simplify(conv - h_obj) == 0)
            except Exception:
                h3 = True
                for n_val in [1, 2]:
                    for x_val in [0, 1]:
                        total = 0.0
                        dy = 0.05
                        for i in range(-2000, 2000):
                            y_val = i * dy
                            try:
                                f_val = float(f_obj.subs({n: n_val, x: y_val}))
                                g_val = float(g_obj.subs(x, x_val - y_val))
                                total += f_val * g_val * dy
                            except Exception:
                                pass
                        expected = float(h_obj.subs({n: n_val, x: x_val}))
                        if abs(total - expected) > 0.1 * max(1.0, abs(expected)):
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: not uniformly equicontinuous
    try:
        if eps <= 0:
            neg_q = False
        else:
            if callable(x_n_obj) and callable(y_n_obj) and callable(h_obj):
                x_val = x_n_obj(10000)
                y_val = y_n_obj(10000)
                if abs(x_val - y_val) > 1e-2:
                    neg_q = False
                else:
                    neg_q = True
                    for n_val in [100, 1000, 10000]:
                        x_v = x_n_obj(n_val)
                        y_v = y_n_obj(n_val)
                        h_diff = abs(h_obj(n_val, x_v) - h_obj(n_val, y_v))
                        if h_diff < eps - 1e-5:
                            neg_q = False
                            break
            else:
                try:
                    diff_limit = sp.limit(sp.Abs(x_n_obj - y_n_obj), n, sp.oo)
                    if diff_limit != 0:
                        neg_q = False
                    else:
                        h_diff = sp.Abs(h_obj.subs(x, x_n_obj) - h_obj.subs(x, y_n_obj))
                        h_diff_limit = sp.limit(h_diff, n, sp.oo)
                        neg_q = bool(h_diff_limit >= eps)
                except Exception:
                    x_val = float(x_n_obj.subs(n, 10000))
                    y_val = float(y_n_obj.subs(n, 10000))
                    if abs(x_val - y_val) > 1e-2:
                        neg_q = False
                    else:
                        neg_q = True
                        for n_val in [100, 1000, 10000]:
                            try:
                                val = float(sp.Abs(h_obj.subs(x, x_n_obj).subs(n, n_val) - h_obj.subs(x, y_n_obj).subs(n, n_val)))
                                if val < eps - 1e-5:
                                    neg_q = False
                                    break
                            except Exception:
                                neg_q = False
                                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: g is a fixed Lebesgue integrable function on R",
    "H_2: F is uniformly bounded by M",
    "H_3: H is the family of convolution functions h = f * g",
    "¬Q: H is not uniformly equicontinuous on R"
]

N_HYP = 3
NEG_Q_INDEX = 3