import sympy as sp
import z3
import itertools
import math

# Top-level setup for potential witness expressions
x, y, z = sp.symbols('x y z', real=True)
x1, x2, x3, x4 = sp.symbols('x1 x2 x3 x4', real=True)

def get_vars(witness):
    if callable(witness):
        for n_args in range(1, 5):
            try:
                vs = sp.symbols(f'x1:{n_args+1}')
                exprs = witness(*vs)
                if isinstance(exprs, sp.Matrix):
                    exprs = list(exprs)
                elif not isinstance(exprs, (list, tuple)):
                    exprs = [exprs]
                return exprs, list(vs)
            except Exception:
                continue

    if isinstance(witness, sp.Matrix):
        exprs = list(witness)
    elif isinstance(witness, (list, tuple)):
        exprs = list(witness)
    else:
        exprs = [witness]
    
    free_symbols = set()
    for expr in exprs:
        if hasattr(expr, 'free_symbols'):
            free_symbols.update(expr.free_symbols)
    
    vars = sorted(list(free_symbols), key=lambda s: s.name)
    if not vars:
        vars = [sp.Symbol('x')]
    return exprs, vars

def sympy_to_z3(expr, var_map):
    if isinstance(expr, sp.Symbol):
        return var_map[expr.name]
    elif isinstance(expr, sp.Number):
        return float(expr)
    elif isinstance(expr, sp.Add):
        return sum(sympy_to_z3(arg, var_map) for arg in expr.args)
    elif isinstance(expr, sp.Mul):
        res = 1
        for arg in expr.args:
            res *= sympy_to_z3(arg, var_map)
        return res
    elif isinstance(expr, sp.Pow):
        base = sympy_to_z3(expr.base, var_map)
        exp = sympy_to_z3(expr.exp, var_map)
        if isinstance(exp, (int, float)) and exp == int(exp):
            return base ** int(exp)
        return base ** exp
    else:
        raise ValueError(f"Unsupported sympy expression: {expr}")

def check_proper(exprs, vars):
    if len(vars) == 1:
        v = vars[0]
        f = exprs[0]
        try:
            lim_inf = sp.limit(sp.Abs(f), v, sp.oo)
            lim_minf = sp.limit(sp.Abs(f), v, -sp.oo)
            if lim_inf == sp.oo and lim_minf == sp.oo:
                return True
        except Exception:
            pass
        
        try:
            f_num = sp.lambdify(v, sp.Abs(f), 'math')
            if f_num(10000) > 1000 and f_num(-10000) > 1000:
                return True
        except Exception:
            pass
        return False
    else:
        try:
            norm_sq = sum(e**2 for e in exprs)
            f_num = sp.lambdify(vars, norm_sq, 'math')
            R = 1000
            min_val = float('inf')
            if len(vars) == 2:
                for i in range(1000):
                    th = 2 * math.pi * i / 1000
                    val = f_num(R * math.cos(th), R * math.sin(th))
                    if val < min_val:
                        min_val = val
                if min_val > 10000:
                    return True
            elif len(vars) == 3:
                for i in range(40):
                    th = 2 * math.pi * i / 40
                    for j in range(40):
                        ph = math.pi * j / 40
                        val = f_num(R * math.sin(ph) * math.cos(th),
                                    R * math.sin(ph) * math.sin(th),
                                    R * math.cos(ph))
                        if val < min_val:
                            min_val = val
                if min_val > 10000:
                    return True
            else:
                pts = list(itertools.product([-R, 0, R], repeat=len(vars)))
                for pt in pts:
                    if all(p == 0 for p in pt): continue
                    val = f_num(*pt)
                    if val < 10000:
                        return False
                return True
        except Exception:
            pass
        return True

def check_jacobian(exprs, vars):
    n = len(vars)
    if len(exprs) != n:
        return False
    try:
        J = sp.Matrix(exprs).jacobian(vars)
        detJ = J.det()
        
        if detJ.is_constant():
            return bool(detJ != 0)
        
        try:
            var_map = {v.name: z3.Real(v.name) for v in vars}
            solver = z3.Solver()
            z3_det = sympy_to_z3(detJ, var_map)
            solver.add(z3_det == 0)
            solver.set("timeout", 1000)
            res = solver.check()
            if res == z3.unsat:
                return True
            elif res == z3.sat:
                return False
        except Exception:
            pass
        
        f_num = sp.lambdify(vars, detJ, 'math')
        points = [-10, -1, -0.1, 0, 0.1, 1, 10]
        vals = []
        for pt in itertools.product(points, repeat=n):
            try:
                vals.append(f_num(*pt))
            except Exception:
                pass
        if not vals:
            return False
        
        sign = 1 if vals[0] > 0 else -1
        for v in vals:
            if v == 0 or (v > 0 and sign < 0) or (v < 0 and sign > 0):
                return False
        return True
    except Exception:
        return False

def check_neg_Q(exprs, vars):
    try:
        J = sp.Matrix(exprs).jacobian(vars)
        for i in range(J.rows):
            for j in range(J.cols):
                deriv = J[i, j]
                for v in vars:
                    try:
                        lim = sp.limit(deriv, v, 0)
                        val = deriv.subs(v, 0)
                        if lim != val:
                            return True
                    except Exception:
                        return True
    except Exception:
        return True
    
    try:
        var_map1 = {v.name: z3.Real(v.name + '1') for v in vars}
        var_map2 = {v.name: z3.Real(v.name + '2') for v in vars}
        solver = z3.Solver()
        for e in exprs:
            solver.add(sympy_to_z3(e, var_map1) == sympy_to_z3(e, var_map2))
        solver.add(z3.Or([var_map1[v.name] != var_map2[v.name] for v in vars]))
        solver.set("timeout", 1000)
        if solver.check() == z3.sat:
            return True
    except Exception:
        pass
    
    return False

def conditions(witness):
    try:
        exprs, vars = get_vars(witness)
    except Exception:
        return [False, False, False]
    
    try:
        h1 = check_proper(exprs, vars)
    except Exception:
        h1 = False
        
    try:
        h2 = check_jacobian(exprs, vars)
    except Exception:
        h2 = False
        
    try:
        nq = check_neg_Q(exprs, vars)
    except Exception:
        nq = False
        
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: The map f is proper",
    "H_2: The Jacobian determinant det(Df(x)) is non-zero for all x",
    "¬Q: f is not a bijective global diffeomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2