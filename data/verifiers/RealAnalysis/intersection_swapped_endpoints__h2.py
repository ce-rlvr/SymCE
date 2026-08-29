import sympy
from sympy.calculus.util import continuous_domain, minimum, maximum

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the false conjecture.
    The witness is expected to be a tuple: (f, g, a, b)
    where f and g are sympy expressions in terms of x, and a, b are real numbers.
    """
    try:
        f, g, a, b = witness
    except Exception:
        return [False, False, False, False]

    try:
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        # A valid interval requires a < b
        if float(a) >= float(b):
            return [False, False, False, False]
        domain = sympy.Interval(a, b)
    except Exception:
        return [False, False, False, False]

    # H_1: f is continuous on the interval
    try:
        dom = continuous_domain(f, x, domain)
        h1 = (dom == domain)
    except Exception:
        h1 = False

    # H_2: f(a) = g(b)
    try:
        fa = f.subs(x, a)
        gb = g.subs(x, b)
        h2 = (fa == gb) or bool(sympy.simplify(fa - gb) == 0)
    except Exception:
        h2 = False

    # H_3: f(b) = g(a)
    try:
        fb = f.subs(x, b)
        ga = g.subs(x, a)
        h3 = (fb == ga) or bool(sympy.simplify(fb - ga) == 0)
    except Exception:
        h3 = False

    # ¬Q: There is no c in the interval such that f(c) = g(c)
    try:
        diff = f - g
        sols = sympy.solveset(diff, x, domain=domain)
        
        if sols == sympy.S.EmptySet:
            neg_q = True
        elif isinstance(sols, sympy.FiniteSet):
            has_sol = False
            for sol in sols:
                val_f = f.subs(x, sol)
                val_g = g.subs(x, sol)
                if (val_f == val_g) or bool(sympy.simplify(val_f - val_g) == 0):
                    has_sol = True
                    break
            neg_q = not has_sol
        else:
            # Fallback for Piecewise or complex expressions where solveset returns ConditionSet
            def get_candidates(expr1, expr2, dom):
                candidates = set()
                def extract_exprs(e):
                    e = sympy.piecewise_fold(e)
                    if isinstance(e, sympy.Piecewise):
                        return [arg[0] for arg in e.args]
                    return [e]
                
                e1s = extract_exprs(expr1)
                e2s = extract_exprs(expr2)
                
                for e1 in e1s:
                    for e2 in e2s:
                        s = sympy.solveset(e1 - e2, x, domain=dom)
                        if isinstance(s, sympy.FiniteSet):
                            candidates.update(s)
                        elif s == sympy.S.EmptySet:
                            continue
                        else:
                            return None
                return candidates

            cands = get_candidates(f, g, domain)
            if cands is not None:
                has_sol = False
                for sol in cands:
                    val_f = f.subs(x, sol)
                    val_g = g.subs(x, sol)
                    if (val_f == val_g) or bool(sympy.simplify(val_f - val_g) == 0):
                        has_sol = True
                        break
                neg_q = not has_sol
            else:
                # Try minimum and maximum as a last resort
                min_val = minimum(diff, x, domain)
                max_val = maximum(diff, x, domain)
                if min_val.is_positive is True or max_val.is_negative is True:
                    neg_q = True
                else:
                    try:
                        if float(min_val) > 0 or float(max_val) < 0:
                            neg_q = True
                        else:
                            neg_q = False
                    except Exception:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: f is continuous on the interval", "H_2: f(a) = g(b)", "H_3: f(b) = g(a)", "¬Q: There is no c in the interval such that f(c) = g(c)"]
N_HYP = 3
NEG_Q_INDEX = 3