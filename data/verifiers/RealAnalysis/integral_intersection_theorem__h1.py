import sympy as sp
from sympy import Symbol, Piecewise, integrate, Interval, solveset, Eq, EmptySet

# Top-level setup for witness expressions
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g, a, b) where f and g are sympy expressions
    (or callables returning sympy expressions) and a, b are the limits of integration.
    """
    try:
        f, g, a, b = witness
    except Exception:
        return [False, False]

    var = x
    # If f and g are provided as Python functions, try to evaluate them with the sympy symbol
    if callable(f):
        try:
            f = f(var)
        except Exception:
            pass
    if callable(g):
        try:
            g = g(var)
        except Exception:
            pass

    try:
        f = sp.sympify(f)
        g = sp.sympify(g)
        a = sp.sympify(a)
        b = sp.sympify(b)
    except Exception:
        return [False, False]

    try:
        free_symbols = (f.free_symbols | g.free_symbols) - {a, b}
        free_symbols = {s for s in free_symbols if s.is_Symbol}
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
    except Exception:
        pass

    # Check Hypothesis 1: \int_a^b f(x) dx = \int_a^b g(x) dx
    try:
        if float(a) >= float(b):
            h1 = False
        else:
            int_f = sp.integrate(f, (var, a, b))
            int_g = sp.integrate(g, (var, a, b))
            diff_int = sp.simplify(int_f - int_g)
            h1 = (diff_int == 0) or (diff_int.is_zero is True)
            if not h1:
                # Try numerical integration as fallback
                try:
                    n_points = 1000
                    a_f = float(a)
                    b_f = float(b)
                    step = (b_f - a_f) / n_points
                    sum_f = sum(float(f.subs(var, a_f + step * (i + 0.5))) for i in range(n_points)) * step
                    sum_g = sum(float(g.subs(var, a_f + step * (i + 0.5))) for i in range(n_points)) * step
                    if abs(sum_f - sum_g) < 1e-5:
                        h1 = True
                except Exception:
                    pass
    except Exception:
        h1 = False

    # Check Negated Conclusion: There is NO point c \in [a, b] such that f(c) = g(c)
    try:
        if float(a) >= float(b):
            neg_q = False
        else:
            diff = sp.simplify(f - g)
            sol = sp.solveset(diff, var, domain=sp.Interval(a, b))
            
            if isinstance(sol, sp.FiniteSet) and len(sol) > 0:
                # Found definitive solutions
                neg_q = False
            else:
                # EmptySet, ConditionSet, or other unevaluated sets.
                # Verify with numerical check.
                can_be_zero = False
                a_f = float(a)
                b_f = float(b)
                n_points = 1000
                step = (b_f - a_f) / n_points
                for i in range(n_points + 1):
                    val = a_f + step * i
                    try:
                        if abs(float(diff.subs(var, val))) < 1e-7:
                            can_be_zero = True
                            break
                    except Exception:
                        pass
                
                if can_be_zero:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Integral of f equals integral of g on the interval",
    "not Q: There is no point c in the interval such that f(c) = g(c)"
]

N_HYP = 1
NEG_Q_INDEX = 1