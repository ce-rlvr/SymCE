import sympy as sp
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z, t

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f, g: U \\to R^m are differentiable at a \\in U",
    "H_3: f(a) and g(a) are not scalar multiples of each other",
    "¬Q: The angle function \\theta(x) is not differentiable at a"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            vars = witness.get('vars', [])
            a_vals = witness.get('a', [])
            f_expr = witness.get('f')
            g_expr = witness.get('g')
        else:
            vars = witness.vars
            a_vals = witness.a
            f_expr = witness.f
            g_expr = witness.g
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
        if not isinstance(a_vals, (list, tuple)):
            a_vals = [a_vals]
            
        n = len(vars)
        H1 = n >= 1
        
        if not isinstance(f_expr, sp.Matrix):
            if isinstance(f_expr, (list, tuple)):
                f_expr = sp.Matrix(f_expr)
            else:
                f_expr = sp.Matrix([f_expr])
                
        if not isinstance(g_expr, sp.Matrix):
            if isinstance(g_expr, (list, tuple)):
                g_expr = sp.Matrix(g_expr)
            else:
                g_expr = sp.Matrix([g_expr])
                
        if len(f_expr) != len(g_expr):
            return [False, False, False, False]
            
        def is_diff(expr_matrix):
            for i in range(len(expr_matrix)):
                val0 = expr_matrix[i].subs(zip(vars, a_vals))
                if val0.has(sp.oo, -sp.oo, sp.nan, sp.zoo, sp.I):
                    return False
                for j in range(n):
                    diff_expr = sp.diff(expr_matrix[i], vars[j])
                    val = diff_expr.subs(zip(vars, a_vals))
                    if val.has(sp.oo, -sp.oo, sp.nan, sp.zoo, sp.I):
                        return False
            return True
            
        H2 = is_diff(f_expr) and is_diff(g_expr)
        
        f_a = f_expr.subs(zip(vars, a_vals))
        g_a = g_expr.subs(zip(vars, a_vals))
        
        def is_scalar_multiple(u, v):
            u_list = [sp.simplify(val) for val in list(u)]
            v_list = [sp.simplify(val) for val in list(v)]
            if all(val == 0 for val in u_list):
                return True
            if all(val == 0 for val in v_list):
                return False
            M = sp.Matrix([u_list, v_list])
            return M.rank() == 1
            
        H3 = not (is_scalar_multiple(f_a, g_a) and is_scalar_multiple(g_a, f_a))
        
        dot_product = sum(f_expr[i]*g_expr[i] for i in range(len(f_expr)))
        norm_f = sp.sqrt(sum(f_expr[i]**2 for i in range(len(f_expr))))
        norm_g = sp.sqrt(sum(g_expr[i]**2 for i in range(len(g_expr))))
        
        theta = sp.acos(dot_product / (norm_f * norm_g))
        
        is_theta_diff = True
        theta_a = theta.subs(zip(vars, a_vals))
        if theta_a.has(sp.oo, -sp.oo, sp.nan, sp.zoo, sp.I):
            is_theta_diff = False
        else:
            for j in range(n):
                diff_theta = sp.diff(theta, vars[j])
                val = diff_theta.subs(zip(vars, a_vals))
                if val.has(sp.oo, -sp.oo, sp.nan, sp.zoo, sp.I):
                    is_theta_diff = False
                    break
                    
        neg_Q = not is_theta_diff
        
        return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]
    except Exception:
        return [False, False, False, False]