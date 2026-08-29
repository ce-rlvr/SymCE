import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    try:
        f, n = witness
    except Exception:
        return [False, False]
    
    try:
        if not isinstance(n, int) or n < 0:
            h1 = False
        else:
            f_expr = sp.sympify(f)
            d2n_f = sp.diff(f_expr, x, 2*n)
            
            if d2n_f.is_polynomial(x):
                h1 = True
            else:
                from sympy.calculus.util import continuous_domain
                from sympy import Interval
                dom = continuous_domain(d2n_f, x, Interval(-1, 1))
                h1 = (dom == Interval(-1, 1))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if f_expr.is_polynomial(x):
                f_poly = sp.poly(f_expr, x)
                integral_val = 0
                for k_tuple, coeff in f_poly.terms():
                    k = k_tuple[0]
                    if k % 2 == 0:
                        term_int = sp.gamma(sp.Rational(k+1, 2)) * sp.sqrt(sp.pi) / sp.gamma(sp.Rational(k, 2) + 1)
                        integral_val += coeff * term_int
            else:
                integral_val = sp.integrate(f_expr / sp.sqrt(1 - x**2), (x, -1, 1))
            
            if n == 0:
                I_n = 0
            else:
                I_n = 0
                for i in range(1, n + 1):
                    node = sp.cos((2*i - 1) * sp.pi / (2*n))
                    I_n += f_expr.subs(x, node)
                I_n = sp.simplify((sp.pi / n) * I_n)
                
            error = sp.simplify(integral_val - I_n)
            coeff = sp.pi / (2**(2*n - 1) * sp.factorial(2*n))
            target = sp.simplify(error / coeff)
            
            if d2n_f.is_constant():
                val = sp.simplify(d2n_f)
                neg_q = not (sp.simplify(target - val) == 0)
            elif d2n_f.is_polynomial(x):
                poly = sp.poly(d2n_f - target, x)
                roots = sp.real_roots(poly)
                has_interior_sol = any(-1 < r.evalf() < 1 for r in roots)
                neg_q = not has_interior_sol
            else:
                sols = sp.solve(d2n_f - target, x)
                has_interior_sol = False
                for sol in sols:
                    if sol.is_real and -1 < sol < 1:
                        has_interior_sol = True
                        break
                    elif sol.is_real is None:
                        try:
                            sol_f = complex(sol.evalf())
                            if abs(sol_f.imag) < 1e-9 and -1 < sol_f.real < 1:
                                has_interior_sol = True
                                break
                        except Exception:
                            pass
                neg_q = not has_interior_sol
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is 2n times continuously differentiable on the interval from -1 to 1",
    "¬Q: The error formula does not hold for any c in the interval from -1 to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1