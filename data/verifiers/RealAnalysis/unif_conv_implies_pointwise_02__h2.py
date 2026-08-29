import sympy
from sympy import limit, oo, Abs, Max, simplify, solveset, Interval, FiniteSet, Symbol
from sympy.calculus.util import maximum

x, y, z, n = sympy.symbols('x y z n')

def conditions(witness):
    try:
        S = witness.get('S')
        f_n = witness.get('f_n')
        f = witness.get('f')
        x_sym = witness.get('x')
        n_sym = witness.get('n')
    except Exception:
        return [False, False, False]

    # H1: S is a non-empty set
    try:
        h1 = (S.is_empty is False)
    except Exception:
        h1 = False

    # H2: The sequence {f_n} converges uniformly to a function f on S
    try:
        if hasattr(n_sym, 'name'):
            n_pos = Symbol(n_sym.name, positive=True, integer=True)
            diff_expr = Abs(f_n - f).subs(n_sym, n_pos)
        else:
            n_pos = n_sym
            diff_expr = Abs(f_n - f)
            
        if isinstance(S, FiniteSet):
            sup = Max(*[diff_expr.subs(x_sym, val) for val in S])
        else:
            sup = maximum(diff_expr, x_sym, S)
            
        lim = limit(sup, n_pos, oo)
        h2 = (lim == 0)
    except Exception:
        h2 = False

    # neg_Q: The sequence {f_n} does NOT converge pointwise to f on S
    try:
        neg_q = False
        points_to_test = []
        if isinstance(S, FiniteSet):
            points_to_test = list(S)
        else:
            if isinstance(S, Interval):
                if S.start.is_finite: points_to_test.append(S.start)
                if S.end.is_finite: points_to_test.append(S.end)
                if S.start.is_finite and S.end.is_finite:
                    points_to_test.append((S.start + S.end) / 2)
            
            sample_points = [0, 1, -1, sympy.pi, sympy.E]
            for pt in sample_points:
                try:
                    if pt in S and pt not in points_to_test:
                        points_to_test.append(pt)
                except Exception:
                    pass
        
        for val in points_to_test:
            val_lim = limit(f_n.subs(x_sym, val), n_sym, oo)
            if simplify(val_lim - f.subs(x_sym, val)) != 0:
                neg_q = True
                break
        
        if not neg_q and not isinstance(S, FiniteSet):
            pw_lim = limit(f_n, n_sym, oo)
            diff = simplify(pw_lim - f)
            if diff != 0:
                roots = solveset(diff, x_sym, domain=S)
                if roots != S:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a non-empty set",
    "H_2: The sequence {f_n} converges uniformly to a function f on S",
    "¬Q: The sequence {f_n} does NOT converge pointwise to f on S"
]

N_HYP = 2
NEG_Q_INDEX = 2