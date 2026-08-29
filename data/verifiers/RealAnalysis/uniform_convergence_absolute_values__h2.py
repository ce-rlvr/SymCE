import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x', real=True)

def get_domain_bounds(domain):
    if domain == sympy.S.Reals:
        return -float('inf'), float('inf')
    if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
        return float(domain.inf), float(domain.sup)
    elif hasattr(domain, 'start') and hasattr(domain, 'end'):
        return float(domain.start), float(domain.end)
    elif isinstance(domain, (list, tuple)) and len(domain) == 2:
        return float(domain[0]), float(domain[1])
    else:
        raise ValueError("Unknown domain format")

def eval_fn(f_n, n_val, x_val):
    if hasattr(f_n, 'subs'):
        val = f_n.subs({n: n_val, x: x_val}).evalf()
        if not val.is_real:
            raise ValueError("Not real")
        return float(val)
    else:
        return float(f_n(n_val, x_val))

def eval_f(f, x_val):
    if hasattr(f, 'subs'):
        val = f.subs(x, x_val).evalf()
        if not val.is_real:
            raise ValueError("Not real")
        return float(val)
    else:
        return float(f(x_val))

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        if len(witness) == 3:
            f_n_obj, f_obj, domain = witness
            a, b = get_domain_bounds(domain)
        elif len(witness) == 2:
            f_n_obj, domain = witness
            a, b = get_domain_bounds(domain)
            
            if a > -float('inf') and b < float('inf'):
                test_pt = (a + b) / 2
            else:
                test_pt = 0.0 if a <= 0 <= b else (a + 1 if a > -float('inf') else b - 1)
                
            if hasattr(f_n_obj, 'subs'):
                try:
                    f_obj = sympy.limit(f_n_obj, n, sympy.oo)
                    # Test if the limit is evaluable to a real number
                    eval_f(f_obj, test_pt)
                except Exception:
                    f_obj = lambda x_val: eval_fn(f_n_obj, 100000, x_val)
            else:
                f_obj = lambda x_val: eval_fn(f_n_obj, 100000, x_val)
        else:
            return [False, False]
            
        # Check H1: (f_n) is a sequence of real-valued functions on S
        test_n = [1, 2, 5]
        test_x = []
        if a > -float('inf') and b < float('inf'):
            test_x = [a + 0.1*(b-a), (a+b)/2, b - 0.1*(b-a)]
        else:
            test_x = [0, 1, -1, 10, -10]
            test_x = [xv for xv in test_x if a <= xv <= b]
            if not test_x:
                test_x = [a + 1] if a > -float('inf') else [b - 1]
                
        h1_ok = True
        for n_val in test_n:
            for x_val in test_x:
                try:
                    val = eval_fn(f_n_obj, n_val, x_val)
                    if math.isnan(val) or math.isinf(val):
                        h1_ok = False
                        break
                except Exception:
                    h1_ok = False
                    break
            if not h1_ok:
                break
                
        # Check neg_Q: (|f_n|) does NOT converge uniformly to |f| on S
        f_n_fast = None
        f_fast = None
        if hasattr(f_n_obj, 'subs'):
            try:
                f_n_fast = sympy.lambdify((n, x), f_n_obj, modules=['math', 'sympy'])
            except Exception:
                pass
        if hasattr(f_obj, 'subs'):
            try:
                f_fast = sympy.lambdify(x, f_obj, modules=['math', 'sympy'])
            except Exception:
                pass

        def fast_eval_fn(n_val, x_val):
            if f_n_fast:
                return float(f_n_fast(n_val, x_val))
            return eval_fn(f_n_obj, n_val, x_val)

        def fast_eval_f(x_val):
            if f_fast:
                return float(f_fast(x_val))
            return eval_f(f_obj, x_val)

        def get_points(n_val):
            pts = set()
            if a > -float('inf') and b < float('inf'):
                for i in range(1001):
                    pts.add(a + i * (b - a) / 1000)
                for k in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
                    if a + k <= b: pts.add(a + k)
                    if b - k >= a: pts.add(b - k)
                for p in [1/n_val, 1/(n_val**2), 1/math.sqrt(n_val)]:
                    if a <= a + p <= b: pts.add(a + p)
                    if a <= b - p <= b: pts.add(b - p)
            else:
                for i in range(-1000, 1001):
                    if a <= i <= b:
                        pts.add(float(i))
                for p in [n_val, n_val/2, 2*n_val, n_val**2, math.sqrt(n_val)]:
                    if a <= p <= b:
                        pts.add(float(p))
                    if a <= -p <= b:
                        pts.add(float(-p))
                for p in [1/n_val, 1/(n_val**2), 1/math.sqrt(n_val)]:
                    if a <= p <= b: pts.add(float(p))
                    if a <= -p <= b: pts.add(float(-p))
            return list(pts)

        max_diffs = []
        for n_val in [10, 100, 1000, 10000, 100000]:
            pts = get_points(n_val)
            current_max = 0
            for x_val in pts:
                try:
                    val_fn = fast_eval_fn(n_val, x_val)
                    val_f = fast_eval_f(x_val)
                    diff = abs(abs(val_fn) - abs(val_f))
                    if diff > current_max:
                        current_max = diff
                except Exception:
                    pass
            max_diffs.append(current_max)
            
        if len(max_diffs) > 0 and max_diffs[-1] > 1e-3:
            neg_q_ok = True
            
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions on a set S",
    "¬Q: The sequence of functions (|f_n|) does NOT converge uniformly to |f| on S"
]

N_HYP = 1
NEG_Q_INDEX = 1