import sympy as sp

# Top-level setup for objects that witness expressions might reference
x, y, z, t = sp.symbols('x y z t')

def is_zero(expr):
    """Safely checks if a sympy expression is mathematically zero."""
    if expr == 0:
        return True
    try:
        simp = sp.simplify(expr)
        if simp == 0:
            return True
        num = simp.evalf()
        if num.is_number and abs(complex(num)) < 1e-9:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        vars = witness['vars']
        f = witness['f']
        g = witness['g']
        t_var = witness['t']
        S_param = witness['S_param']
        t0 = witness['t0']
    except KeyError:
        return [False, False, False, False, False]

    # H1: U is an open subset of R^n
    # We assume U is R^n (which is open) if variables are provided.
    h1 = isinstance(vars, list) and len(vars) > 0

    # H2: f, g are continuously differentiable functions
    try:
        f = sp.sympify(f)
        g = sp.sympify(g)
        grad_f_expr = [sp.diff(f, v) for v in vars]
        grad_g_expr = [sp.diff(g, v) for v in vars]
        h2 = True
    except Exception:
        h2 = False

    # H3: The restriction of f to S has a local extremum at a point a in S
    try:
        S_param = [sp.sympify(expr) for expr in S_param]
        if len(vars) != len(S_param):
            h3 = False
        else:
            a = [expr.subs(t_var, t0) for expr in S_param]
            if any(val.has(sp.nan, sp.oo, sp.zoo, -sp.oo) for val in a):
                h3 = False
            else:
                f_S = f.subs(zip(vars, S_param))
                
                # Check derivatives to confirm a local extremum
                d1 = sp.diff(f_S, t_var).subs(t_var, t0)
                if is_zero(d1):
                    d2 = sp.diff(f_S, t_var, 2).subs(t_var, t0)
                    if not is_zero(d2):
                        h3 = True
                    else:
                        d3 = sp.diff(f_S, t_var, 3).subs(t_var, t0)
                        d4 = sp.diff(f_S, t_var, 4).subs(t_var, t0)
                        if is_zero(d3) and not is_zero(d4):
                            h3 = True
                        else:
                            # If all derivatives are 0, check if it's a constant function
                            if is_zero(sp.diff(f_S, t_var)):
                                h3 = True
                            else:
                                h3 = False
                else:
                    h3 = False
    except Exception:
        h3 = False

    # H4: The gradient of g at a is not the zero vector
    try:
        grad_g_a = [expr.subs(zip(vars, a)) for expr in grad_g_expr]
        if any(val.has(sp.nan, sp.oo, sp.zoo, -sp.oo) for val in grad_g_a):
            h4 = False
        else:
            h4 = any(not is_zero(val) for val in grad_g_a)
    except Exception:
        h4 = False

    # ¬Q: grad f(a) is not a scalar multiple of grad g(a)
    # This means grad f(a) and grad g(a) are linearly independent.
    try:
        grad_f_a = [expr.subs(zip(vars, a)) for expr in grad_f_expr]
        if any(val.has(sp.nan, sp.oo, sp.zoo, -sp.oo) for val in grad_f_a):
            neg_q = False
        else:
            n = len(vars)
            independent = False
            # Check all 2x2 minors; if any is non-zero, the vectors are linearly independent
            for i in range(n):
                for j in range(i+1, n):
                    minor = grad_f_a[i]*grad_g_a[j] - grad_f_a[j]*grad_g_a[i]
                    if not is_zero(minor):
                        independent = True
                        break
                if independent:
                    break
            neg_q = independent
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f, g are continuously differentiable functions",
    "H_3: The restriction of f to S has a local extremum at a point a in S",
    "H_4: The gradient of g at a is not the zero vector",
    "¬Q: grad f(a) is not a scalar multiple of grad g(a)"
]

N_HYP = 4
NEG_Q_INDEX = 4