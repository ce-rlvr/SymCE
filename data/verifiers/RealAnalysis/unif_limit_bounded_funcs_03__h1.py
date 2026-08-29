import sympy as sp

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of functions from S to R",
    "H_2: Each function f_n is bounded on S",
    "H_3: The sequence {f_n} converges uniformly to f on S",
    "¬Q: The limit function f is not bounded on S"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n = witness['f_n']
            f = witness['f']
            domain = witness['domain']
            n = witness['n']
            x = witness['x']
        else:
            f_n, f, domain, n, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: {f_n} is a sequence of functions from S to R
    try:
        h1 = isinstance(domain, sp.Set) and hasattr(f_n, 'subs') and hasattr(f, 'subs')
    except Exception:
        h1 = False

    # H2: Each function f_n is bounded on S
    h2 = False
    try:
        bounded_all = True
        for i in [1, 2, 3, 4, 5]:
            fn_i = f_n.subs(n, i)
            try:
                max_val = sp.maximum(fn_i, x, domain)
                min_val = sp.minimum(fn_i, x, domain)
                if max_val == sp.oo or min_val == -sp.oo:
                    bounded_all = False
                    break
            except Exception:
                try:
                    from sympy.calculus.util import function_range
                    r = function_range(fn_i, x, domain)
                    if r.contains(sp.oo) or r.contains(-sp.oo):
                        bounded_all = False
                        break
                except Exception:
                    try:
                        diff_fn = sp.diff(fn_i, x)
                        crit_points = sp.solve(diff_fn, x)
                        vals = []
                        for cp in crit_points:
                            if cp.is_real and domain.contains(cp):
                                vals.append(fn_i.subs(x, cp))
                        if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
                            try:
                                vals.append(sp.limit(fn_i, x, domain.inf, dir='+'))
                            except Exception:
                                pass
                            try:
                                vals.append(sp.limit(fn_i, x, domain.sup, dir='-'))
                            except Exception:
                                pass
                        for v in vals:
                            if v == sp.oo or v == -sp.oo:
                                bounded_all = False
                                break
                    except Exception:
                        bounded_all = False
                        break
        h2 = bounded_all
    except Exception:
        h2 = False

    # H3: The sequence {f_n} converges uniformly to f on S
    h3 = False
    try:
        diff = f_n - f
        try:
            max_diff = sp.maximum(diff, x, domain)
            min_diff = sp.minimum(diff, x, domain)
            sup_abs = sp.Max(sp.Abs(max_diff), sp.Abs(min_diff))
            lim = sp.limit(sup_abs, n, sp.oo)
            if lim == 0:
                h3 = True
        except Exception:
            diff_diff = sp.diff(diff, x)
            crit_points = sp.solve(diff_diff, x)
            vals = []
            for cp in crit_points:
                vals.append(sp.Abs(diff.subs(x, cp)))
            if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
                try:
                    vals.append(sp.Abs(sp.limit(diff, x, domain.inf, dir='+')))
                except Exception:
                    pass
                try:
                    vals.append(sp.Abs(sp.limit(diff, x, domain.sup, dir='-')))
                except Exception:
                    pass
            if vals:
                all_zero = True
                for v in vals:
                    if sp.limit(v, n, sp.oo) != 0:
                        all_zero = False
                        break
                if all_zero:
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: The limit function f is NOT bounded on S
    neg_q = False
    try:
        max_val = sp.maximum(f, x, domain)
        min_val = sp.minimum(f, x, domain)
        if max_val == sp.oo or min_val == -sp.oo:
            neg_q = True
    except Exception:
        try:
            from sympy.calculus.util import function_range
            r = function_range(f, x, domain)
            if r.contains(sp.oo) or r.contains(-sp.oo):
                neg_q = True
        except Exception:
            try:
                diff_f = sp.diff(f, x)
                crit_points = sp.solve(diff_f, x)
                vals = []
                for cp in crit_points:
                    if cp.is_real and domain.contains(cp):
                        vals.append(f.subs(x, cp))
                if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
                    try:
                        vals.append(sp.limit(f, x, domain.inf, dir='+'))
                    except Exception:
                        pass
                    try:
                        vals.append(sp.limit(f, x, domain.sup, dir='-'))
                    except Exception:
                        pass
                for v in vals:
                    if v == sp.oo or v == -sp.oo:
                        neg_q = True
                        break
            except Exception:
                neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]