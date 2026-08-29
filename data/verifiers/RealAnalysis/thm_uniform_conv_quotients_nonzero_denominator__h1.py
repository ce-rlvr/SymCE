import sympy as sp
import math

# Top-level setup for witness expressions
x, n = sp.symbols('x n', real=True)

CONDITION_LABELS = [
    "H_1: (f_n) converges uniformly to a function f on X",
    "H_2: g is a real-valued function on X such that there exists a constant \\delta > 0 with |g(x)| \\ge \\delta for all x \\in X",
    "¬Q: The sequence of quotients f_n(x)/g(x) does NOT converge uniformly to f(x)/g(x) on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract witness components
        if isinstance(witness, dict):
            f_n_obj = witness.get('f_n', 0)
            f_obj = witness.get('f', 0)
            g_obj = witness.get('g', 1)
            domain = witness.get('domain', 'R')
            delta = witness.get('delta', 0.1)
        else:
            f_n_obj, f_obj, g_obj, domain, delta = witness

        # Convert to callables
        if hasattr(f_n_obj, 'subs'):
            f_n = sp.lambdify((n, x), f_n_obj, 'math')
        else:
            f_n = f_n_obj
            
        if hasattr(f_obj, 'subs'):
            f = sp.lambdify(x, f_obj, 'math')
        else:
            f = f_obj
            
        if hasattr(g_obj, 'subs'):
            g = sp.lambdify(x, g_obj, 'math')
        else:
            g = g_obj

        # Generate grid for domain X
        grid = []
        is_unbounded_R = False
        is_unbounded_Rplus = False
        is_unbounded_Rminus = False
        is_finite_interval = False
        a, b = 0.0, 0.0
        start_val = 0.0
        end_val = 0.0

        if str(domain) == 'R' or domain == sp.S.Reals:
            is_unbounded_R = True
            for i in range(-999, 1000):
                t = i / 1000.0
                grid.append(t / (1 - abs(t)))
        elif str(domain) == 'R+' or domain == sp.Interval(0, sp.oo):
            is_unbounded_Rplus = True
            start_val = 0.0
            for i in range(0, 1000):
                t = i / 1000.0
                grid.append(t / (1 - t))
        elif isinstance(domain, tuple):
            a, b = float(domain[0]), float(domain[1])
            is_finite_interval = True
            for i in range(0, 1001):
                grid.append(a + (b - a) * i / 1000.0)
        elif hasattr(domain, 'is_Interval') and domain.is_Interval:
            if domain.end == sp.oo and domain.start == -sp.oo:
                is_unbounded_R = True
                for i in range(-999, 1000):
                    t = i / 1000.0
                    grid.append(t / (1 - abs(t)))
            elif domain.end == sp.oo:
                is_unbounded_Rplus = True
                start_val = float(domain.start)
                for i in range(0, 1000):
                    t = i / 1000.0
                    grid.append(start_val + t / (1 - t))
            elif domain.start == -sp.oo:
                is_unbounded_Rminus = True
                end_val = float(domain.end)
                for i in range(0, 1000):
                    t = i / 1000.0
                    grid.append(end_val - t / (1 - t))
            else:
                a, b = float(domain.start), float(domain.end)
                is_finite_interval = True
                for i in range(0, 1001):
                    grid.append(a + (b - a) * i / 1000.0)
        else:
            grid = list(domain)

        if not grid and not is_unbounded_R and not is_unbounded_Rplus and not is_unbounded_Rminus and not is_finite_interval:
            return [False, False, False]

        def get_dynamic_points(nv):
            dp = []
            if is_unbounded_R:
                dp.extend([nv, -nv, nv**2, -nv**2, math.sqrt(nv), -math.sqrt(nv)])
            elif is_unbounded_Rplus:
                dp.extend([start_val + nv, start_val + nv**2, start_val + math.sqrt(nv), start_val + 1/nv, start_val + 1/(nv**2)])
            elif is_unbounded_Rminus:
                dp.extend([end_val - nv, end_val - nv**2, end_val - math.sqrt(nv), end_val - 1/nv, end_val - 1/(nv**2)])
            elif is_finite_interval:
                for p in [a + 1/nv, b - 1/nv, a + 1/(nv**2), b - 1/(nv**2)]:
                    if a <= p <= b:
                        dp.append(p)
            return dp

        n_values = [10, 100, 1000, 10000, 100000, 1000000]
        
        all_points = set(grid)
        for nv in n_values:
            all_points.update(get_dynamic_points(nv))

        # Check H2: |g(x)| >= delta > 0
        if delta <= 0:
            h2 = False
        else:
            h2 = True
            evaluated_any = False
            for xv in all_points:
                try:
                    g_val = g(xv) if callable(g) else g
                    if abs(g_val) < delta - 1e-7:
                        h2 = False
                        break
                    evaluated_any = True
                except OverflowError:
                    evaluated_any = True
                except ZeroDivisionError:
                    h2 = False
                    break
                except Exception:
                    h2 = False
                    break
            if not evaluated_any:
                h2 = False

        # Check H1: f_n converges uniformly to f
        max_diffs_h1 = []
        for nv in n_values:
            md = -1
            current_grid = grid + get_dynamic_points(nv)
            for xv in current_grid:
                try:
                    fn_val = f_n(nv, xv) if callable(f_n) else f_n
                    f_val = f(xv) if callable(f) else f
                    val = abs(fn_val - f_val)
                    if val > md: md = val
                except OverflowError:
                    md = float('inf')
                except ZeroDivisionError:
                    md = float('inf')
                except Exception:
                    pass
            if md == -1:
                return [False, False, False]
            max_diffs_h1.append(md)
            
        h1 = (max_diffs_h1[-1] < 1e-2) and (max_diffs_h1[-1] <= max_diffs_h1[-2] + 1e-7)

        # Check neg_Q: f_n/g does NOT converge uniformly to f/g
        max_diffs_q = []
        for nv in n_values:
            md = -1
            current_grid = grid + get_dynamic_points(nv)
            for xv in current_grid:
                try:
                    fn_val = f_n(nv, xv) if callable(f_n) else f_n
                    f_val = f(xv) if callable(f) else f
                    g_val = g(xv) if callable(g) else g
                    val = abs(fn_val/g_val - f_val/g_val)
                    if val > md: md = val
                except OverflowError:
                    md = float('inf')
                except ZeroDivisionError:
                    md = float('inf')
                except Exception:
                    pass
            if md == -1:
                return [False, False, False]
            max_diffs_q.append(md)
            
        neg_q = (max_diffs_q[-1] > 1e-2) or (max_diffs_q[-1] > max_diffs_q[-2] + 1e-7)

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]