import sympy as sp
import math

# Top-level setup
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f_n is a sequence of bounded real-valued functions on S",
    "H_2: f_n is a Cauchy sequence in B(S) with respect to the supremum norm",
    "¬Q: f_n does not converge uniformly to a bounded function on S"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            expr, domain = witness
        else:
            expr = witness
            domain = sp.Interval(0, 1)
            
        # Generate test points in the domain
        if isinstance(domain, sp.Set):
            try:
                if isinstance(domain, sp.Interval) or domain == sp.S.Reals:
                    if domain == sp.S.Reals:
                        start, end = -10.0, 10.0
                        is_start_fin, is_end_fin = False, False
                    else:
                        start = float(domain.start) if domain.start.is_finite else -10.0
                        end = float(domain.end) if domain.end.is_finite else 10.0
                        is_start_fin = domain.start.is_finite
                        is_end_fin = domain.end.is_finite
                        
                    S_points = [start + i * (end - start) / 100.0 for i in range(101)]
                    S_points += [start + 1e-4, start + 1e-3, end - 1e-3, end - 1e-4]
                    if not is_start_fin:
                        S_points += [-1e6, -1e10]
                    if not is_end_fin:
                        S_points += [1e6, 1e10]
                else:
                    S_points = []
                    try:
                        for p in domain.intersect(sp.Interval(-100, 100)):
                            S_points.append(float(p))
                    except Exception:
                        pass
                    if not S_points:
                        S_points = [0.0, 0.5, 1.0]
            except Exception:
                S_points = [0.0, 0.5, 1.0]
        elif isinstance(domain, (list, tuple)):
            S_points = [float(p) for p in domain]
        else:
            S_points = [0.0, 0.5, 1.0]
            
        # Create callable function
        if callable(expr):
            f = expr
        else:
            f = sp.lambdify((n, x), expr, modules=['math', 'sympy'])
            
        # H1: f_n is bounded and real-valued on S
        h1 = True
        for nv in [1, 5, 10, 50]:
            try:
                vals = []
                for xv in S_points:
                    v = f(nv, xv)
                    if isinstance(v, complex):
                        if abs(v.imag) > 1e-9:
                            h1 = False
                            break
                        v = v.real
                    vals.append(float(v))
                if not h1:
                    break
                if any(math.isnan(v) or math.isinf(v) for v in vals):
                    h1 = False
                    break
                if max(vals) - min(vals) > 1e6:
                    h1 = False
                    break
            except Exception:
                h1 = False
                break
                
        # H2: Cauchy sequence in the supremum norm
        h2 = True
        diffs = []
        for N in [20, 50, 100]:
            max_diff = 0
            for mv in [int(1.5*N), int(1.5*N)+1, 2*N, 2*N+1, 3*N, 3*N+1]:
                try:
                    diff = max(abs(complex(f(N, xv)) - complex(f(mv, xv))) for xv in S_points)
                    if diff > max_diff:
                        max_diff = diff
                except Exception:
                    h2 = False
                    break
            if not h2:
                break
            diffs.append(max_diff)
        if h2 and diffs[-1] > 0.05:
            h2 = False
            
        # Neg Q: does not converge uniformly to a bounded function
        neg_q = False
        limit_f = []
        try:
            for xv in S_points:
                v = f(1000, xv)
                if isinstance(v, complex):
                    v = v.real
                limit_f.append(float(v))
                
            if any(math.isnan(v) or math.isinf(v) for v in limit_f):
                neg_q = True
            elif max(limit_f) - min(limit_f) > 1e6:
                neg_q = True
            else:
                sup_diffs = []
                for nv in [50, 100, 200]:
                    sup_diff = max(abs(complex(f(nv, xv)) - complex(limit_f[i])) for i, xv in enumerate(S_points))
                    sup_diffs.append(sup_diff)
                if sup_diffs[-1] > 0.05:
                    neg_q = True
        except Exception:
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]