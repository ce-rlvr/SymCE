import sympy
from sympy import Symbol, Interval, solveset, Eq
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f and g are differentiable on (a, b)",
    "H_2: For all x in (a, b), g'(x) != 0",
    "¬Q: There is no c in (a, b) such that f'(c)/g'(c) = (f(b) - f(a))/(g(b) - g(a))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness: tuple (f, g, a, b)
    where f and g are sympy expressions in terms of x,
    and a, b are real numbers defining the interval (a, b).
    """
    try:
        f, g, a, b = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]
        
    # H1: f and g are differentiable on (a, b)
    try:
        domain = Interval.open(a, b)
        
        cd_f = continuous_domain(f, x, domain)
        cd_g = continuous_domain(g, x, domain)
        
        df = f.diff(x)
        dg = g.diff(x)
        
        cd_df = continuous_domain(df, x, domain)
        cd_dg = continuous_domain(dg, x, domain)
        
        h1 = (cd_f == domain) and (cd_g == domain) and (cd_df == domain) and (cd_dg == domain)
    except Exception:
        h1 = False

    # H2: For all x in (a, b), g'(x) != 0
    try:
        dg = g.diff(x)
        zeros_dg = solveset(dg, x, domain=Interval.open(a, b))
        if zeros_dg.is_empty:
            h2 = True
        elif zeros_dg.is_empty is False:
            h2 = False
        else:
            # Fallback for complex expressions where solveset returns ConditionSet
            h2 = True
            for i in range(1, 10):
                val = float(a + i * (b - a) / 10.0)
                try:
                    root = sympy.nsolve(dg, x, val)
                    if a < root < b:
                        h2 = False
                        break
                except Exception:
                    pass
            if h2:
                for i in range(1, 1000):
                    val = float(a + i * (b - a) / 1000.0)
                    try:
                        if abs(float(dg.subs(x, val))) < 1e-7:
                            h2 = False
                            break
                    except Exception:
                        pass
    except Exception:
        h2 = False

    # neg_Q: No c in (a, b) satisfies f'(c)/g'(c) == (f(b) - f(a))/(g(b) - g(a))
    try:
        val_fa = f.subs(x, a)
        val_fb = f.subs(x, b)
        val_ga = g.subs(x, a)
        val_gb = g.subs(x, b)
        
        denom = val_gb - val_ga
        if denom == 0:
            # The right-hand side is undefined, so no such c can exist
            neg_q = True
        else:
            R = (val_fb - val_fa) / denom
            df = f.diff(x)
            dg = g.diff(x)
            
            eq = Eq(df / dg, R)
            sols = solveset(eq, x, domain=Interval.open(a, b))
            
            if sols.is_empty:
                neg_q = True
            elif sols.is_empty is False:
                neg_q = False
            else:
                # Fallback for complex expressions
                neg_q = True
                for i in range(1, 10):
                    val = float(a + i * (b - a) / 10.0)
                    try:
                        root = sympy.nsolve(eq, x, val)
                        if a < root < b:
                            neg_q = False
                            break
                    except Exception:
                        pass
                if neg_q:
                    for i in range(1, 1000):
                        val = float(a + i * (b - a) / 1000.0)
                        try:
                            lhs = float((df / dg).subs(x, val))
                            if abs(lhs - float(R)) < 1e-7:
                                neg_q = False
                                break
                        except Exception:
                            pass
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]