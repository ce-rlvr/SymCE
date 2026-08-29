import sympy as sp
import math

# Top-level setup
x, y, n = sp.symbols('x y n', real=True)

def num_integrate_inf(func, steps=20000):
    """
    Numerically integrates func(y) from -infinity to infinity
    using the substitution y = tan(t).
    """
    dt = math.pi / steps
    total = 0.0
    for i in range(steps):
        t = -math.pi/2 + (i + 0.5) * dt
        y_val = math.tan(t)
        dy_dt = 1.0 / (math.cos(t)**2)
        try:
            v = func(y_val)
            if isinstance(v, complex):
                v = v.real
            total += float(v) * dy_dt
        except Exception:
            pass
    return total * dt

def conditions(witness):
    """
    witness: tuple (f_expr, K_expr)
    f_expr: sympy expression in x
    K_expr: sympy expression in x and n
    """
    try:
        f_expr, K_expr = witness
    except Exception:
        return [False, False, False, False]
        
    # Provide a mapping for Heaviside to support piecewise definitions
    modules = [{'Heaviside': lambda val: 1.0 if val >= 0 else 0.0}, 'math']
    
    # H1: f is bounded and uniformly continuous
    h1 = False
    try:
        f_diff = sp.diff(f_expr, x)
        f_lam = sp.lambdify(x, f_expr, modules)
        fd_lam = sp.lambdify(x, f_diff, modules)
        
        bounded = True
        # Check large values for asymptotic boundedness and uniform continuity
        for xv in [1e4, 1e4+0.1, 1e4+0.2, -1e4, -1e4-0.1, 1e5, -1e5]:
            if abs(f_lam(xv)) > 1e3 or abs(fd_lam(xv)) > 5000:
                bounded = False
                break
        
        # Check grid for local blowups and derivative bound
        if bounded:
            for val in range(-1000, 1000):
                xv = val / 10.0
                if abs(f_lam(xv)) > 1e3 or abs(fd_lam(xv)) > 5000:
                    bounded = False
                    break
        h1 = bounded
    except Exception:
        h1 = False

    # H2: K_n >= 0
    h2 = False
    try:
        K_lam = sp.lambdify((x, n), K_expr, modules)
        non_negative = True
        for nv in [1, 2, 3]:
            for val in range(-1000, 1000):
                xv = val / 10.0
                if K_lam(xv, nv) < -1e-5:
                    non_negative = False
                    break
            if not non_negative:
                break
        h2 = non_negative
    except Exception:
        h2 = False

    # H3: Integral of K_n is 1
    h3 = False
    try:
        integral_ok = True
        for nv in [1, 2, 3]:
            def integrand_h3(y_val):
                return K_lam(y_val, nv)
            val = num_integrate_inf(integrand_h3, steps=20000)
            if abs(val - 1.0) > 1e-2:
                integral_ok = False
                break
        h3 = integral_ok
    except Exception:
        h3 = False

    # neg_Q: f_n does not converge uniformly to f
    neg_q = False
    try:
        non_convergent = True
        # Check for sufficiently large n to see if the difference remains large
        for nv in [10, 20]:
            diff_large_for_n = False
            for xv in [0.0, 1.0, 1.570796, 3.14159, 2.0, -1.0, -1.570796, 4.0, 5.0]:
                def integrand_q(y_val):
                    return f_lam(xv - y_val) * K_lam(y_val, nv)
                val = num_integrate_inf(integrand_q, steps=20000)
                f_val = f_lam(xv)
                if abs(val - f_val) > 0.15:
                    diff_large_for_n = True
                    break
            if not diff_large_for_n:
                non_convergent = False
                break
        neg_q = non_convergent
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is bounded and uniformly continuous",
    "H_2: K_n is non-negative",
    "H_3: Integral of K_n is 1",
    "¬Q: f_n does not converge uniformly to f"
]

N_HYP = 3
NEG_Q_INDEX = 3