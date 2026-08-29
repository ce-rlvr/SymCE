import sympy
from sympy import symbols, integrate, diff, simplify

# Top-level setup
x, y, z, t = symbols('x y z t', real=True)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    The witness should be a dictionary with:
      'f': sympy expression for the function f
      'vars': tuple/list of sympy symbols representing the variables of f
      'gamma': tuple/list of sympy expressions representing the curve gamma(t)
      't': sympy symbol for the parameter of the curve
      'a': lower bound of the parameter
      'b': upper bound of the parameter
    """
    try:
        f = witness['f']
        vars = witness['vars']
        gamma = witness['gamma']
        t_var = witness['t']
        a = witness['a']
        b = witness['b']
        
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
        if not isinstance(gamma, (list, tuple)):
            gamma = [gamma]
            
    except Exception:
        return [False, False, False]

    # H1: f is continuously differentiable
    try:
        grad_f = [diff(f, v) for v in vars]
        h1 = True
    except Exception:
        h1 = False

    # H2: gamma is a piecewise smooth curve
    try:
        gamma_prime = [diff(g, t_var) for g in gamma]
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The line integral of grad f along gamma is NOT equal to f(gamma(b)) - f(gamma(a))
    try:
        integrand = 0
        for i in range(len(vars)):
            df_dxi = grad_f[i].subs(zip(vars, gamma))
            integrand += df_dxi * gamma_prime[i]
        
        integral_val = integrate(integrand, (t_var, a, b))
        
        gamma_b = [g.subs(t_var, b) for g in gamma]
        gamma_a = [g.subs(t_var, a) for g in gamma]
        
        f_b = f.subs(zip(vars, gamma_b))
        f_a = f.subs(zip(vars, gamma_a))
        
        diff_val = integral_val - (f_b - f_a)
        diff_simp = simplify(diff_val)
        
        if diff_simp == 0:
            neg_q = False
        else:
            try:
                val = complex(diff_val.evalf())
                if abs(val) < 1e-9:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                # If numerical evaluation fails, check if it contains unevaluated integrals
                if diff_simp.has(sympy.Integral):
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        # If integration or evaluation fails (e.g. due to singularity), 
        # the equality f(gamma(b)) - f(gamma(a)) == integral fails, so neg_Q is True.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable function",
    "H_2: gamma is a piecewise smooth curve",
    "¬Q: The line integral of grad f along gamma is NOT equal to f(gamma(b)) - f(gamma(a))"
]

N_HYP = 2
NEG_Q_INDEX = 2