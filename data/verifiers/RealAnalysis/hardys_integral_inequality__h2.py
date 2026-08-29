import sympy
from sympy import Symbol, integrate, oo

x = Symbol('x', positive=True)
t = Symbol('t', positive=True)

def conditions(witness) -> list[bool]:
    try:
        f, p = witness
        p = sympy.sympify(p)
    except Exception:
        return [False, False, False]

    # H1: f is continuous, non-negative on (0, \infty)
    try:
        h1 = True
        for val in [0.1, 1.0, 10.0, 100.0, 1000.0]:
            v = f.subs(x, val).evalf()
            try:
                v_float = float(v)
                if v_float < 0:
                    h1 = False
                    break
            except TypeError:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: integral of f^p from 0 to \infty converges
    try:
        int_f_p = integrate(f**p, (x, 0, oo))
        if int_f_p.has(oo, -oo, sympy.zoo, sympy.nan):
            h2 = False
        else:
            val = int_f_p.evalf()
            if val.has(oo, -oo, sympy.zoo, sympy.nan):
                h2 = False
            else:
                try:
                    float(val)
                    h2 = True
                except TypeError:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: LHS <= RHS fails
    try:
        if p == 1:
            neg_q = True
        else:
            try:
                RHS = (p / (p - 1))**p * int_f_p
            except ZeroDivisionError:
                RHS = sympy.zoo
                
            if RHS.has(sympy.zoo, sympy.nan):
                neg_q = True
            else:
                RHS_val = RHS.evalf()
                is_rhs_real = False
                try:
                    float(RHS_val)
                    is_rhs_real = True
                except TypeError:
                    pass
                
                if not is_rhs_real:
                    neg_q = True
                else:
                    F = integrate(f.subs(x, t), (t, 0, x))
                    lhs_integrand = (F / x)**p
                    LHS = integrate(lhs_integrand, (x, 0, oo))
                    
                    if LHS.has(oo, -oo, sympy.zoo, sympy.nan):
                        neg_q = True
                    else:
                        diff = (RHS - LHS).evalf()
                        try:
                            diff_float = float(diff)
                            if diff_float >= 0:
                                neg_q = False
                            else:
                                neg_q = True
                        except TypeError:
                            # If we cannot evaluate the difference numerically,
                            # we rely on the mathematical fact that the inequality
                            # is only valid for p > 1.
                            if p <= 1:
                                neg_q = True
                            else:
                                neg_q = False
    except Exception:
        try:
            if p <= 1:
                neg_q = True
            else:
                neg_q = False
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: f is a continuous, non-negative function on (0, \infty)",
    r"H_2: The improper integral \int_0^\infty f(x)^p dx converges",
    r"¬Q: \int_0^\infty \left( \frac{1}{x} \int_0^x f(t) dt \right)^p dx \le \left( \frac{p}{p-1} \right)^p \int_0^\infty f(x)^p dx fails"
]

N_HYP = 2
NEG_Q_INDEX = 2