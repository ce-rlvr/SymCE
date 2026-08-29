import sympy as sp
import z3
import math

x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)
Piecewise = sp.Piecewise

def sympy_to_z3(expr, var_map):
    if isinstance(expr, (int, float)):
        return z3.RealVal(expr)
    if isinstance(expr, sp.Number):
        return z3.RealVal(float(expr))
    if isinstance(expr, sp.Symbol):
        return var_map.get(expr, z3.Real(expr.name))
    if isinstance(expr, sp.Add):
        return z3.Sum(*[sympy_to_z3(arg, var_map) for arg in expr.args])
    if isinstance(expr, sp.Mul):
        args = [sympy_to_z3(arg, var_map) for arg in expr.args]
        res = args[0]
        for a in args[1:]:
            res = res * a
        return res
    if isinstance(expr, sp.Pow):
        base = sympy_to_z3(expr.args[0], var_map)
        exp = sympy_to_z3(expr.args[1], var_map)
        return base ** exp
    if isinstance(expr, sp.Piecewise):
        res = sympy_to_z3(expr.args[-1][0], var_map)
        for e, c in reversed(expr.args[:-1]):
            z3_e = sympy_to_z3(e, var_map)
            z3_c = sympy_to_z3_cond(c, var_map)
            res = z3.If(z3_c, z3_e, res)
        return res
    if isinstance(expr, sp.Abs):
        arg = sympy_to_z3(expr.args[0], var_map)
        return z3.If(arg >= 0, arg, -arg)
    if isinstance(expr, sp.Heaviside):
        arg = sympy_to_z3(expr.args[0], var_map)
        return z3.If(arg >= 0, z3.RealVal(1), z3.RealVal(0))
    if isinstance(expr, sp.Max):
        if len(expr.args) == 2:
            a = sympy_to_z3(expr.args[0], var_map)
            b = sympy_to_z3(expr.args[1], var_map)
            return z3.If(a >= b, a, b)
        else:
            raise NotImplementedError("Max with >2 args")
    if isinstance(expr, sp.Min):
        if len(expr.args) == 2:
            a = sympy_to_z3(expr.args[0], var_map)
            b = sympy_to_z3(expr.args[1], var_map)
            return z3.If(a <= b, a, b)
        else:
            raise NotImplementedError("Min with >2 args")
    if isinstance(expr, sp.floor):
        return z3.ToReal(z3.ToInt(sympy_to_z3(expr.args[0], var_map)))
    if isinstance(expr, sp.ceiling):
        arg = sympy_to_z3(expr.args[0], var_map)
        floor_arg = z3.ToReal(z3.ToInt(arg))
        return z3.If(floor_arg == arg, arg, floor_arg + z3.RealVal(1))
    raise NotImplementedError(f"Cannot convert {expr} of type {type(expr)}")

def sympy_to_z3_cond(cond, var_map):
    if cond == True or cond == sp.S.true:
        return z3.BoolVal(True)
    if cond == False or cond == sp.S.false:
        return z3.BoolVal(False)
    if isinstance(cond, sp.Rel):
        lhs = sympy_to_z3(cond.lhs, var_map)
        rhs = sympy_to_z3(cond.rhs, var_map)
        if isinstance(cond, sp.StrictGreaterThan):
            return lhs > rhs
        if isinstance(cond, sp.StrictLessThan):
            return lhs < rhs
        if isinstance(cond, sp.GreaterThan):
            return lhs >= rhs
        if isinstance(cond, sp.LessThan):
            return lhs <= rhs
        if isinstance(cond, sp.Equality):
            return lhs == rhs
        if isinstance(cond, sp.Unequality):
            return lhs != rhs
    if isinstance(cond, sp.And):
        return z3.And(*[sympy_to_z3_cond(arg, var_map) for arg in cond.args])
    if isinstance(cond, sp.Or):
        return z3.Or(*[sympy_to_z3_cond(arg, var_map) for arg in cond.args])
    if isinstance(cond, sp.Not):
        return z3.Not(sympy_to_z3_cond(cond.args[0], var_map))
    raise NotImplementedError(f"Cannot convert condition {cond}")

def num_h1(witness):
    try:
        if callable(witness):
            return abs(float(witness(0.0))) < 1e-9
        elif isinstance(witness, (int, float)):
            return abs(float(witness)) < 1e-9
        else:
            return abs(float(witness.subs(x, 0))) < 1e-9
    except Exception:
        return False

def num_h2(witness):
    def eval_f(v):
        if callable(witness):
            return float(witness(v))
        elif isinstance(witness, (int, float)):
            return float(witness)
        else:
            return float(witness.subs(x, v))
            
    try:
        for i in range(200):
            xv = (math.sin(i * 1.1) + 1) * 50
            yv = (math.cos(i * 1.3) + 1) * 50
            fxy = eval_f(xv + yv)
            fx = eval_f(xv)
            fy = eval_f(yv)
            if fxy > fx + fy + 1e-7:
                return False
                
        for i in range(50):
            xv = (math.sin(i * 2.1) + 1) * 0.5e-5
            yv = (math.cos(i * 2.3) + 1) * 0.5e-5
            fxy = eval_f(xv + yv)
            fx = eval_f(xv)
            fy = eval_f(yv)
            if fxy > fx + fy + 1e-7:
                return False
                
        return True
    except Exception:
        return False

def num_neg_q(witness):
    def eval_f(v):
        if callable(witness):
            return float(witness(v))
        elif isinstance(witness, (int, float)):
            return float(witness)
        else:
            return float(witness.subs(x, v))
            
    try:
        f0 = eval_f(0.0)
        f_small = eval_f(1e-7)
        if abs(f0 - f_small) > 0.01:
            return True
    except Exception:
        pass
        
    test_points = [1.0, 2.0, 3.0, 0.5, 1.5]
    for i in range(20):
        test_points.append((math.sin(i * 3.1) + 1) * 5)
        
    for pt in test_points:
        try:
            f_pt = eval_f(pt)
            f_pt_plus = eval_f(pt + 1e-7)
            f_pt_minus = eval_f(max(0.0, pt - 1e-7))
            if abs(f_pt - f_pt_plus) > 0.01 or abs(f_pt - f_pt_minus) > 0.01:
                return True
        except Exception:
            continue
            
    for large_pt in [1e3, 1e4, 1e5]:
        for offset in [0.0, 0.5, 1.0]:
            try:
                pt = large_pt + offset
                f_l = eval_f(pt)
                f_l_plus = eval_f(pt + 1e-4)
                if abs(f_l - f_l_plus) > 0.1:
                    return True
            except OverflowError:
                return True
            except Exception:
                continue
            
    return False

def check_h1(witness):
    try:
        x_z3 = z3.RealVal(0)
        if callable(witness):
            f0 = witness(x_z3)
        else:
            f0 = sympy_to_z3(witness, {x: x_z3})
        
        solver = z3.Solver()
        solver.add(f0 != 0)
        res = solver.check()
        if res == z3.unsat:
            return True
        elif res == z3.sat:
            return False
    except Exception:
        pass
    
    return num_h1(witness)

def check_h2(witness):
    try:
        x_z3, y_z3 = z3.Reals('x_z3 y_z3')
        if callable(witness):
            fx = witness(x_z3)
            fy = witness(y_z3)
            fxy = witness(x_z3 + y_z3)
        else:
            fx = sympy_to_z3(witness, {x: x_z3})
            fy = sympy_to_z3(witness, {x: y_z3})
            fxy = sympy_to_z3(witness, {x: x_z3 + y_z3})
            
        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(x_z3 >= 0, y_z3 >= 0)
        solver.add(fxy > fx + fy)
        res = solver.check()
        if res == z3.unsat:
            return True
        elif res == z3.sat:
            return False
    except Exception:
        pass
        
    return num_h2(witness)

def check_neg_q(witness):
    try:
        eps, delta, x_z3, y_z3 = z3.Reals('eps delta x_z3 y_z3')
        
        def z3_abs(v):
            return z3.If(v >= 0, v, -v)
            
        if callable(witness):
            fx = witness(x_z3)
            fy = witness(y_z3)
        else:
            fx = sympy_to_z3(witness, {x: x_z3})
            fy = sympy_to_z3(witness, {x: y_z3})
            
        body = z3.And(
            x_z3 >= 0,
            y_z3 >= 0,
            z3_abs(x_z3 - y_z3) < delta,
            z3_abs(fx - fy) >= eps
        )
        
        neg_q_formula = z3.Exists(
            [eps],
            z3.And(
                eps > 0,
                z3.ForAll(
                    [delta],
                    z3.Implies(
                        delta > 0,
                        z3.Exists([x_z3, y_z3], body)
                    )
                )
            )
        )
        
        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(neg_q_formula)
        res = solver.check()
        if res == z3.sat:
            return True
        elif res == z3.unsat:
            return False
    except Exception:
        pass
        
    return num_neg_q(witness)

def conditions(witness) -> list[bool]:
    return [check_h1(witness), check_h2(witness), check_neg_q(witness)]

CONDITION_LABELS = [
    "H_1: f(0) = 0",
    "H_2: f(x + y) <= f(x) + f(y) for all x, y >= 0",
    "¬Q: f is not uniformly continuous on [0, infinity)"
]

N_HYP = 2
NEG_Q_INDEX = 2