import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        f, a, b, lam = witness
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        lam = sympy.sympify(lam)
    except Exception:
        return [False, False]
        
    # H1: f is a continuously differentiable real-valued function on the closed interval from a to b
    try:
        a_val = float(a)
        b_val = float(b)
        lam_val = float(lam)
        if a_val >= b_val:
            h1 = False
        else:
            df = sympy.diff(f, x)
            domain_exact = sympy.Interval(a, b)
            try:
                from sympy.calculus.util import continuous_domain
                cd_f = continuous_domain(f, x, domain_exact)
                cd_df = continuous_domain(df, x, domain_exact)
                h1 = bool(domain_exact.is_subset(cd_f) and domain_exact.is_subset(cd_df))
            except Exception:
                # Fallback if continuous_domain fails to evaluate
                h1 = True
                for i in range(101):
                    pt = a_val + (b_val - a_val) * i / 100.0
                    v_f = complex(f.subs(x, pt).evalf())
                    v_df = complex(df.subs(x, pt).evalf())
                    if abs(v_f.imag) > 1e-9 or abs(v_df.imag) > 1e-9:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: The absolute value of the integral is strictly greater than the bound
    try:
        integrand_lhs = f * sympy.sin(lam * x)
        lhs_integral = sympy.Integral(integrand_lhs, (x, a, b)).evalf()
        lhs_val = abs(complex(lhs_integral).real)
        
        df = sympy.diff(f, x)
        integrand_rhs = abs(df)
        rhs_integral = sympy.Integral(integrand_rhs, (x, a, b)).evalf()
        rhs_integral_val = complex(rhs_integral).real
        
        fa = complex(f.subs(x, a).evalf()).real
        fb = complex(f.subs(x, b).evalf()).real
        
        rhs_val = (abs(fa) + abs(fb) + rhs_integral_val) / float(lam)
        
        neg_q = bool(lhs_val > rhs_val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable real-valued function on the closed interval from a to b",
    "¬Q: The absolute value of the integral is strictly greater than the bound"
]

N_HYP = 1
NEG_Q_INDEX = 1