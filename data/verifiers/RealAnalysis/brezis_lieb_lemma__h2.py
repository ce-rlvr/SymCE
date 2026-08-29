import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, n = sympy.symbols('x n')

CONDITION_LABELS = [
    "H_1: (X, \Sigma, \mu) is a measure space",
    "H_2: {f_n} is a sequence in L^p with sup_n ||f_n||_p < \infty",
    "H_3: f_n \to f almost everywhere",
    "¬Q: Conclusion fails"
]
N_HYP = 3
NEG_Q_INDEX = 3

def safe_pow(base, exponent):
    if exponent == float('inf'):
        if base > 1.000001:
            return float('inf')
        elif base < 0.999999:
            return 0.0
        else:
            return 1.0
    try:
        return base ** exponent
    except OverflowError:
        return float('inf')

def compute_integral(expr, p, domain_vals, is_interval):
    if is_interval:
        a, b = domain_vals
        N_pts = 200
        dx = (b - a) / N_pts
        integral = 0.0
        for i in range(N_pts):
            pt = a + (i + 0.5) * dx
            try:
                val = abs(complex(expr.subs(x, pt)))
            except TypeError:
                val = float(abs(expr.subs(x, pt)))
            integral += safe_pow(val, p) * dx
        return integral
    else:
        integral = 0.0
        for pt in domain_vals:
            try:
                val = abs(complex(expr.subs(x, pt)))
            except TypeError:
                val = float(abs(expr.subs(x, pt)))
            integral += safe_pow(val, p)
        return integral

def compute_norm(expr, p, domain_vals, is_interval):
    if p == float('inf'):
        max_val = 0.0
        if is_interval:
            a, b = domain_vals
            N_pts = 200
            dx = (b - a) / N_pts
            for i in range(N_pts):
                pt = a + (i + 0.5) * dx
                try:
                    val = abs(complex(expr.subs(x, pt)))
                except TypeError:
                    val = float(abs(expr.subs(x, pt)))
                if val > max_val:
                    max_val = val
        else:
            for pt in domain_vals:
                try:
                    val = abs(complex(expr.subs(x, pt)))
                except TypeError:
                    val = float(abs(expr.subs(x, pt)))
                if val > max_val:
                    max_val = val
        return max_val
    else:
        integral = compute_integral(expr, p, domain_vals, is_interval)
        try:
            return integral ** (1.0 / p)
        except OverflowError:
            return float('inf')
        except ZeroDivisionError:
            return float('inf')

def conditions(witness):
    try:
        f_n_expr = sympy.sympify(witness['f_n'])
        f_expr = sympy.sympify(witness['f'])
        p_val = witness['p']
        if p_val == sympy.oo or str(p_val) == 'inf':
            p = float('inf')
        else:
            p = float(p_val)
            
        domain = witness['domain']
        if isinstance(domain, tuple) and len(domain) == 2:
            a, b = domain[0], domain[1]
            if a == -sympy.oo:
                a = -100.0
            else:
                a = float(a)
            if b == sympy.oo:
                b = 100.0
            else:
                b = float(b)
            domain_vals = (a, b)
            is_interval = True
        elif isinstance(domain, list):
            domain_vals = [float(pt) for pt in domain]
            is_interval = False
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: Measure space
    h1 = False
    try:
        if is_interval:
            if domain_vals[0] < domain_vals[1]:
                h1 = True
        else:
            if len(domain_vals) > 0:
                h1 = True
    except Exception:
        h1 = False

    # H2: sup_n ||f_n||_p < oo
    h2 = False
    try:
        norms = []
        for n_val in [1, 10, 50, 100]:
            fn_n = f_n_expr.subs(n, n_val)
            norm = compute_norm(fn_n, p, domain_vals, is_interval)
            norms.append(norm)
        if max(norms) < 1e5:
            # Check for unbounded growth
            if norms[-1] > norms[0] + 5 and norms[-1] > norms[-2] * 1.1:
                h2 = False
            elif norms[-1] > norms[0] * 3 and norms[-1] > 2.0:
                h2 = False
            else:
                h2 = True
    except Exception:
        h2 = False

    # H3: f_n -> f a.e.
    h3 = False
    try:
        max_diff = 0.0
        if is_interval:
            a, b = domain_vals
            N_pts = 50
            dx = (b - a) / N_pts
            pts = [a + (i + 0.5) * dx for i in range(N_pts)]
        else:
            pts = domain_vals
            
        for pt in pts:
            try:
                f_val = complex(f_expr.subs(x, pt))
                fn_val = complex(f_n_expr.subs({n: 1000, x: pt}))
            except TypeError:
                f_val = float(f_expr.subs(x, pt))
                fn_val = float(f_n_expr.subs({n: 1000, x: pt}))
            diff = abs(fn_val - f_val)
            if diff > max_diff:
                max_diff = diff
        if max_diff < 0.2:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: conclusion fails
    neg_q = False
    try:
        int_f_p = compute_integral(f_expr, p, domain_vals, is_interval)
        if math.isinf(int_f_p) or int_f_p > 1e5:
            # f not in L^p, conclusion fails
            neg_q = True
        else:
            n_val = 200
            fn_n = f_n_expr.subs(n, n_val)
            
            int_fn_p = compute_integral(fn_n, p, domain_vals, is_interval)
            
            diff_expr = fn_n - f_expr
            int_diff_p = compute_integral(diff_expr, p, domain_vals, is_interval)
            
            if math.isinf(int_fn_p) and math.isinf(int_diff_p):
                # inf - inf is undefined, conclusion fails
                neg_q = True
            elif math.isinf(int_fn_p) or math.isinf(int_diff_p):
                neg_q = True
            else:
                lhs = int_fn_p - int_diff_p
                rhs = int_f_p
                if abs(lhs - rhs) > 0.1:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]