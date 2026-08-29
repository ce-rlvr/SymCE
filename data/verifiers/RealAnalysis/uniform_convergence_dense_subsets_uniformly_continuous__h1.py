import sympy

# Top-level setup
x, n = sympy.symbols('x n', real=True)

CONDITION_LABELS = [
    "H_1: D is a dense subset of X",
    "H_2: (f_n) is a sequence of uniformly continuous functions from X to Y",
    "H_3: The sequence (f_n) converges uniformly on D",
    "¬Q: The sequence (f_n) does not converge uniformly on the entire space X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_in_Y(expr, domain, Y, x_sym):
    try:
        min_val = sympy.calculus.util.minimum(expr, x_sym, domain)
        max_val = sympy.calculus.util.maximum(expr, x_sym, domain)
        if isinstance(Y, sympy.Interval):
            if min_val < Y.inf or max_val > Y.sup:
                return False
            if min_val == Y.inf and Y.left_open:
                sol = sympy.solveset(sympy.Eq(expr, Y.inf), x_sym, domain=domain)
                if sol.is_empty is False:
                    return False
            if max_val == Y.sup and Y.right_open:
                sol = sympy.solveset(sympy.Eq(expr, Y.sup), x_sym, domain=domain)
                if sol.is_empty is False:
                    return False
            return True
        rng = sympy.calculus.util.function_range(expr, x_sym, domain)
        return rng.is_subset(Y)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            X = witness['X']
            Y = witness['Y']
            D = witness['D']
            f = witness['f']
            x_sym = witness['x']
            n_sym = witness['n']
        else:
            X, Y, D, f, x_sym, n_sym = witness
    except Exception:
        return [False, False, False, False]

    # H1: D is a dense subset of X
    try:
        is_subset = D.is_subset(X)
        is_dense = D.closure.is_superset(X)
        h1 = bool(is_subset and is_dense)
    except Exception:
        h1 = False

    # H2: (f_n) is a sequence of uniformly continuous functions from X to Y
    try:
        h2 = True
        for n_val in [1, 2, 5, 10]:
            fn = f.subs(n_sym, n_val)
            
            is_bounded = False
            try:
                if X.inf.is_finite and X.sup.is_finite:
                    is_bounded = True
            except AttributeError:
                pass
            
            is_uniformly_continuous = False
            if is_bounded:
                cont_dom = sympy.calculus.util.continuous_domain(fn, x_sym, sympy.Reals)
                if X.closure.is_subset(cont_dom):
                    is_uniformly_continuous = True
            
            if not is_uniformly_continuous:
                try:
                    df = sympy.diff(fn, x_sym)
                    min_df = sympy.calculus.util.minimum(df, x_sym, X)
                    max_df = sympy.calculus.util.maximum(df, x_sym, X)
                    if min_df != -sympy.oo and max_df != sympy.oo:
                        is_uniformly_continuous = True
                except Exception:
                    pass
            
            if not is_uniformly_continuous:
                h2 = False
                break
            
            if not is_in_Y(fn, X, Y, x_sym):
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: (f_n) converges uniformly on D
    try:
        f_lim = sympy.limit(f, n_sym, sympy.oo)
        if not is_in_Y(f_lim, D, Y, x_sym):
            h3 = False
        else:
            diff_simp = sympy.simplify(f - f_lim)
            if not diff_simp.has(x_sym):
                h3 = bool(sympy.limit(diff_simp, n_sym, sympy.oo) == 0)
            else:
                sup_diff_sq = sympy.calculus.util.maximum((f - f_lim)**2, x_sym, D)
                h3 = bool(sympy.limit(sup_diff_sq, n_sym, sympy.oo) == 0)
    except Exception:
        h3 = False

    # neg_Q: (f_n) does NOT converge uniformly on X
    try:
        f_lim = sympy.limit(f, n_sym, sympy.oo)
        if not is_in_Y(f_lim, X, Y, x_sym):
            neg_q = True
        else:
            diff_simp = sympy.simplify(f - f_lim)
            if not diff_simp.has(x_sym):
                neg_q = bool(sympy.limit(diff_simp, n_sym, sympy.oo) != 0)
            else:
                sup_diff_sq = sympy.calculus.util.maximum((f - f_lim)**2, x_sym, X)
                neg_q = bool(sympy.limit(sup_diff_sq, n_sym, sympy.oo) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]