import sympy
from sympy import Symbol, Interval, FiniteSet, S, limit, oo, Abs, ImageSet, Lambda

# Top-level setup
n = Symbol('n')
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (X, f_n, f) or (X, f_n, f, x_n)
    where:
      - X is a sympy Set (e.g., Interval(-1, 1), S.Reals)
      - f_n is a sympy Expr representing the sequence of functions in terms of n and x
      - f is a sympy Expr representing the pointwise limit function in terms of x
      - x_n (optional) is a sequence of points in X where uniform convergence fails
    """
    try:
        if len(witness) == 2:
            X, f_n = witness
            f_n = sympy.sympify(f_n)
            sym_n_tmp = n
            if isinstance(f_n, sympy.Expr):
                for s in f_n.free_symbols:
                    if s.name == 'n': sym_n_tmp = s
            f = limit(f_n, sym_n_tmp, oo)
            x_n = None
        elif len(witness) == 3:
            X, f_n, f = witness
            f_n = sympy.sympify(f_n)
            f = sympy.sympify(f)
            x_n = None
        elif len(witness) == 4:
            X, f_n, f, x_n = witness
            f_n = sympy.sympify(f_n)
            f = sympy.sympify(f)
            x_n = sympy.sympify(x_n)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Extract symbols to handle potential assumption mismatches
    sym_x = x
    sym_n = n
    try:
        if isinstance(f_n, sympy.Expr):
            for s in f_n.free_symbols:
                if s.name == 'x': sym_x = s
                if s.name == 'n': sym_n = s
        if isinstance(f, sympy.Expr):
            for s in f.free_symbols:
                if s.name == 'x': sym_x = s
    except Exception:
        pass

    # H1: X is a symmetric subset of R
    h1_ok = False
    try:
        if X == S.Reals:
            h1_ok = True
        elif isinstance(X, Interval):
            h1_ok = (X.start == -X.end) and (X.left_open == X.right_open)
        elif isinstance(X, FiniteSet):
            h1_ok = all(-val in X for val in X)
        else:
            if X.is_subset(S.Reals):
                if ImageSet(Lambda(sym_x, -sym_x), X) == X:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H2: (f_n) is a sequence of real-valued functions defined on X
    h2_ok = False
    try:
        if isinstance(f_n, sympy.Expr):
            if isinstance(X, Interval):
                if X.start.is_finite and X.end.is_finite:
                    test_x = (X.start + X.end) / 2
                elif X.start.is_finite:
                    test_x = X.start + 1
                elif X.end.is_finite:
                    test_x = X.end - 1
                else:
                    test_x = 0
            elif isinstance(X, FiniteSet):
                test_x = list(X)[0]
            else:
                test_x = 0
                
            val = f_n.subs({sym_n: 1, sym_x: test_x})
            if val.is_real is not False:
                h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: O_n(x) does not converge uniformly to O(x) on X
    neg_q_ok = False
    try:
        O_n = (f_n - f_n.subs(sym_x, -sym_x)) / 2
        O = (f - f.subs(sym_x, -sym_x)) / 2
        D_n = Abs(O_n - O)
        
        test_ns = [100, 101, 102, 1000, 1001, 1002, 10000, 10001, 10002]
        
        if x_n is not None:
            D_n_x_n = D_n.subs(sym_x, x_n)
            vals = []
            for test_n in test_ns:
                try:
                    xn_val = x_n.subs(sym_n, test_n)
                    if X.contains(xn_val) is not False:
                        val = float(D_n_x_n.subs(sym_n, test_n))
                        vals.append(val)
                except Exception:
                    pass
            if any(v > 1e-5 for v in vals):
                neg_q_ok = True
            else:
                try:
                    L = limit(D_n_x_n, sym_n, oo)
                    if L != 0:
                        neg_q_ok = True
                except Exception:
                    pass
                    
        if not neg_q_ok:
            # Grid search fallback
            grid = []
            if isinstance(X, Interval):
                if X.start.is_finite and X.end.is_finite:
                    left = float(X.start)
                    right = float(X.end)
                    grid = [left + (right - left) * i / 1000.0 for i in range(1, 1000)]
                    for k in [2, 3, 4, 5]:
                        grid.append(left + 10**(-k))
                        grid.append(right - 10**(-k))
                elif X.start.is_finite:
                    left = float(X.start)
                    grid = [left + i * 0.1 for i in range(1, 1000)]
                elif X.end.is_finite:
                    right = float(X.end)
                    grid = [right - i * 0.1 for i in range(1, 1000)]
            elif isinstance(X, FiniteSet):
                grid = [float(v) for v in X]
            elif X == S.Reals:
                grid = [float(i)/10.0 for i in range(-1000, 1000)]
                grid.extend([10**k for k in range(1, 6)])
                grid.extend([-10**k for k in range(1, 6)])
            else:
                grid = [float(i)/10.0 for i in range(-100, 100)]
                
            for k in range(1, 6):
                grid.append(10**(-k))
                grid.append(-10**(-k))
                
            valid_grid = []
            for pt in grid:
                try:
                    if X.contains(sympy.sympify(pt)) is not False:
                        valid_grid.append(pt)
                except Exception:
                    pass
            grid = valid_grid
            
            for test_n in test_ns:
                expr = D_n.subs(sym_n, test_n)
                max_val = 0
                try:
                    f_num = sympy.lambdify(sym_x, expr, modules=['math'])
                    for pt in grid:
                        try:
                            val = abs(f_num(pt))
                            if val > max_val:
                                max_val = val
                        except Exception:
                            pass
                except Exception:
                    for pt in grid:
                        try:
                            val = float(expr.subs(sym_x, pt))
                            if val > max_val:
                                max_val = val
                        except Exception:
                            pass
                if max_val > 1e-2:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a symmetric subset of R",
    "H_2: (f_n) is a sequence of real-valued functions defined on X",
    "¬Q: O_n(x) does not converge uniformly to O(x) on X"
]

N_HYP = 2
NEG_Q_INDEX = 2