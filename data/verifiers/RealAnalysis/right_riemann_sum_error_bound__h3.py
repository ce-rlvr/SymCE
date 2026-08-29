import sympy
import math
from sympy.abc import x

def unpack_witness(witness):
    if isinstance(witness, dict):
        return witness['f'], witness['a'], witness['b'], witness['M'], witness['n']
    elif isinstance(witness, (list, tuple)) and len(witness) == 5:
        return witness[0], witness[1], witness[2], witness[3], witness[4]
    else:
        raise ValueError("Invalid witness format. Expected (f, a, b, M, n).")

def conditions(witness) -> list[bool]:
    try:
        f, a, b, M, n = unpack_witness(witness)
        a = float(a)
        b = float(b)
        M = float(M)
        n_int = int(n)
    except Exception:
        return [False, False, False]
        
    free_symbols = f.free_symbols if hasattr(f, 'free_symbols') else set()
    if len(free_symbols) == 1:
        sym = list(free_symbols)[0]
    else:
        sym = x
        
    # H1: f is continuously differentiable on the interval
    h1_ok = False
    try:
        if a > b:
            h1_ok = True
        else:
            df = sympy.diff(f, sym)
            h1_ok = True
            
            try:
                from sympy.calculus.singularities import singularities
                from sympy import Interval
                sings = singularities(f, sym)
                if sings.intersect(Interval(a, b)).is_empty is False:
                    h1_ok = False
                sings_df = singularities(df, sym)
                if sings_df.intersect(Interval(a, b)).is_empty is False:
                    h1_ok = False
            except Exception:
                pass

            if h1_ok:
                for i in range(101):
                    val = a + (b - a) * i / 100.0
                    v1 = float(f.subs(sym, val))
                    v2 = float(df.subs(sym, val))
                    if math.isnan(v1) or math.isinf(v1) or math.isnan(v2) or math.isinf(v2):
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H2: There exists M > 0 such that |f'(x)| <= M for all x in the interval
    h2_ok = False
    try:
        if M <= 0:
            h2_ok = False
        elif a > b:
            h2_ok = True
        else:
            df = sympy.diff(f, sym)
            h2_ok = True
            
            try:
                from sympy.calculus.util import maximum, minimum
                from sympy import Interval
                max_val = maximum(df, sym, Interval(a, b))
                min_val = minimum(df, sym, Interval(a, b))
                if hasattr(max_val, 'is_number') and max_val.is_number and hasattr(min_val, 'is_number') and min_val.is_number:
                    if float(max_val) > M + 1e-7 or float(min_val) < -M - 1e-7:
                        h2_ok = False
            except Exception:
                pass
                
            if h2_ok:
                for i in range(1001):
                    val = a + (b - a) * i / 1000.0
                    v = float(df.subs(sym, val))
                    if abs(v) > M + 1e-7:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # neg_Q: The error bound fails
    neg_q_ok = False
    try:
        integral_expr = sympy.Integral(f, (sym, a, b))
        integral_val = float(integral_expr.evalf())
        
        sum_val = 0.0
        if n_int >= 1:
            for k in range(1, n_int + 1):
                eval_point = a + k * (b - a) / n_int
                sum_val += float(f.subs(sym, eval_point))
        elif n_int <= -1:
            sum_val = 0.0
        else:
            raise ValueError("n cannot be 0")
            
        approx = ((b - a) / n_int) * sum_val
        
        lhs = abs(integral_val - approx)
        rhs = (M * (b - a)**2) / (2 * n_int)
        
        neg_q_ok = lhs > rhs + 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is continuously differentiable on the interval",
    "H_2: derivative is bounded by M on the interval",
    "not Q: The error bound fails"
]

N_HYP = 2
NEG_Q_INDEX = 2