import sympy as sp
from sympy import Symbol, limit, oo, diff, solve, fraction, S, Abs

# Top-level setup: named object bindings
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims: If (f_n) converges pointwise to f on R, then f is Lipschitz continuous with constant L.
    """
    # Parse witness
    if isinstance(witness, dict):
        f_n = witness.get('f_n')
        f = witness.get('f', None)
        L = witness.get('L', None)
    elif isinstance(witness, (list, tuple)):
        f_n = witness[0]
        f = witness[1] if len(witness) > 1 else None
        L = witness[2] if len(witness) > 2 else None
    else:
        f_n = witness
        f = None
        L = None

    try:
        if f_n is not None:
            f_n = sp.sympify(f_n)
        if f is not None:
            f = sp.sympify(f)
    except Exception:
        pass

    # If f is not provided, try to compute it as the pointwise limit
    if f is None and f_n is not None:
        try:
            f = limit(f_n, n, oo)
        except Exception:
            pass

    # H_1: (f_n) is a sequence of functions from R to R
    try:
        h1 = True
        test_points_h1 = [S(0), sp.Rational(3, 2), sp.Rational(-314, 100)]
        for test_n in [1, 2, 5]:
            for test_x in test_points_h1:
                try:
                    val = float(f_n.subs({n: test_n, x: test_x}))
                except Exception:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: (f_n) converges pointwise to f on R
    try:
        h2 = False
        if f is not None and f_n is not None:
            h2_ok = True
            test_points_h2 = [S(0), S(1), S(-1), sp.Rational(5, 2), sp.Rational(-314, 100), S(10), S(-10)]
            for test_x in test_points_h2:
                try:
                    fn_x = f_n.subs(x, test_x)
                    try:
                        lim_fn_x = limit(fn_x, n, oo)
                        val_lim = float(lim_fn_x)
                    except Exception:
                        # Fallback to evaluating at a large n
                        val_lim = float(fn_x.subs(n, 10000))
                    
                    f_x = f.subs(x, test_x)
                    val_f = float(f_x)
                    
                    if abs(val_lim - val_f) > 1e-4:
                        h2_ok = False
                        break
                except Exception:
                    h2_ok = False
                    break
            h2 = h2_ok
    except Exception:
        h2 = False

    # neg_Q: The limit function f is NOT Lipschitz continuous with constant L
    try:
        neg_q = False
        if f is not None:
            # 1. Check difference quotients
            pts = [i * 0.5 for i in range(-20, 21)] + [10, 100, 1000, -10, -100, -1000]
            pts += [1e-2, 1e-3, 1e-4, 1e-5, -1e-2, -1e-3, -1e-4, -1e-5]
            pairs = [(pts[i], pts[j]) for i in range(len(pts)) for j in range(i+1, len(pts))]
            
            for x1, x2 in pairs:
                try:
                    y1 = float(f.subs(x, x1))
                    y2 = float(f.subs(x, x2))
                    diff_y = abs(y1 - y2)
                    diff_x = abs(x1 - x2)
                    if diff_x > 1e-9:
                        ratio = diff_y / diff_x
                        if L is not None:
                            if ratio > float(L) + 1e-7:
                                neg_q = True
                                break
                        else:
                            if ratio > 1e6:
                                neg_q = True
                                break
                except Exception:
                    pass
                    
            # 2. Check derivative magnitude
            if not neg_q:
                df = diff(f, x)
                test_points_df = [i * 0.1 for i in range(-100, 101)] + [10, 100, 1000, -10, -100, -1000]
                for pt in test_points_df:
                    try:
                        df_val = abs(float(df.subs(x, pt)))
                        if L is not None:
                            if df_val > float(L) + 1e-7:
                                neg_q = True
                                break
                        else:
                            if df_val > 1e6:
                                neg_q = True
                                break
                    except Exception:
                        pass
                        
            # 3. If L is not provided, check if derivative is unbounded (limits or vertical asymptotes)
            if not neg_q and L is None:
                try:
                    lim_inf = limit(df, x, oo)
                    if lim_inf == oo or lim_inf == -oo:
                        neg_q = True
                except Exception:
                    pass
                try:
                    lim_minf = limit(df, x, -oo)
                    if lim_minf == oo or lim_minf == -oo:
                        neg_q = True
                except Exception:
                    pass
                
                if not neg_q:
                    try:
                        num, den = fraction(df)
                        roots = solve(den, x)
                        for r in roots:
                            if r.is_real:
                                neg_q = True
                                break
                    except Exception:
                        pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of functions from R to R",
    "H_2: (f_n) converges pointwise to f on R",
    "¬Q: The limit function f is NOT Lipschitz continuous with constant L"
]

N_HYP = 2
NEG_Q_INDEX = 2