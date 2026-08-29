import sympy
import math

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        check_L = False
        L = None
        
        # Unpack witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, L = witness
                if isinstance(L, (int, float, sympy.Number)):
                    check_L = True
            elif len(witness) == 4:
                _, _, f, L = witness
                if isinstance(L, (int, float, sympy.Number)):
                    check_L = True
            else:
                f = witness[-1]
        else:
            f = witness

        # Ensure f is a sympy expression
        if callable(f) and not isinstance(f, sympy.Expr):
            x_sym = sympy.Symbol('x')
            try:
                f = f(x_sym)
            except Exception:
                pass

        if not isinstance(f, sympy.Expr):
            try:
                f = sympy.sympify(f)
            except Exception:
                pass

        if not isinstance(f, sympy.Expr):
            return [False, False, False]

        # H_1: (X, d) is a metric space
        # We evaluate on R with standard metric, which is a valid metric space.
        h1 = True

        # H_2: f: X -> R is a function
        h2 = True

        # neg_Q: |f| does NOT satisfy ||f(x)| - |f(y)|| <= L d(x,y) for all x,y
        neg_q = False
        free_symbols = f.free_symbols
        if len(free_symbols) >= 1:
            x_sym = list(free_symbols)[0]
        else:
            x_sym = sympy.Symbol('x')

        points = [
            0, 1, -1, 2, -2, 5, -5, 10, -10, 100, -100, 
            1000, -1000, 10000, -10000, 0.5, -0.5, 0.1, -0.1, 0.01, -0.01
        ]
        
        f_vals = {}
        for p in points:
            try:
                val = float(f.subs(x_sym, p))
                if not math.isnan(val) and not math.isinf(val):
                    f_vals[p] = val
            except Exception:
                pass
                
        threshold_L = float(L) if check_L else 10000.0

        # Check discrete pairs
        for p1 in f_vals:
            for p2 in f_vals:
                if p1 != p2:
                    diff_f = abs(abs(f_vals[p1]) - abs(f_vals[p2]))
                    diff_x = abs(p1 - p2)
                    if diff_f > threshold_L * diff_x + 1e-9:
                        neg_q = True
                        break
            if neg_q:
                break
                
        # Check derivatives for unboundedness or exceeding L
        if not neg_q:
            try:
                df = sympy.diff(f, x_sym)
                for p in points:
                    try:
                        df_val = float(df.subs(x_sym, p))
                        if not math.isnan(df_val) and not math.isinf(df_val):
                            if abs(df_val) > threshold_L + 1e-5:
                                # Verify with a small step to ensure it translates to the absolute value function
                                p2 = p + 1e-5
                                v1 = float(f.subs(x_sym, p))
                                v2 = float(f.subs(x_sym, p2))
                                if abs(abs(v1) - abs(v2)) > threshold_L * 1e-5 + 1e-12:
                                    neg_q = True
                                    break
                    except Exception:
                        pass
            except Exception:
                pass

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: f: X -> R is a function",
    "¬Q: |f| does not satisfy ||f(x)| - |f(y)|| <= L d(x,y) for all x,y"
]

N_HYP = 2
NEG_Q_INDEX = 2