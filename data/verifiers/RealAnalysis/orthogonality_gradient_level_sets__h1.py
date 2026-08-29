import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary containing:
      'f': sympy expression for the function f
      'vars': list of sympy symbols representing the variables of f
      'c': real number for the level set value
      'gamma': list of sympy expressions representing the curve gamma(t)
      't': sympy symbol representing the parameter of gamma
      'a': list of real numbers representing the point a
    """
    try:
        f_expr = witness['f']
        vars_syms = witness['vars']
        c_val = witness['c']
        gamma_exprs = witness['gamma']
        t_sym = witness['t']
        a_vals = witness['a']
    except Exception:
        return [False, False, False, False]

    # H_1: f is a continuously differentiable function
    try:
        grad_f = [sympy.diff(f_expr, v) for v in vars_syms]
        grad_f_a = [g.subs({v: a_val for v, a_val in zip(vars_syms, a_vals)}) for g in grad_f]
        # Check if the gradient evaluates to a valid finite vector at a
        if any(g.has(sympy.nan, sympy.oo, sympy.zoo) for g in grad_f_a):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: c is a real number and S is a level set, gamma maps to S
    try:
        if len(vars_syms) != len(gamma_exprs):
            h2 = False
        else:
            f_gamma = f_expr.subs({v: g for v, g in zip(vars_syms, gamma_exprs)})
            diff_expr = sympy.simplify(f_gamma - c_val)
            h2 = bool(diff_expr == 0)
    except Exception:
        h2 = False

    # H_3: gamma is a differentiable curve with gamma(0) = a
    try:
        if len(gamma_exprs) != len(a_vals):
            h3 = False
        else:
            gamma_0 = [g.subs(t_sym, 0) for g in gamma_exprs]
            h3_eval = all(sympy.simplify(g0 - a) == 0 for g0, a in zip(gamma_0, a_vals))
            
            gamma_prime = [sympy.diff(g, t_sym) for g in gamma_exprs]
            gamma_prime_0 = [gp.subs(t_sym, 0) for gp in gamma_prime]
            if any(gp.has(sympy.nan, sympy.oo, sympy.zoo) for gp in gamma_prime_0):
                h3 = False
            else:
                h3 = bool(h3_eval)
    except Exception:
        h3 = False

    # ¬Q: The gradient of f at a is NOT orthogonal to gamma'(0)
    # Note: Mathematically, the dot product is always zero by the chain rule.
    # The conjecture is false because the dropped hypothesis is "nabla f(a) != 0".
    # When the gradient is the zero vector, it fails to define a proper orthogonal direction.
    try:
        grad_f = [sympy.diff(f_expr, v) for v in vars_syms]
        grad_f_a = [g.subs({v: a_val for v, a_val in zip(vars_syms, a_vals)}) for g in grad_f]
        
        gamma_prime = [sympy.diff(g, t_sym) for g in gamma_exprs]
        gamma_prime_0 = [gp.subs(t_sym, 0) for gp in gamma_prime]
        
        dot_product = sum(gf * gp for gf, gp in zip(grad_f_a, gamma_prime_0))
        is_orthogonal = (sympy.simplify(dot_product) == 0)
        
        grad_is_zero = all(sympy.simplify(gf) == 0 for gf in grad_f_a)
        
        neg_q = bool((not is_orthogonal) or grad_is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable function",
    "H_2: S is a level set of f for value c, and gamma maps to S",
    "H_3: gamma is a differentiable curve with gamma(0) = a",
    "¬Q: The gradient of f at a is not orthogonal to gamma'(0) (or is the zero vector)"
]

N_HYP = 3
NEG_Q_INDEX = 3