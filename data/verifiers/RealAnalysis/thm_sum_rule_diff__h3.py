import sympy
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings that the witness expression may reference.
# We define a standard real variable 'x' for 1D functions.
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g, a) where:
      - f and g are sympy expressions (or matrices) representing functions of x.
      - a is the point at which differentiability is evaluated.
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                f, g, a = witness
            elif len(witness) == 2:
                f, g = witness
                a = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
    except Exception:
        return [False, False, False]
        
    # H_1: U is an open subset of R^n
    # We verify that 'a' is a valid real number, implying it belongs to an open subset of R.
    try:
        h1 = isinstance(a, (int, float)) or (hasattr(a, 'is_real') and a.is_real)
    except Exception:
        h1 = False
        
    # H_2: f, g are functions U -> R^m
    # We verify that f and g can be evaluated at 'a' and do not yield undefined/infinite values.
    try:
        h2 = hasattr(f, 'subs') and hasattr(g, 'subs')
        if h2:
            v_f = f.subs(x, a)
            v_g = g.subs(x, a)
            if hasattr(v_f, 'has') and v_f.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                h2 = False
            if hasattr(v_g, 'has') and v_g.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails
    # Conclusion: f+g is differentiable at a, and D(f+g)(a) = Df(a) + Dg(a).
    # This fails if f+g is not differentiable, OR if Df(a) or Dg(a) is undefined,
    # OR if the equality does not hold.
    try:
        h = sympy.Symbol('h', real=True)
        
        def limits_equal(L1, L2):
            if L1 == L2:
                return True
            try:
                diff = L1 - L2
                if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                    return True
                if hasattr(diff, 'is_zero') and diff.is_zero:
                    return True
                diff_simp = sympy.simplify(diff)
                if hasattr(diff_simp, 'is_zero_matrix') and diff_simp.is_zero_matrix:
                    return True
                if hasattr(diff_simp, 'is_zero') and diff_simp.is_zero:
                    return True
            except Exception:
                pass
            return False

        def get_deriv(expr):
            if isinstance(expr, MatrixBase) or hasattr(expr, 'applyfunc'):
                L_plus = expr.applyfunc(lambda e: sympy.limit((e.subs(x, a+h) - e.subs(x, a))/h, h, 0, dir='+'))
                L_minus = expr.applyfunc(lambda e: sympy.limit((e.subs(x, a+h) - e.subs(x, a))/h, h, 0, dir='-'))
                if limits_equal(L_plus, L_minus) and not L_plus.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                    return True, L_plus
                return False, None
            else:
                dq = (expr.subs(x, a+h) - expr.subs(x, a))/h
                L_plus = sympy.limit(dq, h, 0, dir='+')
                L_minus = sympy.limit(dq, h, 0, dir='-')
                if limits_equal(L_plus, L_minus):
                    if getattr(L_plus, 'is_finite', None) is True:
                        return True, L_plus
                    elif not L_plus.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo):
                        return True, L_plus
                return False, None

        diff_fg, deriv_fg = get_deriv(f + g)
        diff_f, deriv_f = get_deriv(f)
        diff_g, deriv_g = get_deriv(g)
        
        if not diff_fg:
            conclusion = False
        elif not diff_f or not diff_g:
            # If f or g is not differentiable, Df(a) or Dg(a) is undefined, making the equality false.
            conclusion = False
        else:
            conclusion = limits_equal(deriv_fg, deriv_f + deriv_g)
            
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f, g are functions U -> R^m",
    "¬Q: f+g is not differentiable at a, or D(f+g)(a) != Df(a) + Dg(a) (e.g., Df(a) is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2