import sympy
import sympy.abc
import z3
import math
import itertools
import functools

x = sympy.abc.x

def sympy_to_z3(expr, z3_var):
    if isinstance(expr, sympy.Symbol):
        return z3_var
    elif isinstance(expr, (int, float)):
        return float(expr)
    elif isinstance(expr, sympy.Number):
        return float(expr)
    elif isinstance(expr, sympy.Add):
        return sum(sympy_to_z3(arg, z3_var) for arg in expr.args)
    elif isinstance(expr, sympy.Mul):
        res = 1
        for arg in expr.args:
            res *= sympy_to_z3(arg, z3_var)
        return res
    elif isinstance(expr, sympy.Pow):
        base = sympy_to_z3(expr.args[0], z3_var)
        exp = sympy_to_z3(expr.args[1], z3_var)
        return base ** exp
    elif isinstance(expr, sympy.Abs):
        arg = sympy_to_z3(expr.args[0], z3_var)
        return z3.If(arg > 0, arg, -arg)
    elif hasattr(expr, 'func') and expr.func.__name__ == 'Max':
        args = [sympy_to_z3(arg, z3_var) for arg in expr.args]
        res = args[0]
        for arg in args[1:]:
            res = z3.If(res > arg, res, arg)
        return res
    elif hasattr(expr, 'func') and expr.func.__name__ == 'Min':
        args = [sympy_to_z3(arg, z3_var) for arg in expr.args]
        res = args[0]
        for arg in args[1:]:
            res = z3.If(res < arg, res, arg)
        return res
    elif hasattr(expr, 'is_constant') and expr.is_constant():
        return float(expr)
    else:
        raise ValueError(f"Unsupported sympy expression: {expr}")

def check_lipschitz(f, L):
    try:
        L_float = float(L)
    except Exception:
        return None
        
    if L_float < 0:
        return False

    # Try z3 for exact verification
    try:
        u = z3.Real('u')
        v = z3.Real('v')
        fu = sympy_to_z3(f, u)
        fv = sympy_to_z3(f, v)
        
        diff_f = z3.If(fu > fv, fu - fv, fv - fu)
        diff_x = z3.If(u > v, u - v, v - u)
        
        solver = z3.Solver()
        solver.set("timeout", 500)
        solver.add(diff_f > L_float * diff_x)
        
        res = solver.check()
        if res == z3.unsat:
            return True
        elif res == z3.sat:
            return False
    except Exception:
        pass

    # Fallback to numerical grid search
    try:
        f_lam = sympy.lambdify(x, f, modules=[{'Max': max, 'Min': min, 'Abs': abs, 'sign': lambda v: 1 if v>0 else (-1 if v<0 else 0)}, 'math'])
    except Exception:
        return None

    test_points = [i * 0.01 for i in range(-1000, 1000)]
    test_points += [i * 1.0 for i in range(-100, 100)]
    
    evaluated_successfully = False
    
    # Local derivative approximation check
    for p in test_points:
        u_val = p
        v_val = p + 1e-5
        try:
            val_u = float(f_lam(u_val))
            val_v = float(f_lam(v_val))
            evaluated_successfully = True
            if abs(val_u - val_v) > L_float * 1e-5 + 1e-6:
                return False
        except Exception:
            pass
            
    if not evaluated_successfully:
        return None
        
    # Global pairs check
    subset = test_points[::10]
    for u_val, v_val in itertools.combinations(subset, 2):
        try:
            val_u = float(f_lam(u_val))
            val_v = float(f_lam(v_val))
            if abs(val_u - val_v) > L_float * abs(u_val - v_val) + 1e-6:
                return False
        except Exception:
            pass
            
    return True

def conditions(witness) -> list[bool]:
    try:
        f, L1, g, L2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1_res = check_lipschitz(f, L1)
        h1_ok = (h1_res is True)
    except Exception:
        h1_ok = False
        
    try:
        L_max = max(float(L1), float(L2))
        h_expr = sympy.Max(f, g)
        hq_res = check_lipschitz(h_expr, L_max)
        neg_q = (hq_res is False)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous with constant L1",
    "¬Q: h(x) = max(f(x), g(x)) is NOT Lipschitz continuous with constant max(L1, L2)"
]

N_HYP = 1
NEG_Q_INDEX = 1