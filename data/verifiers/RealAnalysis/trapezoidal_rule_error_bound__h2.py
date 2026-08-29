import sympy

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False]
        f, a, b, M = witness
    except Exception:
        return [False, False]

    # H1: f is twice continuously differentiable on the interval
    try:
        f_sym = sympy.sympify(f)
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        M_sym = sympy.sympify(M)
        
        if not (a_sym.is_real and b_sym.is_real and M_sym.is_real):
            h1 = False
        elif not bool(a_sym < b_sym):
            h1 = False
        else:
            free_vars = f_sym.free_symbols
            if len(free_vars) > 1:
                h1 = False
            else:
                var = list(free_vars)[0] if free_vars else sympy.Symbol('x')
                f2 = sympy.diff(f_sym, var, 2)
                v1 = f2.subs(var, a_sym).evalf()
                v2 = f2.subs(var, b_sym).evalf()
                v3 = f2.subs(var, (a_sym+b_sym)/2).evalf()
                if v1.is_real and v2.is_real and v3.is_real:
                    h1 = True
                else:
                    h1 = False
    except Exception:
        h1 = False

    # neg_Q: error > M * (b - a)**3 / 12
    try:
        f_sym = sympy.sympify(f)
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        M_sym = sympy.sympify(M)
        var = list(f_sym.free_symbols)[0] if f_sym.free_symbols else sympy.Symbol('x')
        
        integral_val = sympy.Integral(f_sym, (var, a_sym, b_sym)).evalf()
        trap_val = ((b_sym - a_sym) / 2 * (f_sym.subs(var, a_sym) + f_sym.subs(var, b_sym))).evalf()
        
        error = abs(integral_val - trap_val)
        bound = M_sym * (b_sym - a_sym)**3 / 12
        
        neg_q = bool(error > bound)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The function f is twice continuously differentiable on the interval",
    "neg_Q: The error of the trapezoidal rule is strictly greater than the bound"
]

N_HYP = 1
NEG_Q_INDEX = 1