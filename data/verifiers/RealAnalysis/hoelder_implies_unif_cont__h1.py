import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)
Reals = sp.S.Reals

def conditions(witness):
    """
    witness can be a tuple: (f_expr, domain, C, alpha) or (f_expr, domain)
    where f_expr is a sympy expression in terms of x,
    domain is a sympy Set (e.g., sp.S.Reals, sp.Interval(0, 1)),
    C is a positive float, and alpha is a float in (0, 1].
    """
    if isinstance(witness, tuple):
        if len(witness) == 4:
            f_expr, domain, C, alpha = witness
        elif len(witness) == 2:
            f_expr, domain = witness
            C, alpha = None, None
        else:
            return [False, False]
    else:
        return [False, False]

    # H_1: Holder continuous
    h1_ok = False
    try:
        if C is not None and alpha is not None:
            if C > 0 and 0 < alpha <= 1:
                f_lam = sp.lambdify(x, f_expr, modules=['math', 'sympy'])
                test_points = [i * 0.5 for i in range(-100, 101)] + [i * 0.1 for i in range(-10, 11)]
                if domain.sup == sp.oo or domain.inf == -sp.oo:
                    test_points += [-1e6, -1e6+1, -1e5, -1e5+1, 1e5, 1e5-1, 1e6, 1e6-1]
                test_points = list(set(test_points))
                test_points.sort()
                
                points = []
                for p in test_points:
                    try:
                        if domain.contains(p) == sp.S.true or domain.contains(p) == True:
                            points.append(p)
                    except Exception:
                        pass
                
                if len(points) > 100:
                    step = len(points) / 100.0
                    points = [points[int(i * step)] for i in range(100)]
                    
                valid = True
                for p1 in points:
                    for p2 in points:
                        if p1 == p2:
                            continue
                        try:
                            val1 = float(f_lam(p1))
                            val2 = float(f_lam(p2))
                            if abs(val1 - val2) > C * (abs(p1 - p2)**float(alpha)) + 1e-5:
                                valid = False
                                break
                        except Exception:
                            pass
                    if not valid:
                        break
                h1_ok = valid
        else:
            # Estimate if C and alpha are not provided
            f_lam = sp.lambdify(x, f_expr, modules=['math', 'sympy'])
            test_points = [i * 0.5 for i in range(-100, 101)] + [i * 0.1 for i in range(-10, 11)]
            if domain.sup == sp.oo or domain.inf == -sp.oo:
                test_points += [-1e6, -1e6+1, -1e5, -1e5+1, 1e5, 1e5-1, 1e6, 1e6-1]
            test_points = list(set(test_points))
            test_points.sort()
            
            points = []
            for p in test_points:
                try:
                    if domain.contains(p) == sp.S.true or domain.contains(p) == True:
                        points.append(p)
                except Exception:
                    pass
            
            if len(points) > 100:
                step = len(points) / 100.0
                points = [points[int(i * step)] for i in range(100)]
                
            for test_alpha in [1.0, 0.5, 0.1]:
                max_C = 0
                valid = True
                for p1 in points:
                    for p2 in points:
                        if p1 == p2:
                            continue
                        try:
                            val1 = float(f_lam(p1))
                            val2 = float(f_lam(p2))
                            diff = abs(val1 - val2)
                            dist = abs(p1 - p2)**test_alpha
                            if dist == 0:
                                continue
                            C_est = diff / dist
                            if C_est > max_C:
                                max_C = C_est
                            if max_C > 1e6:
                                valid = False
                                break
                        except Exception:
                            pass
                    if not valid:
                        break
                if valid and max_C <= 1e6:
                    h1_ok = True
                    break
    except Exception:
        h1_ok = False

    # neg_Q: NOT uniformly continuous
    neg_q_ok = False
    try:
        # 1. Internal singularities
        try:
            singularities = sp.singularities(f_expr, x)
            if isinstance(singularities, sp.Set):
                intersection = domain.intersect(singularities)
                if not intersection.is_empty:
                    neg_q_ok = True
        except Exception:
            pass

        if not neg_q_ok:
            # 2. Open boundaries limits
            try:
                if isinstance(domain, sp.Interval):
                    if domain.left_open and domain.start != -sp.oo:
                        lim = sp.limit(f_expr, x, domain.start, dir='+')
                        if lim in [sp.oo, -sp.oo, sp.zoo] or isinstance(lim, sp.AccumBounds):
                            neg_q_ok = True
                    if domain.right_open and domain.end != sp.oo:
                        lim = sp.limit(f_expr, x, domain.end, dir='-')
                        if lim in [sp.oo, -sp.oo, sp.zoo] or isinstance(lim, sp.AccumBounds):
                            neg_q_ok = True
            except Exception:
                pass

        if not neg_q_ok:
            # 3. Infinity growth
            def check_infinity_growth(domain_dir):
                try:
                    f_lam = sp.lambdify(x, f_expr, modules=['math', 'sympy'])
                    pts = []
                    base_pts = [10.0, 50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0, 50000.0, 100000.0]
                    for p in base_pts:
                        pts.append(p if domain_dir == 1 else -p)
                    
                    delta = 0.01
                    diffs = []
                    for x_val in pts:
                        if domain.contains(x_val) == sp.S.true or domain.contains(x_val) == True:
                            y_val = x_val + (delta if domain_dir == 1 else -delta)
                            if domain.contains(y_val) == sp.S.true or domain.contains(y_val) == True:
                                diffs.append(abs(float(f_lam(x_val)) - float(f_lam(y_val))))
                    if len(diffs) >= 3:
                        if max(diffs) > 0.5 and (max(diffs) - min(diffs)) > 0.2:
                            return True
                except Exception:
                    pass
                return False

            try:
                if domain.sup == sp.oo:
                    if check_infinity_growth(1):
                        neg_q_ok = True
                if domain.inf == -sp.oo and not neg_q_ok:
                    if check_infinity_growth(-1):
                        neg_q_ok = True
            except Exception:
                pass

        if not neg_q_ok:
            # 4. Oscillation near open boundaries
            try:
                if isinstance(domain, sp.Interval):
                    f_lam = sp.lambdify(x, f_expr, modules=['math', 'sympy'])
                    if domain.left_open and domain.start != -sp.oo:
                        vals = []
                        for i in range(1, 20):
                            pt = float(domain.start) + 10**(-i)
                            if domain.contains(pt) == sp.S.true or domain.contains(pt) == True:
                                vals.append(float(f_lam(pt)))
                        if len(vals) > 5:
                            diffs = [abs(vals[i] - vals[i-1]) for i in range(1, len(vals))]
                            if max(diffs) > 0.5:
                                neg_q_ok = True
                    if not neg_q_ok and domain.right_open and domain.end != sp.oo:
                        vals = []
                        for i in range(1, 20):
                            pt = float(domain.end) - 10**(-i)
                            if domain.contains(pt) == sp.S.true or domain.contains(pt) == True:
                                vals.append(float(f_lam(pt)))
                        if len(vals) > 5:
                            diffs = [abs(vals[i] - vals[i-1]) for i in range(1, len(vals))]
                            if max(diffs) > 0.5:
                                neg_q_ok = True
            except Exception:
                pass
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exist constants C > 0 and 0 < alpha <= 1 such that |f(x) - f(y)| <= C|x - y|^alpha",
    "not Q: f is not uniformly continuous on D"
]

N_HYP = 1
NEG_Q_INDEX = 1