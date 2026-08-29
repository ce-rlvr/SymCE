import sympy
import math

x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should provide a strictly positive real number `a` and a function `f`.
    """
    a = None
    f = None
    if isinstance(witness, dict):
        a = witness.get('a')
        f = witness.get('f')
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        a, f = witness
    else:
        return [False, False]

    # H_1: a is a strictly positive real number
    h1_ok = False
    try:
        if isinstance(a, (int, float)):
            h1_ok = a > 0
        else:
            a_sym = sympy.sympify(a)
            if a_sym.is_positive:
                h1_ok = True
            elif a_sym.is_real is not False:
                h1_ok = bool(a_sym > 0)
    except Exception:
        h1_ok = False

    # neg_Q: f is NOT uniformly continuous on [a, oo)
    neg_q_ok = False
    try:
        if callable(f):
            f_expr = f(x)
        elif hasattr(f, 'free_symbols'):
            f_expr = f
            free_syms = f_expr.free_symbols
            if len(free_syms) == 1:
                x_sym = list(free_syms)[0]
                if x_sym != x:
                    f_expr = f_expr.subs(x_sym, x)
        elif isinstance(f, str):
            f_expr = sympy.sympify(f)
            free_syms = f_expr.free_symbols
            if len(free_syms) == 1:
                x_sym = list(free_syms)[0]
                if x_sym != x:
                    f_expr = f_expr.subs(x_sym, x)
        else:
            f_expr = None

        if f_expr is not None:
            # 1. Symbolic check for unbounded derivative limit
            try:
                df = sympy.diff(f_expr, x)
                lim_df = sympy.limit(df, x, sympy.oo)
                if lim_df in [sympy.oo, -sympy.oo]:
                    neg_q_ok = True
            except Exception:
                pass

            # 2. Bounded/Growing derivative check
            if not neg_q_ok:
                try:
                    df = sympy.diff(f_expr, x)
                    df_vals = []
                    for k in range(1, 8):
                        for j in [1.0, 2.5, 5.0, 7.5]:
                            try:
                                val = float(abs(df.subs(x, j * 10**k)))
                                df_vals.append(val)
                            except Exception:
                                pass
                    if len(df_vals) >= 10:
                        max_df = max(df_vals)
                        min_df = min(df_vals)
                        half = len(df_vals) // 2
                        max_first_half = max(df_vals[:half])
                        max_second_half = max(df_vals[half:])
                        
                        if max_df < 1e12 and (max_df <= 2 * min_df or max_df < 1000):
                            # Derivative is bounded, so it IS uniformly continuous
                            return [h1_ok, False]
                        elif max_second_half > 5 * max_first_half and max_second_half > 100:
                            # Derivative is clearly unbounded and growing
                            neg_q_ok = True
                except Exception:
                    pass

            # 3. Numerical check for unbounded difference
            if not neg_q_ok:
                not_uc = True
                try:
                    a_val = float(a)
                except Exception:
                    a_val = 1.0
                
                for delta in [0.1, 0.01, 0.001, 0.0001, 1e-5]:
                    found_large_diff = False
                    vals_to_check = []
                    for k in [1, 2, 3, 4, 5, 6, 7, 8]:
                        base = max(10**k, a_val)
                        vals_to_check.extend([base, base + 1.0, base + 2.0, base + 3.0])
                    
                    for val in vals_to_check:
                        try:
                            y1 = float(f_expr.subs(x, val))
                            y2 = float(f_expr.subs(x, val + delta))
                            if abs(y1 - y2) > 0.5:
                                found_large_diff = True
                                break
                        except Exception:
                            continue
                    if not found_large_diff:
                        not_uc = False
                        break
                if not_uc:
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a is a strictly positive real number",
    "¬Q: f is NOT uniformly continuous on [a, oo)"
]

N_HYP = 1
NEG_Q_INDEX = 1