import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness):
    # H1: f is a Lebesgue measurable function
    try:
        if not isinstance(witness, sympy.Expr):
            h1_ok = False
        elif witness.has(sympy.DiracDelta):
            # DiracDelta is a distribution, not a function
            h1_ok = False
        else:
            free_syms = witness.free_symbols
            if len(free_syms) > 1:
                h1_ok = False
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        if h1_ok:
            free_syms = witness.free_symbols
            if len(free_syms) == 1:
                var = list(free_syms)[0]
            else:
                var = sympy.Symbol('x', real=True)
                
            f = witness
            xi = sympy.Symbol('xi', real=True)
            
            # 1. Try to compute the Fourier transform
            try:
                F = sympy.fourier_transform(f, var, xi)
            except Exception:
                F = None

            if F is not None and not F.has(sympy.Integral) and 'FourierTransform' not in type(F).__name__:
                if F.has(sympy.DiracDelta) or F.has(sympy.Heaviside) or F.has(sympy.sign) or F.has(sympy.oo) or F.has(sympy.nan) or F.has(sympy.zoo):
                    neg_q = True
                else:
                    try:
                        dF = sympy.diff(F, xi)
                        vals = []
                        for val in [10, 100, 1000, 10000]:
                            v = abs(complex(dF.subs(xi, val).evalf()))
                            vals.append(v)
                        if len(vals) >= 2 and vals[-1] > 100 and vals[-1] > vals[-2]:
                            neg_q = True
                    except Exception:
                        pass
                        
                    if not neg_q:
                        try:
                            for val in [0, 1, 10, 100]:
                                v1 = complex(F.subs(xi, val).evalf())
                                v2 = complex(F.subs(xi, val + 1e-5).evalf())
                                if abs(v1 - v2) > 0.1:
                                    neg_q = True
                                    break
                        except Exception:
                            pass
                            
                    if not neg_q:
                        try:
                            v0 = F.subs(xi, 0)
                            if v0 == sympy.oo or v0 == sympy.zoo or v0 == sympy.nan:
                                neg_q = True
                        except Exception:
                            pass

            if not neg_q:
                # 2. Check limit at infinity
                try:
                    lim_inf = sympy.limit(f, var, sympy.oo)
                    if lim_inf != 0 and not isinstance(lim_inf, sympy.AccumBounds):
                        neg_q = True
                    else:
                        lim_inf_neg = sympy.limit(f, var, -sympy.oo)
                        if lim_inf_neg != 0 and not isinstance(lim_inf_neg, sympy.AccumBounds):
                            neg_q = True
                except Exception:
                    pass

            if not neg_q:
                # 3. Check periodicity
                try:
                    period = sympy.periodicity(f, var)
                    if period is not None and period != 0:
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                # 4. Check if it's a polynomial of degree >= 0
                try:
                    if f.is_polynomial(var) and f != 0:
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                # 5. Check for singularities on the real line
                try:
                    sings = sympy.singularities(f, var)
                    if isinstance(sings, sympy.Set):
                        for s in sings:
                            if s.is_real:
                                lim_s = sympy.limit(f, var, s)
                                if lim_s == sympy.oo or lim_s == -sympy.oo or lim_s == sympy.zoo or lim_s == sympy.nan or str(lim_s) in ['oo', '-oo', 'zoo', 'nan']:
                                    neg_q = True
                                    break
                except Exception:
                    pass

            if not neg_q:
                # 6. Check if f(x) decays too slowly (not in L1)
                try:
                    vals_xf = []
                    for base_val in [1000, 10000, 100000, 1000000]:
                        max_v = 0
                        for offset in [0, 1, 2, 3]:
                            val = base_val + offset
                            try:
                                v_pos = abs(complex((var * f).subs(var, val).evalf()))
                            except Exception:
                                v_pos = 0
                            try:
                                v_neg = abs(complex((var * f).subs(var, -val).evalf()))
                            except Exception:
                                v_neg = 0
                            max_v = max(max_v, v_pos, v_neg)
                        vals_xf.append(max_v)
                        
                    if len(vals_xf) == 4:
                        is_decreasing = (vals_xf[1] < vals_xf[0] * 0.95) and \
                                        (vals_xf[2] < vals_xf[1] * 0.95) and \
                                        (vals_xf[3] < vals_xf[2] * 0.95)
                        if all(v > 0.01 for v in vals_xf) and not is_decreasing:
                            neg_q = True
                except Exception:
                    pass
    except Exception:
        pass

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a Lebesgue measurable function",
    "¬Q: The Fourier transform of f is not uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1