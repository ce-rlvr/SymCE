import sympy as sp
import math

x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f_expr = sp.sympify(witness['f'])
            a_val = float(witness['a'])
            b_val = float(witness['b'])
        else:
            f_expr = sp.sympify(witness[0])
            a_val = float(witness[1])
            b_val = float(witness[2])
    except Exception:
        return [False, False]
        
    try:
        if any(f_expr.has(func) for func in [sp.Abs, sp.sign, sp.floor, sp.ceiling, sp.Piecewise]):
            h1_ok = False
        else:
            f_prime = sp.diff(f_expr, x)
            n = 100
            if a_val == b_val:
                pts = [a_val]
            elif a_val > b_val:
                pts = [b_val + (a_val - b_val) * i / n for i in range(n + 1)]
            else:
                pts = [a_val + (b_val - a_val) * i / n for i in range(n + 1)]
                
            h1_ok = True
            for p in pts:
                v1 = float(f_expr.subs(x, p))
                v2 = float(f_prime.subs(x, p))
                if not (math.isfinite(v1) and math.isfinite(v2)):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    try:
        if a_val >= b_val:
            neg_q = True
        else:
            try:
                f_lam = sp.lambdify(x, f_expr, 'math')
                fp_lam = sp.lambdify(x, f_prime, 'math')
            except Exception:
                f_lam = lambda val: float(f_expr.subs(x, val))
                fp_lam = lambda val: float(f_prime.subs(x, val))
                
            try:
                integral_val = float(sp.integrate(f_expr, (x, a_val, b_val)))
            except Exception:
                n_int = 1000
                h = (b_val - a_val) / n_int
                s = f_lam(a_val) + f_lam(b_val)
                for i in range(1, n_int):
                    if i % 2 == 0:
                        s += 2 * f_lam(a_val + i * h)
                    else:
                        s += 4 * f_lam(a_val + i * h)
                integral_val = s * h / 3
            
            LHS = integral_val - f_lam(a_val) * (b_val - a_val)
            target_fp = LHS / ((b_val - a_val)**2 / 2)
            
            fp_vals = []
            for i in range(1001):
                p = a_val + (b_val - a_val) * i / 1000
                fp_vals.append(fp_lam(p))
                
            min_fp = min(fp_vals)
            max_fp = max(fp_vals)
            
            if min_fp - 1e-4 <= target_fp <= max_fp + 1e-4:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = ["H_1: f is continuously differentiable on the interval", "¬Q: There does not exist c in the interval satisfying the equation"]
N_HYP = 1
NEG_Q_INDEX = 1