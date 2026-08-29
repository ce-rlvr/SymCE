import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

def check_in_domain(val, domain):
    if domain == sp.S.Reals:
        return True
    try:
        if isinstance(domain, sp.Set):
            return bool(domain.contains(val))
        elif isinstance(domain, (list, tuple)) and len(domain) == 2:
            a, b = domain
            a_val = float(a) if a != -sp.oo else -float('inf')
            b_val = float(b) if b != sp.oo else float('inf')
            return a_val <= float(val) <= b_val
    except Exception:
        pass
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n = witness['f_n']
            f = witness['f']
            g_n = witness['g_n']
            g = witness['g']
            domain = witness.get('domain', sp.S.Reals)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                f_n, f, g_n, g, domain = witness
            elif len(witness) == 4:
                f_n, f, g_n, g = witness
                domain = sp.S.Reals
            else:
                return [False, False]
        else:
            return [False, False]
            
        f_n = sp.sympify(f_n)
        f = sp.sympify(f)
        g_n = sp.sympify(g_n)
        g = sp.sympify(g)
        
        if isinstance(domain, str):
            if domain.lower() in ['reals', 'r']:
                domain = sp.S.Reals
            else:
                domain = sp.sympify(domain)
    except Exception:
        return [False, False]

    # H_1: g_n converges uniformly to g on S
    h1_ok = False
    try:
        diff = sp.simplify(g_n - g)
        if diff == 0:
            h1_ok = True
        elif not diff.has(x):
            if sp.limit(diff, n, sp.oo) == 0:
                h1_ok = True
    except Exception:
        pass

    # Numerical fallback for H_1
    if not h1_ok:
        try:
            is_unif = True
            n_val = 10000
            test_points = [-100, -10, -1, 0, 1, 10, 100, n_val, -n_val, n_val**2, -n_val**2]
            for xv in test_points:
                if not check_in_domain(xv, domain):
                    continue
                val = float(sp.Abs(g_n - g).subs({x: xv, n: n_val}))
                if val > 1e-2:
                    is_unif = False
                    break
            if is_unif:
                h1_ok = True
        except Exception:
            pass

    # ¬Q: max(f_n, g_n) does NOT converge uniformly to max(f, g) on S
    neg_q_ok = False
    try:
        candidates = [
            n, -n, n**2, -n**2, sp.sqrt(n), -sp.sqrt(n), 
            1/n, -1/n, sp.exp(n), -sp.exp(n), sp.log(n), -sp.log(n),
            2*n, n/2, sp.S(1), sp.S(0), sp.pi, -sp.pi, sp.pi/n, sp.pi/(2*n),
            1 - 1/n, 1 - 1/n**2, sp.S(-1), -1 + 1/n
        ]
        
        for cand in candidates:
            try:
                val_100 = float(cand.subs(n, 100))
                if not check_in_domain(val_100, domain):
                    continue
            except Exception:
                pass
                
            def get_val(expr, xv, n_val):
                val_expr = expr.subs({x: xv, n: n_val}).evalf()
                try:
                    return float(val_expr)
                except TypeError:
                    return float(sp.re(val_expr))
                except OverflowError:
                    return float('inf')

            def seq_fn(n_val):
                xv = cand.subs(n, n_val)
                fn_num = get_val(f_n, xv, n_val)
                gn_num = get_val(g_n, xv, n_val)
                f_num = get_val(f, xv, n_val)
                g_num = get_val(g, xv, n_val)
                
                if math.isinf(fn_num) or math.isinf(gn_num) or math.isinf(f_num) or math.isinf(g_num):
                    return float('inf')
                    
                return abs(max(fn_num, gn_num) - max(f_num, g_num))
                
            vals = []
            valid_seq = True
            for n_val in [10, 100, 1000, 10000, 100000]:
                try:
                    vals.append(seq_fn(n_val))
                except Exception:
                    valid_seq = False
                    break
            
            if not valid_seq or len(vals) < 5:
                continue
                
            # Check if the difference sequence fails to converge to 0
            if vals[-1] >= 1e-4 and vals[-1] >= 0.9 * vals[-2]:
                neg_q_ok = True
                break
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: g_n converges uniformly to g on S",
    "¬Q: max(f_n, g_n) does not converge uniformly to max(f, g) on S"
]

N_HYP = 1
NEG_Q_INDEX = 1