import sympy

x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a continuous function on the interval",
    "H_2: f(x) > 0 for all x in the interval",
    "¬Q: The continuous AM-GM inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (f, a, b), checks if it is a valid counterexample.
    f should be a sympy expression in terms of x.
    a and b should be real numbers.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        f_expr, a, b = witness
        f = sympy.sympify(f_expr)
        
        if not f.free_symbols.issubset({x}):
            return [False, False, False]
            
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False, False]

    # H1: f is continuous on the interval
    try:
        if a > b:
            h1 = True
        elif a == b:
            v = f.subs(x, a).evalf()
            h1 = v.is_real and not v.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo)
        else:
            dom = sympy.calculus.util.continuous_domain(f, x, sympy.Interval(a, b))
            h1 = sympy.Interval(a, b).is_subset(dom)
    except Exception:
        h1 = False

    # H2: f(x) > 0 for all x in the interval
    try:
        if a > b:
            h2 = True
        elif a == b:
            v = f.subs(x, a).evalf()
            h2 = bool(v > 0)
        else:
            min_val = sympy.calculus.util.minimum(f, x, sympy.Interval(a, b))
            h2 = bool(min_val > 0)
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    try:
        if a >= b:
            # If a == b, division by zero makes the formula undefined.
            # If a > b, the standard formulation of the theorem usually assumes a < b, 
            # but mathematically the integrals reverse sign and the (b-a) reverses sign, 
            # so the inequality still holds. However, if a == b it definitely fails.
            if a == b:
                neg_Q = True
            else:
                integral_f = sympy.Integral(f, (x, a, b)).evalf()
                LHS = (1.0 / (b - a)) * integral_f
                
                integral_ln_f = sympy.Integral(sympy.log(f), (x, a, b)).evalf()
                RHS = sympy.exp((1.0 / (b - a)) * integral_ln_f).evalf()
                
                lhs_val = complex(LHS)
                rhs_val = complex(RHS)
                
                if abs(lhs_val.imag) > 1e-7 or abs(rhs_val.imag) > 1e-7:
                    neg_Q = True
                else:
                    neg_Q = bool(lhs_val.real < rhs_val.real - 1e-7)
        else:
            integral_f = sympy.Integral(f, (x, a, b)).evalf()
            LHS = (1.0 / (b - a)) * integral_f
            
            integral_ln_f = sympy.Integral(sympy.log(f), (x, a, b)).evalf()
            RHS = sympy.exp((1.0 / (b - a)) * integral_ln_f).evalf()
            
            lhs_val = complex(LHS)
            rhs_val = complex(RHS)
            
            if abs(lhs_val.imag) > 1e-7 or abs(rhs_val.imag) > 1e-7:
                neg_Q = True
            else:
                neg_Q = bool(lhs_val.real < rhs_val.real - 1e-7)
    except Exception:
        neg_Q = True

    return [bool(h1), bool(h2), bool(neg_Q)]