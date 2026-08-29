import sympy as sp
import z3
import math
import itertools
import functools
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_jacobian_condition(witness):
    n = witness['n']
    m = witness['m']
    F_func = witness['F']
    a = witness['a']
    b = witness['b']
    
    x_sym = [sp.Symbol(f'x_{i}') for i in range(n)]
    y_sym = [sp.Symbol(f'y_{i}') for i in range(m)]
    
    F_sym = F_func(x_sym, y_sym)
    if not isinstance(F_sym, (list, tuple)):
        F_sym = [F_sym]
        
    Jy = sp.Matrix(m, m, lambda i, j: sp.diff(F_sym[i], y_sym[j]))
    Jx = sp.Matrix(m, n, lambda i, j: sp.diff(F_sym[i], x_sym[j]))
    
    subs_dict = {x_sym[i]: sp.Rational(str(a[i])) for i in range(n)}
    subs_dict.update({y_sym[i]: sp.Rational(str(b[i])) for i in range(m)})
    
    Jy_val = Jy.subs(subs_dict)
    Jx_val = Jx.subs(subs_dict)
    
    det_val = Jy_val.det()
    is_singular = False
    try:
        if float(det_val) == 0.0:
            is_singular = True
    except Exception:
        if det_val == 0 or det_val.is_zero == True:
            is_singular = True
            
    if not is_singular:
        return False
        
    nullspace = Jy_val.T.nullspace()
    for v in nullspace:
        prod = v.T * Jx_val
        is_zero = True
        for i in range(n):
            val = prod[0, i]
            try:
                if float(val) != 0.0:
                    is_zero = False
                    break
            except Exception:
                if val != 0 and val.is_zero is not True:
                    is_zero = False
                    break
        if not is_zero:
            return True
            
    return False

def check_neg_Q(witness):
    try:
        if check_jacobian_condition(witness):
            return True
    except Exception:
        pass
        
    n = witness['n']
    m = witness['m']
    F_func = witness['F']
    a = witness['a']
    b = witness['b']
    
    try:
        delta_x = z3.Real('delta_x')
        x = [z3.Real(f'x_{i}') for i in range(n)]
        y1 = [z3.Real(f'y1_{i}') for i in range(m)]
        y2 = [z3.Real(f'y2_{i}') for i in range(m)]

        x_cond = z3.And([z3.And(x[i] > float(a[i]) - delta_x, x[i] < float(a[i]) + delta_x) for i in range(n)])
        y1_cond = z3.And([z3.And(y1[i] > float(b[i]) - 0.1, y1[i] < float(b[i]) + 0.1) for i in range(m)])
        y2_cond = z3.And([z3.And(y2[i] > float(b[i]) - 0.1, y2[i] < float(b[i]) + 0.1) for i in range(m)])
        y1_neq_y2 = z3.Or([y1[i] != y2[i] for i in range(m)])

        F1 = F_func(x, y1)
        if not isinstance(F1, (list, tuple)): F1 = [F1]
        F2 = F_func(x, y2)
        if not isinstance(F2, (list, tuple)): F2 = [F2]
        
        F1_zero = z3.And([F1[i] == 0 for i in range(m)])
        F2_zero = z3.And([F2[i] == 0 for i in range(m)])

        exists_body = z3.And(x_cond, y1_cond, y2_cond, y1_neq_y2, F1_zero, F2_zero)
        exists_q = z3.Exists(x + y1 + y2, exists_body)

        forall_q = z3.ForAll([delta_x], z3.Implies(delta_x > 0, exists_q))

        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(forall_q)
        if solver.check() == z3.sat:
            return True
    except Exception:
        pass
        
    try:
        d = [z3.Real(f'd_{i}') for i in range(n)]
        eps = z3.Real('eps')
        eps_0 = z3.Real('eps_0')
        y = [z3.Real(f'y_{i}') for i in range(m)]

        x_eps = [float(a[i]) + eps * d[i] for i in range(n)]
        y_cond = z3.And([z3.And(y[i] > float(b[i]) - 0.1, y[i] < float(b[i]) + 0.1) for i in range(m)])
        
        F_eps = F_func(x_eps, y)
        if not isinstance(F_eps, (list, tuple)): F_eps = [F_eps]
        F_zero = z3.And([F_eps[i] == 0 for i in range(m)])

        forall_body = z3.Implies(z3.And(eps > 0, eps < eps_0, y_cond), z3.Not(F_zero))
        forall_q = z3.ForAll([eps] + y, forall_body)

        exists_q = z3.Exists(d + [eps_0], z3.And(eps_0 > 0, forall_q))

        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(exists_q)
        if solver.check() == z3.sat:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    h1_h2_ok = False
    try:
        n = witness['n']
        m = witness['m']
        F_func = witness['F']
        a = witness['a']
        b = witness['b']
        
        x_sym = [sp.Symbol(f'x_{i}') for i in range(n)]
        y_sym = [sp.Symbol(f'y_{i}') for i in range(m)]
        
        F_sym = F_func(x_sym, y_sym)
        if not isinstance(F_sym, (list, tuple)):
            F_sym = [F_sym]
            
        if len(F_sym) == m:
            h1_h2_ok = True
            for f in F_sym:
                for var in x_sym + y_sym:
                    df = sp.diff(f, var)
                    subs_dict = {x_sym[i]: sp.Rational(str(a[i])) for i in range(n)}
                    subs_dict.update({y_sym[i]: sp.Rational(str(b[i])) for i in range(m)})
                    val = df.subs(subs_dict)
                    try:
                        fval = float(val)
                        if math.isnan(fval) or math.isinf(fval):
                            h1_h2_ok = False
                            break
                    except Exception:
                        if not val.is_real:
                            h1_h2_ok = False
                            break
                if not h1_h2_ok:
                    break
    except Exception:
        h1_h2_ok = False

    h3_ok = False
    try:
        subs_dict = {x_sym[i]: sp.Rational(str(a[i])) for i in range(n)}
        subs_dict.update({y_sym[i]: sp.Rational(str(b[i])) for i in range(m)})
        
        h3_ok = True
        for f in F_sym:
            val = f.subs(subs_dict)
            try:
                if float(val) != 0.0:
                    h3_ok = False
                    break
            except Exception:
                if val != 0 and val.is_zero is not True:
                    h3_ok = False
                    break
    except Exception:
        h3_ok = False

    neg_q_ok = False
    try:
        neg_q_ok = check_neg_Q(witness)
    except Exception:
        neg_q_ok = False

    return [h1_h2_ok, h1_h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an open set",
    "H_2: F is a continuously differentiable function",
    "H_3: F(a, b) = 0",
    "¬Q: The conclusion fails (no such neighborhoods V and W exist where y=g(x) is uniquely defined and C^1)"
]
N_HYP = 3
NEG_Q_INDEX = 3