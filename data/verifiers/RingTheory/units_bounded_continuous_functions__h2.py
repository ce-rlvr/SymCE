import sympy
from sympy import Symbol, S, oo
from sympy.calculus.util import continuous_domain, function_range
from sympy.abc import x, y, z

def get_range_inf_sup(expr, var, X):
    try:
        frange = function_range(expr, var, X)
        return frange.inf, frange.sup
    except Exception:
        if isinstance(X, sympy.sets.FiniteSet):
            vals = []
            for val in X:
                v = expr.subs(var, val)
                if v.is_real:
                    vals.append(v)
            if not vals:
                return oo, -oo
            return sympy.Min(*vals), sympy.Max(*vals)
        raise

def conditions(witness):
    try:
        if isinstance(witness, dict):
            X = witness.get('X')
            f = witness.get('f')
            var = witness.get('var', x)
        elif len(witness) == 3:
            X, f, var = witness
        elif len(witness) == 2:
            X, f = witness
            if hasattr(f, 'free_symbols') and f.free_symbols:
                var = list(f.free_symbols)[0]
            else:
                var = x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: X is a topological space
    try:
        h1 = isinstance(X, sympy.sets.Set)
    except Exception:
        h1 = False

    # H2: f is an element of C_b(X, R)
    try:
        cd = continuous_domain(f, var, S.Reals)
        is_continuous = X.is_subset(cd)
        if is_continuous is True:
            f_inf, f_sup = get_range_inf_sup(f, var, X)
            is_bounded = (f_inf > -oo) and (f_sup < oo)
        else:
            is_bounded = False
        h2 = bool(is_continuous is True and is_bounded)
    except Exception:
        h2 = False

    # neg_Q: f is a unit in C_b(X, R) XOR exists epsilon > 0 such that |f(x)| >= epsilon
    try:
        # Check if f is a unit in C_b(X, R)
        # This means there exists g in C_b(X, R) such that f*g = 1, so g = 1/f
        g = 1 / f
        cd_g = continuous_domain(g, var, S.Reals)
        g_is_continuous = X.is_subset(cd_g)
        if g_is_continuous is True:
            g_inf, g_sup = get_range_inf_sup(g, var, X)
            g_is_bounded = (g_inf > -oo) and (g_sup < oo)
        else:
            g_is_bounded = False
        is_unit = bool(g_is_continuous is True and g_is_bounded)

        # Check if exists epsilon > 0 such that |f(x)| >= epsilon for all x in X
        # This is equivalent to inf_{x \in X} |f(x)| > 0
        abs_f = abs(f)
        abs_inf, _ = get_range_inf_sup(abs_f, var, X)
        has_epsilon = bool(abs_inf > 0)

        # The conclusion is a biconditional (iff). Its negation is XOR.
        neg_q = bool(is_unit != has_epsilon)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: f is an element of C_b(X, R)",
    "¬Q: f is a unit in C_b(X, R) XOR there exists epsilon > 0 such that |f(x)| >= epsilon for all x in X"
]

N_HYP = 2
NEG_Q_INDEX = 2