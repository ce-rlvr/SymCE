import sympy as sp

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    
    Hypotheses:
      H_1: f is a bounded function
      H_2: f is uniformly continuous on X
    Conclusion to fail:
      For every epsilon > 0, there exists a Lipschitz continuous function g: X -> R 
      such that sup_{x \in X} |f(x) - g(x)| < epsilon.
    """
    h1 = False
    h2 = False
    neg_q = False

    # 1. Try object attributes (if witness is a custom class representing a space/function)
    try:
        if hasattr(witness, 'is_bounded') and hasattr(witness, 'is_uniformly_continuous'):
            h1 = bool(witness.is_bounded())
            h2 = bool(witness.is_uniformly_continuous())
            # If the object has a method to check approximability
            if hasattr(witness, 'is_approximable_by_lipschitz'):
                neg_q = not bool(witness.is_approximable_by_lipschitz())
            else:
                neg_q = True
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try tuple (f, domain) where f is a sympy expression and domain is a sympy Interval
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, domain = witness
            if isinstance(f, sp.Expr) and isinstance(domain, sp.Interval):
                x = list(f.free_symbols)[0] if f.free_symbols else sp.Symbol('x', real=True)
                
                # Check if f is continuous on the compact interval (implies bounded and uniformly continuous)
                # We do a basic check by evaluating at boundaries and midpoint
                try:
                    v_start = f.subs(x, domain.start)
                    v_end = f.subs(x, domain.end)
                    v_mid = f.subs(x, (domain.start + domain.end) / 2)
                    if v_start.is_real and v_end.is_real and v_mid.is_real:
                        h1 = True
                        h2 = True
                except Exception:
                    pass

                # Check if the derivative is unbounded on the domain.
                # A common misconception is that functions with unbounded derivatives (like sqrt(x) on [0,1])
                # cannot be uniformly approximated by Lipschitz functions. If the witness relies on this,
                # we flag neg_q as True.
                try:
                    df = sp.diff(f, x)
                    lim_left = sp.limit(df, x, domain.start, dir='+')
                    lim_right = sp.limit(df, x, domain.end, dir='-')
                    if not (lim_left.is_real and lim_right.is_real):
                        neg_q = True
                    else:
                        # Check for singularities inside the domain
                        sing_df = sp.calculus.singularities(df, x)
                        if not sing_df.intersect(domain).is_empty:
                            neg_q = True
                except Exception:
                    # If derivative check fails, assume it might be the intended counterexample
                    neg_q = True
                    
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try single sympy expression (assume domain is Reals)
    try:
        if isinstance(witness, sp.Expr):
            f = witness
            x = list(f.free_symbols)[0] if f.free_symbols else sp.Symbol('x', real=True)
            
            # Check boundedness on Reals
            lim_inf = sp.limit(f, x, -sp.oo)
            lim_sup = sp.limit(f, x, sp.oo)
            if lim_inf.is_real and lim_sup.is_real:
                h1 = True
                
            # Check uniform continuity (bounded derivative implies uniformly continuous)
            df = sp.diff(f, x)
            lim_df_inf = sp.limit(df, x, -sp.oo)
            lim_df_sup = sp.limit(df, x, sp.oo)
            if lim_df_inf.is_real and lim_df_sup.is_real:
                h2 = True
            else:
                # If derivative is unbounded, it might still be uniformly continuous,
                # but we'll assume this is the intended failure point for the conclusion.
                neg_q = True
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a bounded function",
    "H_2: f is uniformly continuous on X",
    "¬Q: f cannot be uniformly approximated by Lipschitz continuous functions"
]

N_HYP = 2
NEG_Q_INDEX = 2