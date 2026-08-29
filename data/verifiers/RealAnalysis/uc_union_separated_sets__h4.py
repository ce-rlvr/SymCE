import z3
import math
import itertools
import functools
from sympy import (
    Symbol, Interval, Union, Intersection, Complement, FiniteSet,
    Piecewise, oo, S, Abs, Rational, And, Or, Not, Contains
)

# Top-level setup
x = Symbol('x', real=True)

def set_to_z3(S_set, z3_var):
    if S_set == S.EmptySet:
        return z3.BoolVal(False)
    if S_set == S.Reals:
        return z3.BoolVal(True)
    if isinstance(S_set, Interval):
        conds = []
        if S_set.inf != -oo:
            if S_set.left_open: conds.append(z3_var > float(S_set.inf))
            else: conds.append(z3_var >= float(S_set.inf))
        if S_set.sup != oo:
            if S_set.right_open: conds.append(z3_var < float(S_set.sup))
            else: conds.append(z3_var <= float(S_set.sup))
        if not conds: return z3.BoolVal(True)
        return z3.And(*conds)
    if isinstance(S_set, Union):
        return z3.Or(*[set_to_z3(arg, z3_var) for arg in S_set.args])
    if isinstance(S_set, Intersection):
        return z3.And(*[set_to_z3(arg, z3_var) for arg in S_set.args])
    if isinstance(S_set, Complement):
        return z3.And(set_to_z3(S_set.args[0], z3_var), z3.Not(set_to_z3(S_set.args[1], z3_var)))
    if isinstance(S_set, FiniteSet):
        return z3.Or(*[z3_var == float(arg) for arg in S_set.args])
    raise ValueError(f"Unsupported set: {S_set}")

def sympy_cond_to_z3(cond, z3_var):
    if cond == S.true or cond is True: return z3.BoolVal(True)
    if cond == S.false or cond is False: return z3.BoolVal(False)
    if cond.is_Relational:
        lhs = sympy_to_z3(cond.lhs, z3_var)
        rhs = sympy_to_z3(cond.rhs, z3_var)
        if cond.rel_op == '==': return lhs == rhs
        if cond.rel_op == '!=': return lhs != rhs
        if cond.rel_op == '<': return lhs < rhs
        if cond.rel_op == '<=': return lhs <= rhs
        if cond.rel_op == '>': return lhs > rhs
        if cond.rel_op == '>=': return lhs >= rhs
    if cond.is_Boolean:
        if isinstance(cond, And):
            return z3.And(*[sympy_cond_to_z3(c, z3_var) for c in cond.args])
        if isinstance(cond, Or):
            return z3.Or(*[sympy_cond_to_z3(c, z3_var) for c in cond.args])
        if isinstance(cond, Not):
            return z3.Not(sympy_cond_to_z3(cond.args[0], z3_var))
    if isinstance(cond, Contains):
        if cond.args[0] == x:
            return set_to_z3(cond.args[1], z3_var)
    raise ValueError(f"Unsupported cond: {cond}")

def sympy_to_z3(expr, z3_var):
    if isinstance(expr, Rational):
        return z3.RealVal(expr.p) / z3.RealVal(expr.q)
    if expr.is_Number:
        return float(expr)
    if expr == x:
        return z3_var
    if expr.is_Add:
        return sum(sympy_to_z3(arg, z3_var) for arg in expr.args)
    if expr.is_Mul:
        res = 1
        for arg in expr.args:
            res *= sympy_to_z3(arg, z3_var)
        return res
    if expr.is_Pow:
        base = sympy_to_z3(expr.args[0], z3_var)
        exp_sympy = expr.args[1]
        if exp_sympy.is_Number:
            if exp_sympy == -1:
                return 1 / base
            elif exp_sympy == 0:
                return 1
            elif exp_sympy == 1:
                return base
            elif exp_sympy == 2:
                return base * base
        exp = sympy_to_z3(exp_sympy, z3_var)
        return base ** exp
    if isinstance(expr, Abs):
        arg = sympy_to_z3(expr.args[0], z3_var)
        return z3.If(arg >= 0, arg, -arg)
    if isinstance(expr, Piecewise):
        res = sympy_to_z3(expr.args[-1][0], z3_var)
        for e, c in reversed(expr.args[:-1]):
            z3_c = sympy_cond_to_z3(c, z3_var)
            z3_e = sympy_to_z3(e, z3_var)
            res = z3.If(z3_c, z3_e, res)
        return res
    raise ValueError(f"Unsupported expr: {expr}")

def get_z3_set(S_obj, z3_var):
    if callable(S_obj):
        try:
            res = S_obj(z3_var)
            if isinstance(res, bool):
                return z3.BoolVal(res)
            return res
        except Exception:
            raise ValueError("Callable set must accept z3 Real")
    else:
        return set_to_z3(S_obj, z3_var)

def get_z3_f(f_obj, z3_var):
    if callable(f_obj):
        try:
            expr = f_obj(x)
            return sympy_to_z3(expr, z3_var)
        except Exception:
            pass
        try:
            res = f_obj(z3_var)
            if isinstance(res, (int, float)):
                return z3.RealVal(res)
            return res
        except Exception:
            raise ValueError("Callable f must accept sympy Symbol or z3 Real")
    else:
        return sympy_to_z3(f_obj, z3_var)

def z3_distance_gt_0(A_z3, B_z3, z3_var):
    d = z3.Real('d')
    x_var = z3.Real('x_dist')
    y_var = z3.Real('y_dist')
    
    A_x = z3.substitute(A_z3, (z3_var, x_var))
    B_y = z3.substitute(B_z3, (z3_var, y_var))
    
    abs_xy = z3.If(x_var > y_var, x_var - y_var, y_var - x_var)
    
    dist_gt_0 = z3.Exists(d, z3.And(
        d > 0,
        z3.ForAll([x_var, y_var], z3.Implies(
            z3.And(A_x, B_y),
            abs_xy >= d
        ))
    ))
    
    solver = z3.Solver()
    solver.set("timeout", 1000)
    solver.add(dist_gt_0)
    return solver.check() == z3.sat

def z3_is_uniformly_continuous(S_z3, f_z3, z3_var):
    e = z3.Real('e')
    d = z3.Real('d')
    x_var = z3.Real('x_uc')
    y_var = z3.Real('y_uc')
    
    S_x = z3.substitute(S_z3, (z3_var, x_var))
    S_y = z3.substitute(S_z3, (z3_var, y_var))
    f_x = z3.substitute(f_z3, (z3_var, x_var))
    f_y = z3.substitute(f_z3, (z3_var, y_var))
    
    abs_xy = z3.If(x_var > y_var, x_var - y_var, y_var - x_var)
    abs_f = z3.If(f_x > f_y, f_x - f_y, f_y - f_x)
    
    not_uc = z3.Exists(e, z3.And(
        e > 0,
        z3.ForAll(d, z3.Implies(
            d > 0,
            z3.Exists([x_var, y_var], z3.And(
                S_x, S_y,
                abs_xy < d,
                abs_f >= e
            ))
        ))
    ))
    
    solver = z3.Solver()
    solver.set("timeout", 1000)
    solver.add(not_uc)
    res = solver.check()
    if res == z3.sat:
        return False
    elif res == z3.unsat:
        return True
    else:
        return None

CONDITION_LABELS = [
    "H_1: A and B are non-empty subsets of X",
    "H_2: inf {d(a,b) | a in A, b in B} > 0",
    "H_3: f is uniformly continuous on B",
    "¬Q: f is NOT uniformly continuous on A union B"
]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        A_obj = witness['A']
        B_obj = witness['B']
        f_obj = witness['f']
    except (KeyError, TypeError):
        return [False, False, False, False]
        
    z3_var = z3.Real('z3_var')
    
    try:
        A_z3 = get_z3_set(A_obj, z3_var)
        B_z3 = get_z3_set(B_obj, z3_var)
        f_z3 = get_z3_f(f_obj, z3_var)
    except Exception:
        return [False, False, False, False]
        
    # H1: A and B are non-empty
    try:
        solver = z3.Solver()
        solver.set("timeout", 1000)
        solver.add(A_z3)
        A_ne = (solver.check() == z3.sat)
        
        solver = z3.Solver()
        solver.set("timeout", 1000)
        solver.add(B_z3)
        B_ne = (solver.check() == z3.sat)
        
        h1_ok = A_ne and B_ne
    except Exception:
        h1_ok = False
        
    # H2: inf d(A, B) > 0
    try:
        h2_ok = z3_distance_gt_0(A_z3, B_z3, z3_var)
    except Exception:
        h2_ok = False
        
    # H3: f is uniformly continuous on B
    try:
        res_h3 = z3_is_uniformly_continuous(B_z3, f_z3, z3_var)
        h3_ok = (res_h3 is True)
    except Exception:
        h3_ok = False
        
    # neg_Q: f is NOT uniformly continuous on A \cup B
    try:
        A_cup_B = z3.Or(A_z3, B_z3)
        res_nq = z3_is_uniformly_continuous(A_cup_B, f_z3, z3_var)
        neg_q_ok = (res_nq is False)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]