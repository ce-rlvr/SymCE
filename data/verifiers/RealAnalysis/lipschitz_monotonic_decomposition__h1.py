import sympy as sp

# Top-level setup
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that ANY function f: R -> R can be decomposed into the 
    difference of two non-decreasing Lipschitz continuous functions.
    This is false because such a decomposition exists if and only if f itself is Lipschitz.
    Therefore, the conclusion fails (neg_Q is True) iff f is NOT Lipschitz on R.
    """
    try:
        f = witness
        if not isinstance(f, sp.Expr):
            f = f(x)
            
        free_symbols = f.free_symbols
        if len(free_symbols) == 1:
            sym = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            sym = x
        else:
            syms = [s for s in free_symbols if s.name == 'x']
            sym = syms[0] if syms else list(free_symbols)[0]
    except Exception:
        return [False]

    neg_q = False

    # 1. Check continuous domain (if not continuous on all of R, it's not Lipschitz on R)
    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(f, sym, sp.S.Reals)
        if dom != sp.S.Reals:
            neg_q = True
    except Exception:
        pass

    if not neg_q:
        try:
            df = sp.diff(f, sym)
            
            # 2. Check limits of df at infinity
            for limit_point in [sp.oo, -sp.oo]:
                try:
                    L = sp.limit(df, sym, limit_point)
                    if L in [sp.oo, -sp.oo]:
                        neg_q = True
                        break
                except Exception:
                    pass
            
            # 3. Check limit of f/sym at infinity (superlinear growth implies not Lipschitz)
            if not neg_q:
                for limit_point in [sp.oo, -sp.oo]:
                    try:
                        L = sp.limit(f / sym, sym, limit_point)
                        if L in [sp.oo, -sp.oo]:
                            neg_q = True
                            break
                    except Exception:
                        pass
            
            # 4. Polynomial check for df
            if not neg_q:
                try:
                    if df.is_polynomial(sym):
                        if sp.degree(df, sym) >= 1:
                            neg_q = True
                except Exception:
                    pass
            
            # 5. Rational function check for df
            if not neg_q:
                try:
                    if df.is_rational_function(sym):
                        df_canc = sp.cancel(df)
                        n, d = df_canc.as_numer_denom()
                        if sp.degree(n, sym) > sp.degree(d, sym):
                            neg_q = True
                        elif sp.degree(d, sym) > 0:
                            roots = sp.real_roots(d)
                            if len(roots) > 0:
                                neg_q = True
                except Exception:
                    pass
            
            # 6. Singularities of df
            if not neg_q:
                try:
                    from sympy.calculus.singularities import singularities
                    sings = singularities(df, sym)
                    if not sings.is_empty:
                        for s in sings:
                            if s.is_real:
                                L_plus = sp.limit(df, sym, s, dir='+')
                                L_minus = sp.limit(df, sym, s, dir='-')
                                if L_plus in [sp.oo, -sp.oo] or L_minus in [sp.oo, -sp.oo]:
                                    neg_q = True
                                    break
                except Exception:
                    pass

            # 7. Function range of df
            if not neg_q:
                try:
                    from sympy.calculus.util import function_range
                    frange = function_range(df, sym, sp.S.Reals)
                    if frange.sup == sp.oo or frange.inf == -sp.oo:
                        neg_q = True
                except Exception:
                    pass

            # 8. Numerical growth check for unbounded df (positive side)
            if not neg_q:
                try:
                    maxes = []
                    for k in range(1, 6):
                        pts = [10**k + j * (10**(k+1) - 10**k)/20.0 for j in range(20)]
                        m = max(float(abs(df.subs(sym, p).evalf())) for p in pts)
                        maxes.append(m)
                    
                    is_growing = True
                    for i in range(len(maxes)-1):
                        if maxes[i+1] <= maxes[i] * 1.1:
                            is_growing = False
                            break
                    
                    if is_growing and maxes[-1] > 100:
                        neg_q = True
                except Exception:
                    pass

            # 9. Numerical growth check for unbounded df (negative side)
            if not neg_q:
                try:
                    maxes_neg = []
                    for k in range(1, 6):
                        pts = [-10**k - j * (10**(k+1) - 10**k)/20.0 for j in range(20)]
                        m = max(float(abs(df.subs(sym, p).evalf())) for p in pts)
                        maxes_neg.append(m)
                    
                    is_growing = True
                    for i in range(len(maxes_neg)-1):
                        if maxes_neg[i+1] <= maxes_neg[i] * 1.1:
                            is_growing = False
                            break
                    
                    if is_growing and maxes_neg[-1] > 100:
                        neg_q = True
                except Exception:
                    pass

        except Exception:
            pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: f cannot be decomposed into the difference of two non-decreasing Lipschitz continuous functions (f is not Lipschitz)"
]

N_HYP = 0
NEG_Q_INDEX = 0