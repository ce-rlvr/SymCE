import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x, t = sp.symbols('x t', positive=True)

def conditions(witness):
    """
    Given a witness tuple (p, c, f), checks if it is a valid counterexample to the false conjecture.
    p and c are real numbers, f is a function or SymPy expression in terms of x.
    """
    try:
        p, c, f = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        if isinstance(f, str):
            f_sym = sp.sympify(f, locals={'x': x, 't': t})
        elif callable(f):
            f_sym = sp.sympify(f(x))
        else:
            f_sym = sp.sympify(f)
            
        # Ensure the expression uses our positive symbols
        for sym in f_sym.free_symbols:
            if sym.name == 'x':
                f_sym = f_sym.subs(sym, x)
            elif sym.name == 't':
                f_sym = f_sym.subs(sym, t)
                
        p_sym = sp.sympify(p)
        c_sym = sp.sympify(c)
    except Exception:
        return [False, False, False, False]

    # H_1: p > 1
    try:
        h1 = float(p_sym) > 1.0
    except Exception:
        h1 = False

    # H_2: f is a non-negative measurable function on (0, infinity)
    try:
        h2 = True
        # Sample a few positive points to verify non-negativity
        for val in [0.01, 0.1, 1.0, 10.0, 100.0]:
            if hasattr(f_sym, 'subs'):
                v = f_sym.subs(x, val)
            else:
                v = f_sym
            if float(v) < 0:
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: The integral of x^{p-c} f(x)^p dx from 0 to infinity is finite
    try:
        integrand3 = x**(p_sym - c_sym) * f_sym**p_sym
        val3 = sp.integrate(integrand3, (x, 0, sp.oo))
        if val3.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
            h3 = False
        else:
            val3_f = complex(val3.evalf())
            if abs(val3_f.imag) > 1e-7:
                h3 = False
            else:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: The conclusion inequality fails
    try:
        F = sp.integrate(f_sym.subs(x, t), (t, 0, x))
        LHS_expr = x**(-c_sym) * F**p_sym
        LHS_val = sp.integrate(LHS_expr, (x, 0, sp.oo))
        
        LHS_evaluated = False
        if LHS_val.has(sp.nan, sp.zoo):
            LHS_real = False
            LHS_evaluated = False
        else:
            try:
                LHS_f = complex(LHS_val.evalf())
                if abs(LHS_f.imag) > 1e-7:
                    LHS_real = False
                    LHS_evaluated = True
                else:
                    LHS_real = True
                    LHS_f = LHS_f.real
                    LHS_evaluated = True
            except TypeError:
                if LHS_val == sp.oo:
                    LHS_f = float('inf')
                    LHS_real = True
                    LHS_evaluated = True
                elif LHS_val == -sp.oo:
                    LHS_f = float('-inf')
                    LHS_real = True
                    LHS_evaluated = True
                else:
                    LHS_real = False
                    LHS_evaluated = False

        RHS_evaluated = False
        if float(c_sym) == 1.0:
            RHS_real = False
            RHS_evaluated = True
        else:
            RHS_expr = x**(p_sym - c_sym) * f_sym**p_sym
            RHS_int = sp.integrate(RHS_expr, (x, 0, sp.oo))
            RHS_val = ((p_sym / (c_sym - 1))**p_sym) * RHS_int
            
            if RHS_val.has(sp.nan, sp.zoo):
                RHS_real = False
                RHS_evaluated = False
            else:
                try:
                    RHS_f_complex = complex(RHS_val.evalf())
                    if abs(RHS_f_complex.imag) > 1e-7:
                        RHS_real = False
                        RHS_evaluated = True
                    else:
                        RHS_real = True
                        RHS_f = RHS_f_complex.real
                        RHS_evaluated = True
                except TypeError:
                    if RHS_val == sp.oo:
                        RHS_f = float('inf')
                        RHS_real = True
                        RHS_evaluated = True
                    elif RHS_val == -sp.oo:
                        RHS_f = float('-inf')
                        RHS_real = True
                        RHS_evaluated = True
                    else:
                        RHS_real = False
                        RHS_evaluated = False

        if not LHS_evaluated or not RHS_evaluated:
            # If we couldn't evaluate one side, we can only be sure it fails if the other side evaluated to a non-real number
            if RHS_evaluated and not RHS_real:
                neg_q = True
            elif LHS_evaluated and not LHS_real:
                neg_q = True
            else:
                neg_q = False
        else:
            if not LHS_real or not RHS_real:
                neg_q = True
            else:
                neg_q = not (LHS_f <= RHS_f + 1e-7)
            
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is strictly greater than 1",
    "H_2: f is a non-negative measurable function on (0, infinity)",
    "H_3: The integral of x^{p-c} f(x)^p dx from 0 to infinity is finite",
    "¬Q: The conclusion inequality fails"
]

N_HYP = 3
NEG_Q_INDEX = 3