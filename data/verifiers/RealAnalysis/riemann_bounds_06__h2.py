import sympy
import math
import itertools
import functools

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Generalized First Mean Value Theorem for Integrals.
    The witness is expected to be a tuple: (f, g, a, b)
    where f and g are sympy expressions in terms of x, and a, b are real numbers.
    """
    try:
        f, g, a, b = witness
    except Exception:
        return [False, False]
    
    try:
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False]
        
    # H_1: f and g are continuous on the interval
    try:
        try:
            is_valid_interval = bool(a < b)
        except TypeError:
            is_valid_interval = False
            
        if not is_valid_interval:
            h1 = False
        else:
            if f.is_polynomial(x) and g.is_polynomial(x):
                h1 = True
            else:
                try:
                    from sympy.calculus.util import continuous_domain
                    dom_f = continuous_domain(f, x, sympy.Interval(a, b))
                    dom_g = continuous_domain(g, x, sympy.Interval(a, b))
                    h1 = bool(sympy.Interval(a, b).is_subset(dom_f) and sympy.Interval(a, b).is_subset(dom_g))
                except Exception:
                    # Fallback if continuous_domain fails
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: There is no c in the interval such that integral of f*g = f(c) * integral of g
    try:
        LHS = sympy.integrate(f * g, (x, a, b))
        I_g = sympy.integrate(g, (x, a, b))
        
        if LHS.has(sympy.Integral) or I_g.has(sympy.Integral):
            # If sympy cannot compute the integral, we cannot verify the conclusion fails
            neg_q = False
        else:
            I_g_simp = sympy.simplify(I_g)
            if I_g_simp == 0:
                LHS_simp = sympy.simplify(LHS)
                neg_q = bool(LHS_simp != 0)
            else:
                V = sympy.simplify(LHS / I_g_simp)
                
                try:
                    from sympy.calculus.util import minimum, maximum
                    min_f = minimum(f, x, sympy.Interval(a, b))
                    max_f = maximum(f, x, sympy.Interval(a, b))
                except Exception:
                    # Fallback to evaluating at endpoints and critical points
                    vals = [f.subs(x, a), f.subs(x, b)]
                    try:
                        crit_points = sympy.solve(sympy.diff(f, x), x)
                        for cp in crit_points:
                            try:
                                if cp.is_real and a <= cp <= b:
                                    vals.append(f.subs(x, cp))
                            except Exception:
                                pass
                    except Exception:
                        pass
                    
                    try:
                        vals_eval = [float(sympy.N(v)) for v in vals]
                        min_f = min(vals_eval)
                        max_f = max(vals_eval)
                    except Exception:
                        min_f = float('-inf')
                        max_f = float('inf')
                
                try:
                    V_val = float(sympy.N(V))
                    min_f_val = float(sympy.N(min_f))
                    max_f_val = float(sympy.N(max_f))
                    # Use a small tolerance for floating point errors
                    neg_q = (V_val < min_f_val - 1e-9) or (V_val > max_f_val + 1e-9)
                except Exception:
                    try:
                        is_less = bool(V < min_f)
                        is_greater = bool(V > max_f)
                        neg_q = is_less or is_greater
                    except Exception:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The functions f and g are continuous on the closed interval",
    "¬Q: There is no c in the interval such that the integral of f(x)g(x) equals f(c) times the integral of g(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1