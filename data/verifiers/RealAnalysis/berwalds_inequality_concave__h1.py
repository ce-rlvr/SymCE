import sympy
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'f', 'a', 'b', 'p', or a tuple (f, a, b, p).
    """
    if isinstance(witness, dict):
        f = witness.get("f", x)
        a = witness.get("a", 0)
        b = witness.get("b", 1)
        p = witness.get("p", 2)
    else:
        try:
            f, a, b, p = witness
        except Exception:
            return [False, False, False]
            
    # H1: f is concave on the interval
    h1 = False
    try:
        a_val = float(a)
        b_val = float(b)
        if a_val < b_val:
            f_expr = sympy.sympify(f)
            N = 100
            pts = [a_val + (b_val - a_val) * i / N for i in range(N + 1)]
            
            f_vals = []
            valid = True
            for pt in pts:
                val = complex(f_expr.subs(x, pt))
                if abs(val.imag) > 1e-9:
                    valid = False
                    break
                f_vals.append(val.real)
                
            if valid:
                max_val = max(f_vals)
                min_val = min(f_vals)
                tol = max(1e-9, (max_val - min_val) * 1e-5)
                
                concave = True
                # Local concavity check
                for i in range(1, N):
                    if f_vals[i-1] - 2*f_vals[i] + f_vals[i+1] > tol:
                        concave = False
                        break
                
                # Global concavity check
                if concave:
                    step = max(1, N // 20)
                    for i in range(0, N, step):
                        for j in range(i + step, N + 1, step):
                            x1 = pts[i]
                            x2 = pts[j]
                            y1 = f_vals[i]
                            y2 = f_vals[j]
                            mid = 0.5 * x1 + 0.5 * x2
                            val_mid = complex(f_expr.subs(x, mid))
                            if abs(val_mid.imag) > 1e-9 or val_mid.real < 0.5 * y1 + 0.5 * y2 - tol:
                                concave = False
                                break
                        if not concave:
                            break
                h1 = concave
    except Exception:
        h1 = False

    # H2: p is a real number strictly greater than 1
    h2 = False
    try:
        if float(p) > 1.0:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    neg_q = False
    try:
        a_val = float(a)
        b_val = float(b)
        p_val = float(p)
        if a_val < b_val:
            f_expr = sympy.sympify(f)
            n_steps = 1000
            h_step = (b_val - a_val) / n_steps
            
            integral_f = 0.0
            integral_fp = 0j
            
            valid = True
            for i in range(n_steps + 1):
                xi = a_val + i * h_step
                val_c = complex(f_expr.subs(x, xi))
                if abs(val_c.imag) > 1e-9:
                    valid = False
                    break
                val = val_c.real
                
                val_p = complex(val) ** p_val
                
                # Simpson rule weights
                if i == 0 or i == n_steps:
                    weight = 1.0 / 3.0
                elif i % 2 == 1:
                    weight = 4.0 / 3.0
                else:
                    weight = 2.0 / 3.0
                    
                integral_f += weight * val
                integral_fp += weight * val_p
                
            if valid:
                integral_f *= h_step
                integral_fp *= h_step
                
                mean_fp = integral_fp / (b_val - a_val)
                if abs(mean_fp.imag) > 1e-7:
                    neg_q = True
                else:
                    lhs = complex(mean_fp.real) ** (1.0 / p_val)
                    if abs(lhs.imag) > 1e-7:
                        neg_q = True
                    else:
                        rhs = (2.0 / ((p_val + 1.0) ** (1.0 / p_val))) * (integral_f / (b_val - a_val))
                        tol = max(1e-9, 1e-7 * abs(rhs))
                        if lhs.real > rhs + tol:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is concave on the interval",
    "H_2: p is a real number strictly greater than 1",
    "¬Q: Berwald inequality fails for f"
]

N_HYP = 2
NEG_Q_INDEX = 2