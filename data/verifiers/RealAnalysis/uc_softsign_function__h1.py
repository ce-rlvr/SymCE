import sympy as sp
import math

x = sp.Symbol('x', real=True)

def conditions(witness):
    neg_q = False
    is_sympy = False
    f_expr = None

    try:
        if callable(witness):
            try:
                f_expr = witness(x)
                is_sympy = True
            except Exception:
                is_sympy = False
        elif isinstance(witness, str):
            f_expr = sp.sympify(witness)
            is_sympy = True
        else:
            f_expr = witness
            is_sympy = True

        if is_sympy:
            if hasattr(f_expr, 'free_symbols'):
                free_syms = f_expr.free_symbols
                if len(free_syms) == 1:
                    sym = list(free_syms)[0]
                    f_expr = f_expr.subs(sym, x)
                elif len(free_syms) > 1:
                    return [False]
            else:
                f_expr = sp.sympify(f_expr)

        def is_nonzero_limit(L):
            if L == 0:
                return False
            if L in [sp.oo, -sp.oo, sp.zoo]:
                return True
            if hasattr(sp, 'AccumBounds') and isinstance(L, sp.AccumBounds):
                if L.min == 0 and L.max == 0:
                    return False
                return True
            if hasattr(L, 'is_nonzero') and L.is_nonzero:
                return True
            return False

        if is_sympy and not neg_q:
            # 0. Check continuous domain
            try:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(f_expr, x, sp.S.Reals)
                if dom != sp.S.Reals:
                    neg_q = True
            except Exception:
                pass

            # 1. Check for singularities
            if not neg_q:
                try:
                    sings = sp.singularities(f_expr, x)
                    if not sings.is_empty:
                        neg_q = True
                except Exception:
                    pass

            # 2. Domain check via lambdify
            if not neg_q:
                try:
                    f_lam = sp.lambdify(x, f_expr, 'math')
                    for test_pt in [0.0, -1.0, 1.0, -10.0, 10.0]:
                        try:
                            v = f_lam(test_pt)
                            if math.isnan(v) or math.isinf(v):
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
                except Exception:
                    pass

            # 3. Limit checks for non-uniform continuity
            if not neg_q:
                try:
                    diff1 = f_expr.subs(x, x + 1/x) - f_expr
                    L1 = sp.limit(diff1, x, sp.oo)
                    if is_nonzero_limit(L1):
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                try:
                    diff2 = f_expr.subs(x, x + 1/x) - f_expr
                    L2 = sp.limit(diff2, x, -sp.oo)
                    if is_nonzero_limit(L2):
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                try:
                    df = sp.diff(f_expr, x)
                    L_df = sp.limit(df, x, sp.oo)
                    if L_df in [sp.oo, -sp.oo, sp.zoo]:
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                try:
                    n = sp.Symbol('n', integer=True, positive=True)
                    diff_seq1 = f_expr.subs(x, n + 1/n) - f_expr.subs(x, n)
                    L_seq1 = sp.limit(diff_seq1, n, sp.oo)
                    if is_nonzero_limit(L_seq1):
                        neg_q = True
                except Exception:
                    pass

            if not neg_q:
                try:
                    n = sp.Symbol('n', integer=True, positive=True)
                    diff_seq2 = f_expr.subs(x, sp.sqrt(n + 1)) - f_expr.subs(x, sp.sqrt(n))
                    L_seq2 = sp.limit(diff_seq2, n, sp.oo)
                    if is_nonzero_limit(L_seq2):
                        neg_q = True
                except Exception:
                    pass

        if not is_sympy and not neg_q:
            # Pure numerical checks for non-sympy callables
            try:
                for test_pt in [0.0, -1.0, 1.0, -10.0, 10.0]:
                    try:
                        v = witness(test_pt)
                        if math.isnan(v) or math.isinf(v):
                            neg_q = True
                            break
                    except Exception:
                        neg_q = True
                        break
            except Exception:
                pass

            if not neg_q:
                try:
                    diffs = []
                    for val in [1e2, 1e3, 1e4, 1e5]:
                        diffs.append(abs(witness(val + 1/val) - witness(val)))
                    if diffs[-1] > 0.1 and diffs[-1] >= diffs[-2] * 0.5:
                        neg_q = True
                except OverflowError:
                    neg_q = True
                except Exception:
                    pass

            if not neg_q:
                try:
                    diffs = []
                    for n_val in [10**3, 10**4, 10**5, 10**6]:
                        x1 = math.sqrt(n_val + 1)
                        x2 = math.sqrt(n_val)
                        diffs.append(abs(witness(x1) - witness(x2)))
                    if diffs[-1] > 0.1 and diffs[-1] >= diffs[-2] * 0.5:
                        neg_q = True
                except OverflowError:
                    neg_q = True
                except Exception:
                    pass

    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = ["¬Q: f is not uniformly continuous on R"]
N_HYP = 0
NEG_Q_INDEX = 0