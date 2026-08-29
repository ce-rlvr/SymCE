import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Check if the witness function is NOT uniformly continuous on R.
    Returns [neg_Q_ok].
    """
    try:
        neg_q = is_not_uniformly_continuous(witness)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The function f is not uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0

def is_not_uniformly_continuous(f_expr):
    # 1. Check if it's continuous on all of R
    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(f_expr, x, sympy.S.Reals)
        if dom != sympy.S.Reals:
            return True
    except Exception:
        pass

    # 2. Fallback domain checks
    for val in [0, 1, -1, 2, -2, sympy.pi, -sympy.pi]:
        try:
            res = f_expr.subs(x, val).evalf()
            if not res.is_real:
                return True
        except Exception:
            return True
            
    try:
        sings = sympy.singularities(f_expr, x)
        if sings is not None and not isinstance(sings, sympy.sets.EmptySet):
            if isinstance(sings, sympy.sets.FiniteSet):
                if any(s.is_real for s in sings):
                    return True
            else:
                return True
    except Exception:
        pass
        
    try:
        n, d = sympy.fraction(sympy.cancel(f_expr))
        if d != 1:
            roots = sympy.solve(d, x)
            if any(r.is_real for r in roots):
                return True
    except Exception:
        pass

    # 3. Check limit(f(x)/x) for unboundedness
    def is_unbounded(L):
        if L in [sympy.oo, -sympy.oo, sympy.zoo]:
            return True
        if isinstance(L, sympy.AccumBounds):
            if L.min == -sympy.oo or L.max == sympy.oo:
                return True
        return False

    try:
        L_inf = sympy.limit(f_expr / x, x, sympy.oo)
        if is_unbounded(L_inf):
            return True
    except Exception:
        pass

    try:
        L_minf = sympy.limit(f_expr / x, x, -sympy.oo)
        if is_unbounded(L_minf):
            return True
    except Exception:
        pass

    # 4. Check limit(f(x+shift) - f(x)) != 0 for shifts that go to 0
    def is_not_zero(L):
        if L == 0 or L.is_zero:
            return False
        if isinstance(L, sympy.AccumBounds):
            if L.min == 0 and L.max == 0:
                return False
            return True
        if L in [sympy.oo, -sympy.oo, sympy.zoo]:
            return True
        if L.is_number and L.is_finite:
            try:
                if abs(float(L)) > 1e-9:
                    return True
            except Exception:
                pass
        return False

    shifts_inf = [
        1/x, 
        1/sympy.sqrt(x), 
        x**sympy.Rational(-1, 4), 
        x**sympy.Rational(-3, 4)
    ]
    for shift in shifts_inf:
        try:
            diff_expr = f_expr.subs(x, x + shift) - f_expr
            L_diff_inf = sympy.limit(diff_expr, x, sympy.oo)
            if is_not_zero(L_diff_inf):
                return True
        except Exception:
            pass

    neg_x = -x
    shifts_minf = [
        1/neg_x, 
        1/sympy.sqrt(neg_x), 
        neg_x**sympy.Rational(-1, 4), 
        neg_x**sympy.Rational(-3, 4)
    ]
    for shift in shifts_minf:
        try:
            diff_expr_neg = f_expr.subs(x, x + shift) - f_expr
            L_diff_minf = sympy.limit(diff_expr_neg, x, -sympy.oo)
            if is_not_zero(L_diff_minf):
                return True
        except Exception:
            pass

    return False