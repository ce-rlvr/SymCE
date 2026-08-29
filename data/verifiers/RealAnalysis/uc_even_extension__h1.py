import sympy
import math

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    # H_1: g is the even extension of f
    h1_ok = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, g = witness
        else:
            f = None
            g = witness

        # Check if g is defined on R (at least at some test points including 0)
        defined_everywhere = True
        test_points = [0.123, -0.345, 0.0, 0.567, -0.789]
        for val in test_points:
            try:
                res = float(g.subs(x, val))
                if math.isnan(res) or math.isinf(res):
                    defined_everywhere = False
                    break
            except Exception:
                defined_everywhere = False
                break
        
        if defined_everywhere:
            if f is not None:
                diff = sympy.simplify(g - f.subs(x, sympy.Abs(x)))
                if diff == 0:
                    h1_ok = True
                else:
                    match = True
                    for val in test_points:
                        gv = float(g.subs(x, val))
                        fv = float(f.subs(x, abs(val)))
                        if abs(gv - fv) > 1e-7:
                            match = False
                            break
                    h1_ok = match
            else:
                diff = sympy.simplify(g - g.subs(x, -x))
                if diff == 0:
                    h1_ok = True
                else:
                    match = True
                    for val in test_points:
                        gv1 = float(g.subs(x, val))
                        gv2 = float(g.subs(x, -val))
                        if abs(gv1 - gv2) > 1e-7:
                            match = False
                            break
                    h1_ok = match
    except Exception:
        h1_ok = False

    # neg_Q: g is not uniformly continuous on R
    neg_q = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            g = witness[1]
        else:
            g = witness

        # 1. Check if not continuous
        try:
            dom = sympy.calculus.util.continuous_domain(g, x, sympy.S.Reals)
            if dom != sympy.S.Reals:
                neg_q = True
        except Exception:
            pass

        # 2. Check polynomial degree
        if not neg_q:
            try:
                p = sympy.Poly(g, x)
                if p.degree() >= 2:
                    neg_q = True
            except Exception:
                pass

        # 3. Check derivative limit
        if not neg_q:
            try:
                deriv = g.diff(x)
                lim = sympy.limit(sympy.Abs(deriv), x, sympy.oo)
                if lim == sympy.oo:
                    neg_q = True
            except Exception:
                pass

        # 4. Numerical check for uniform continuity at infinity
        if not neg_q:
            try:
                diffs = []
                for i in [10, 100, 1000, 10000, 100000]:
                    x_val = float(i)
                    y_val = x_val + 1e-3
                    try:
                        gx = float(g.subs(x, x_val))
                        gy = float(g.subs(x, y_val))
                        diffs.append(abs(gx - gy))
                    except OverflowError:
                        neg_q = True
                        break
                
                if not neg_q:
                    is_growing = False
                    for j in range(len(diffs)):
                        for k in range(j+1, len(diffs)):
                            if diffs[k] > 2 * diffs[j] and diffs[k] > 0.1:
                                is_growing = True
                                break
                    if is_growing:
                        neg_q = True
            except Exception:
                pass

        # 5. Numerical check for unboundedness or oscillation near 0
        if not neg_q:
            try:
                diffs_near_0 = []
                for k in range(1, 6):
                    x_val = 10**(-k)
                    y_val = x_val + 10**(-k-3)
                    try:
                        gx = float(g.subs(x, x_val))
                        gy = float(g.subs(x, y_val))
                        diffs_near_0.append(abs(gx - gy))
                    except OverflowError:
                        neg_q = True
                        break
                
                if not neg_q:
                    is_growing_near_0 = False
                    for j in range(len(diffs_near_0)):
                        for m in range(j+1, len(diffs_near_0)):
                            if diffs_near_0[m] > 2 * diffs_near_0[j] and diffs_near_0[m] > 0.1:
                                is_growing_near_0 = True
                                break
                    if is_growing_near_0:
                        neg_q = True
            except Exception:
                pass

    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: g is the even extension of f",
    "¬Q: g is not uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1