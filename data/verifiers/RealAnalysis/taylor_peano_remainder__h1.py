import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      'f': sympy expression for the function
      'a': left endpoint (number or real symbol)
      'b': right endpoint (number or real symbol)
      'n': integer
      'x': (optional) sympy symbol used in f, defaults to Symbol('x', real=True)
    """
    try:
        f = witness['f']
        a = witness['a']
        b = witness['b']
        n = witness['n']
        x_sym = witness.get('x', sympy.Symbol('x', real=True))
    except Exception:
        return [False, False, False]

    # H1: f is n-1 times differentiable on [a, b]
    try:
        if n - 1 < 0:
            h1_ok = True
        else:
            df = sympy.diff(f, x_sym, n - 1)
            val_a = df.subs(x_sym, a)
            val_b = df.subs(x_sym, b)
            val_mid = df.subs(x_sym, (a + b) / 2)
            h1_ok = (val_a.is_real is not False) and (val_b.is_real is not False) and (val_mid.is_real is not False)
    except Exception:
        h1_ok = False

    # H2: f^(n)(a) exists
    try:
        if n == 0:
            val = f.subs(x_sym, a)
            h2_ok = (val.is_real is not False)
        else:
            df_n1 = sympy.diff(f, x_sym, n - 1)
            dq = (df_n1 - df_n1.subs(x_sym, a)) / (x_sym - a)
            fn_a = sympy.limit(dq, x_sym, a, dir='+')
            h2_ok = (fn_a.is_real is not False)
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion fails
    try:
        if a == b:
            neg_q_ok = True
        else:
            P_n = 0
            for k in range(n + 1):
                if k == 0:
                    term = f.subs(x_sym, a)
                else:
                    df_k1 = sympy.diff(f, x_sym, k - 1)
                    dq_k = (df_k1 - df_k1.subs(x_sym, a)) / (x_sym - a)
                    fk_a = sympy.limit(dq_k, x_sym, a, dir='+')
                    term = (fk_a / sympy.factorial(k)) * (x_sym - a)**k
                P_n += term
            
            h_n = (f - P_n) / ((x_sym - a)**n)
            lim_h = sympy.limit(h_n, x_sym, a, dir='+')
            
            if isinstance(lim_h, sympy.Limit):
                neg_q_ok = False
            elif hasattr(lim_h, 'is_zero') and lim_h.is_zero is not None:
                neg_q_ok = not lim_h.is_zero
            else:
                neg_q_ok = (sympy.simplify(lim_h) != 0)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is n-1 times differentiable on the interval",
    "H_2: nth derivative of f at a exists",
    "not Q: The conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2