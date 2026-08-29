import sympy

x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a real-valued function continuous on the closed interval 0 to 1",
    "¬Q: There does NOT exist c in 0 to 1/2 such that f(c) = f(c + 1/2)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if callable(witness):
        try:
            expr = witness(x)
        except Exception:
            return [False, False]
    else:
        expr = witness

    try:
        expr = sympy.sympify(expr)
    except Exception:
        return [False, False]

    # H_1: expr is continuous on [0, 1]
    h1 = False
    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(expr, x, sympy.Interval(0, 1))
        if sympy.Interval(0, 1).is_subset(domain):
            h1 = True
            # Check real-valuedness at a few points to be safe
            for pt in [0, sympy.Rational(1, 4), sympy.Rational(1, 2), sympy.Rational(3, 4), 1]:
                val = expr.subs(x, pt)
                if not val.is_real:
                    if val.is_real is False:
                        h1 = False
                        break
                    try:
                        if abs(complex(val).imag) > 1e-9:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: NO c in [0, 1/2] such that f(c) = f(c + 1/2)
    neg_q = False
    try:
        c = sympy.Symbol('c', real=True)
        f_c = expr.subs(x, c)
        f_c_half = expr.subs(x, c + sympy.Rational(1, 2))
        eq = sympy.simplify(f_c - f_c_half)
        
        if eq.is_zero:
            neg_q = False
        else:
            sols = sympy.solveset(eq, c, domain=sympy.Interval(0, sympy.Rational(1, 2)))
            if sols == sympy.EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.FiniteSet) and len(sols) > 0:
                neg_q = False
            else:
                # Fallback to min/max to handle ConditionSet or confirm roots
                from sympy.calculus.util import minimum, maximum
                min_val = minimum(eq, c, sympy.Interval(0, sympy.Rational(1, 2)))
                max_val = maximum(eq, c, sympy.Interval(0, sympy.Rational(1, 2)))
                
                # If the function is strictly positive or strictly negative, it has no roots
                if (min_val.is_real and min_val > 0) or (max_val.is_real and max_val < 0):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]