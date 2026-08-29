import sympy

x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a continuous, strictly increasing function on the interval from 0 to a",
    "H_2: a > 0",
    "neg_Q: The integral inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f_expr, f_inv_expr, a_val = witness
            elif len(witness) == 2:
                f_expr, a_val = witness
                f_inv_expr = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        a_float = float(a_val)
        if a_float > 0:
            h2_ok = True
            
    except Exception:
        return [False, False, False]

    if h2_ok:
        h1_ok = True
        try:
            prev_val_sym = f_expr.subs(x, 0).evalf(50)
            if abs(complex(prev_val_sym).imag) > 1e-12:
                h1_ok = False
            
            if h1_ok:
                for i in range(1, 101):
                    val = i * a_float / 100.0
                    curr_val_sym = f_expr.subs(x, val).evalf(50)
                    if abs(complex(curr_val_sym).imag) > 1e-12:
                        h1_ok = False
                        break
                    
                    if curr_val_sym.as_real_imag()[0] <= prev_val_sym.as_real_imag()[0]:
                        h1_ok = False
                        break
                    prev_val_sym = curr_val_sym
            
            if h1_ok:
                df = sympy.diff(f_expr, x)
                for i in range(100):
                    val = (i + 0.5) * a_float / 100.0
                    df_val = df.subs(x, val).evalf(50)
                    if abs(complex(df_val).imag) > 1e-12:
                        h1_ok = False
                        break
                    if df_val.as_real_imag()[0] < 0:
                        h1_ok = False
                        break
        except Exception:
            h1_ok = False

    try:
        if f_inv_expr is None:
            y = sympy.Symbol('y', real=True)
            sols = sympy.solve(f_expr - y, x)
            f_a_val = complex(f_expr.subs(x, a_val).evalf(50)).real
            for sol in sols:
                try:
                    val = complex(sol.subs(y, f_a_val).evalf(50)).real
                    if abs(val - a_float) < 1e-5:
                        f_inv_expr = sol.subs(y, x)
                        break
                except Exception:
                    pass
            if f_inv_expr is None and len(sols) == 1:
                f_inv_expr = sols[0].subs(y, x)
                
        if f_inv_expr is not None:
            int1_sym = sympy.integrate(f_expr, (x, 0, a_val))
            int1_c = complex(int1_sym.evalf())
            if abs(int1_c.imag) <= 1e-9:
                int1 = int1_c.real
                
                f_a_sym = f_expr.subs(x, a_val)
                f_a_c = complex(f_a_sym.evalf())
                f_a = f_a_c.real
                
                int2_sym = sympy.integrate(f_inv_expr, (x, 0, f_a_sym))
                int2_c = complex(int2_sym.evalf())
                if abs(int2_c.imag) <= 1e-9:
                    int2 = int2_c.real
                    
                    lhs = int1 * int2
                    rhs = (a_float**2 * f_a**2) / 4.0
                    
                    if lhs > rhs + 1e-9:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]