import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: a is a point in U",
    "H_3: f and g are differentiable at a",
    "H_4: g(a) is not equal to 0",
    "¬Q: The quotient function f/g is not differentiable at a, or its gradient is not (g(a)∇f(a) - f(a)∇g(a)) / (g(a))^2"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False, False]

    try:
        vars = [sp.Symbol(v) if isinstance(v, str) else v for v in witness.get('vars', [])]
    except Exception:
        vars = []
        
    try:
        a = [sp.sympify(val) for val in witness.get('a', [])]
    except Exception:
        a = []
        
    try:
        f_val = witness.get('f')
        if isinstance(f_val, (list, tuple)):
            f = sp.Matrix(f_val)
        else:
            f = sp.sympify(f_val)
    except Exception:
        f = None
        
    try:
        g_val = witness.get('g')
        if isinstance(g_val, (list, tuple)):
            g = sp.Matrix(g_val)
        else:
            g = sp.sympify(g_val)
    except Exception:
        g = None

    # H1: U is an open subset of R^n
    try:
        h1 = isinstance(vars, (list, tuple)) and len(vars) > 0 and all(isinstance(v, sp.Symbol) for v in vars)
    except Exception:
        h1 = False

    # H2: a is a point in U
    try:
        h2 = isinstance(a, (list, tuple)) and len(a) == len(vars)
    except Exception:
        h2 = False

    # H3: f and g are differentiable at a
    def is_diff(expr):
        if expr is None:
            return False
        if isinstance(expr, sp.Matrix):
            jac = expr.jacobian(vars)
            val = expr.subs(dict(zip(vars, a)))
        else:
            jac = sp.Matrix([expr]).jacobian(vars)
            val = sp.sympify(expr).subs(dict(zip(vars, a)))
        jac_a = jac.subs(dict(zip(vars, a)))
        if jac_a.has(sp.nan, sp.zoo, sp.oo, -sp.oo) or val.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
            return False
        return True

    try:
        h3 = is_diff(f) and is_diff(g)
    except Exception:
        h3 = False

    # H4: g(a) != 0
    try:
        if g is None:
            h4 = False
        elif isinstance(g, sp.Matrix):
            ga = g.subs(dict(zip(vars, a)))
            h4 = not ga.is_zero_matrix
        else:
            ga = sp.sympify(g).subs(dict(zip(vars, a)))
            h4 = (ga != 0) and not ga.is_zero
    except Exception:
        h4 = False

    # Conclusion
    try:
        if f is None or g is None:
            concl = False
        else:
            if isinstance(g, sp.Matrix):
                quotient = f / g
            else:
                quotient = f / g
                
            if isinstance(quotient, sp.Matrix):
                q_jac = quotient.jacobian(vars)
            else:
                q_jac = sp.Matrix([quotient]).jacobian(vars)
                
            q_jac_a = q_jac.subs(dict(zip(vars, a)))
            if q_jac_a.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
                diff_q = False
            else:
                diff_q = True
                
            if not diff_q:
                concl = False
            else:
                if isinstance(f, sp.Matrix):
                    grad_f_a = f.jacobian(vars).subs(dict(zip(vars, a)))
                    fa = f.subs(dict(zip(vars, a)))
                else:
                    grad_f_a = sp.Matrix([f]).jacobian(vars).subs(dict(zip(vars, a)))
                    fa = sp.sympify(f).subs(dict(zip(vars, a)))
                    
                if isinstance(g, sp.Matrix):
                    grad_g_a = g.jacobian(vars).subs(dict(zip(vars, a)))
                    ga = g.subs(dict(zip(vars, a)))
                else:
                    grad_g_a = sp.Matrix([g]).jacobian(vars).subs(dict(zip(vars, a)))
                    ga = sp.sympify(g).subs(dict(zip(vars, a)))
                    
                formula = (ga * grad_f_a - fa * grad_g_a) / (ga**2)
                
                diff_expr = sp.simplify(q_jac_a - formula)
                if isinstance(diff_expr, sp.Matrix):
                    concl = diff_expr.is_zero_matrix
                    if not concl:
                        try:
                            concl = all(abs(complex(val)) < 1e-9 for val in diff_expr)
                        except Exception:
                            pass
                else:
                    concl = (diff_expr == 0) or diff_expr.is_zero
                    if not concl:
                        try:
                            concl = abs(complex(diff_expr)) < 1e-9
                        except Exception:
                            pass
    except Exception:
        concl = False

    neg_q = not concl

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]