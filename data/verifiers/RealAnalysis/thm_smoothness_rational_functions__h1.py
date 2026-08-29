import sympy
import math
import itertools

# Top-level setup
x, y, z = sympy.symbols('x y z', real=True)

def get_critical_points(expr, free_vars):
    crit_points = []
    args_to_solve = []
    
    for func in (sympy.Abs, sympy.sign, sympy.floor, sympy.ceiling, sympy.Min, sympy.Max):
        for sub in expr.find(func):
            args_to_solve.extend(sub.args)
            
    for sub in expr.find(sympy.Piecewise):
        for expr_i, cond_i in sub.args:
            if isinstance(cond_i, (sympy.Eq, sympy.Ne, sympy.Lt, sympy.Le, sympy.Gt, sympy.Ge)):
                args_to_solve.append(cond_i.lhs - cond_i.rhs)
                
    for sub in expr.find(sympy.Pow):
        base, exp = sub.args
        if exp.is_real and not exp.is_integer:
            args_to_solve.append(base)
        if exp.is_real and exp < 0:
            args_to_solve.append(base)
            
    for sub in expr.find(sympy.log):
        args_to_solve.append(sub.args[0])
        
    for arg in args_to_solve[:10]:
        try:
            roots = sympy.solve(arg, free_vars, dict=True)
            for r in roots:
                pt = {}
                valid = True
                for v in free_vars:
                    val = r.get(v, 0)
                    try:
                        pt[v] = float(val)
                    except Exception:
                        valid = False
                        break
                if valid:
                    crit_points.append(pt)
        except Exception:
            pass
            
    crit_points.append({v: 0.0 for v in free_vars})
    
    grid_1d = [-1.0, 1.0]
    for pt in itertools.product(grid_1d, repeat=len(free_vars)):
        crit_points.append(dict(zip(free_vars, pt)))
        
    unique_pts = []
    for pt in crit_points:
        if not any(all(abs(pt[v] - u[v]) < 1e-9 for v in free_vars) for u in unique_pts):
            unique_pts.append(pt)
            
    return unique_pts

def check_smoothness_symbolic(expr, free_vars, pt):
    eps = 1e-7
    far_eps = 0.1
    for var in free_vars:
        derivs = [expr]
        curr = expr
        for _ in range(5):
            curr = sympy.diff(curr, var)
            derivs.append(curr)
            
        pt_plus = {k: (v + eps if k == var else v) for k, v in pt.items()}
        pt_minus = {k: (v - eps if k == var else v) for k, v in pt.items()}
        pt_far = {k: (v + far_eps if k == var else v) for k, v in pt.items()}
        
        try:
            v_center = expr.subs(pt).evalf()
            if v_center.is_real:
                val_center = float(v_center)
                v_plus_0 = expr.subs(pt_plus).evalf()
                v_minus_0 = expr.subs(pt_minus).evalf()
                if v_plus_0.is_real and abs(float(v_plus_0) - val_center) > 0.1:
                    return False
                if v_minus_0.is_real and abs(float(v_minus_0) - val_center) > 0.1:
                    return False
        except Exception:
            pass
            
        vals_plus = []
        vals_minus = []
        
        for d in derivs:
            try:
                v_plus = d.subs(pt_plus).evalf()
                v_minus = d.subs(pt_minus).evalf()
                v_far = d.subs(pt_far).evalf()
                
                if not v_plus.is_real or not v_minus.is_real:
                    return False
                    
                val_plus = float(v_plus)
                val_minus = float(v_minus)
                val_far = float(v_far) if v_far.is_real else 0.0
                
                if math.isnan(val_plus) or math.isnan(val_minus):
                    return False
                if math.isinf(val_plus) or math.isinf(val_minus):
                    return False
                    
                if abs(val_plus) > 1000 * abs(val_far) + 1e6:
                    return False
                if abs(val_minus) > 1000 * abs(val_far) + 1e6:
                    return False
                    
                vals_plus.append(val_plus)
                vals_minus.append(val_minus)
            except Exception:
                return False
                
        for i in range(len(derivs) - 1):
            jump = abs(vals_plus[i] - vals_minus[i])
            if jump > 0.1:
                avg_deriv = jump / (2 * eps)
                max_deriv = max(abs(vals_plus[i+1]), abs(vals_minus[i+1]))
                if max_deriv < 0.1 * avg_deriv:
                    return False
                    
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            Q = witness.get('Q')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            P, Q = witness
        else:
            return [False, False]
            
        if not isinstance(P, sympy.Expr):
            P = sympy.sympify(P)
        if not isinstance(Q, sympy.Expr):
            Q = sympy.sympify(Q)
            
        try:
            if Q.is_zero:
                h1 = False
            elif Q.expand().is_zero:
                h1 = False
            else:
                h1 = True
        except Exception:
            h1 = False
            
        try:
            free_vars = list(P.free_symbols | Q.free_symbols)
            if not free_vars:
                neg_q = False
            elif P.is_polynomial() and Q.is_polynomial():
                neg_q = False
            else:
                R = P / Q
                crit_points = get_critical_points(R, free_vars)
                
                is_smooth = True
                for pt in crit_points:
                    try:
                        q_val = float(Q.subs(pt).evalf())
                        if abs(q_val) < 1e-9:
                            continue
                    except Exception:
                        continue
                        
                    if not check_smoothness_symbolic(R, free_vars, pt):
                        is_smooth = False
                        break
                        
                neg_q = not is_smooth
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Q is not identically zero",
    "¬Q: R(x) = P(x)/Q(x) is not infinitely differentiable on U"
]
N_HYP = 1
NEG_Q_INDEX = 1